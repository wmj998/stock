import pandas as pd
import requests
from matplotlib import pyplot as plt
from pymongo import MongoClient
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller as ADF
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima_model import ARIMA

plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决plt中文显示的问题
plt.rcParams['axes.unicode_minus'] = False  # 解决plt负号显示的问题


def col(host='localhost', port=27017, db='stock', collection='price'):
    client = MongoClient(host=host, port=port)
    db = client[db]
    collection = db[collection]
    return collection


def get(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        documents = response.json()
        collection = col()
        collection.insert_many(documents)
    except Exception as e:
        print(e)


def read():
    collection = col()
    documents = collection.find()
    return documents


def handle(data):
    df = pd.DataFrame(data)
    df.drop(columns='_id', inplace=True)
    df.set_index('day', inplace=True)
    df = df.astype(float, copy=False)
    return df


def draw(df):
    style = ['-.', '--', '-', ':']
    df[['open', 'high', 'low', 'close']].plot(title='股票价格波动趋势图', ylabel='prices', style=style)
    # plt.show()
    df[['volume']].plot(title='股票成交量波动趋势图', ylabel='numbers')
    plt.show()


def predict(df, number=5):
    columns = df.columns[:-1]
    predicts = []
    for column in columns:
        data = df[[column]]

        # data.plot(title='原始序列的时序图')
        # plot_acf(data, title='原始序列的自相关图')
        # plt.show()
        # print('原始序列的ADF检验结果为：\n', ADF(data))
        # # 返回值依次为adf、pvalue、usedlag、nobs、critical values、icbest、regresults、resstore
        #
        # d_data = data.diff().dropna()
        # d_data.plot(title='一阶差分之后序列的时序图')
        # plot_acf(d_data, title='一阶差分之后序列的自相关图')
        # plot_pacf(d_data, title='一阶差分之后序列的偏自相关图')
        # plt.show()
        # print('差分序列的ADF检验结果为：\n', ADF(d_data))
        # print('差分序列的白噪声检验结果为：\n', acorr_ljungbox(d_data, lags=1))  # 返回统计量和p值

        # 定阶
        pmax = int(len(data) / 10)  # 一般阶数不超过length/10
        qmax = int(len(data) / 10)  # 一般阶数不超过length/10
        bic_matrix = []  # BIC矩阵
        for p in range(pmax):
            tmp = []
            for q in range(qmax):
                try:  # 存在部分报错，所以用try来跳过报错
                    tmp.append(ARIMA(data, (p, 1, q)).fit().bic)
                except:
                    tmp.append(None)
            bic_matrix.append(tmp)
        bic_matrix = pd.DataFrame(bic_matrix)
        p, q = bic_matrix.stack().idxmin()  # 先用stack展平，然后用idxmin找出最小值位置
        # print('BIC最小的p值和q值为：%s、%s' % (p, q))
        model = ARIMA(data, (p, 1, q)).fit()
        # print('模型报告为：\n', model.summary2())
        column = model.forecast(number)
        predicts.append(column)

    data = df[['volume']]
    # data.plot(title='原始序列的时序图')
    # plot_acf(data, title='原始序列的自相关图')
    # plt.show()
    # print('原始序列的ADF检验结果为：\n', ADF(data))
    # # 返回值依次为adf、pvalue、usedlag、nobs、critical values、icbest、regresults、resstore
    # print('原始序列的白噪声检验结果为：\n', acorr_ljungbox(data, lags=1))  # 返回统计量和p值

    # 定阶
    pmax = int(len(data) / 10)  # 一般阶数不超过length/10
    qmax = int(len(data) / 10)  # 一般阶数不超过length/10
    bic_matrix = []  # BIC矩阵
    for p in range(pmax):
        tmp = []
        for q in range(qmax):
            try:  # 存在部分报错，所以用try来跳过报错
                tmp.append(ARIMA(data, (p, 0, q)).fit().bic)
            except:
                tmp.append(None)
        bic_matrix.append(tmp)
    bic_matrix = pd.DataFrame(bic_matrix)
    p, q = bic_matrix.stack().idxmin()  # 先用stack展平，然后用idxmin找出最小值位置
    # print('BIC最小的p值和q值为：%s、%s' % (p, q))
    model = ARIMA(data, (p, 0, q)).fit()
    # print('模型报告为：\n', model.summary2())
    predict_volume = model.forecast(number)

    print('预测结果、标准误差、置信区间：', '\nopen：', predicts[0],
          '\nhigh：', predicts[1], '\nlow：', predicts[2],
          '\nclose：', predicts[3], '\nvolume：', predict_volume)


def main():
    url = 'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sh600438&scale=60&ma=no&datalen=60'
    get(url)
    documents = read()
    df = handle(documents)
    draw(df)
    predict(df)


if __name__ == '__main__':
    main()
