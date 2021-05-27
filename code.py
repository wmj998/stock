import requests
import pandas as pd
import matplotlib.pyplot as plt
from relation_mysql import action_db
from pd_mysql import action_table
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller as ADF
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima_model import ARIMA

plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决plt中文显示的问题
plt.rcParams['axes.unicode_minus'] = False  # 解决plt负号显示的问题


def get_html(url):
    try:
        response = requests.get(url=url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.json()
    except:
        print('Error_get_html')
        return ''


def get_data(infos):
    data = []
    for info in infos:
        columns = info.keys()
        data.append(info.values())
    data = pd.DataFrame(data=data, columns=columns)
    return data


def create_db(db):
    action = action_db(host="localhost", user="root",
                       password="w_f1216570180", port=3306)
    action.create(db=db)


class Data:
    def __init__(self, db):
        self.action = action_table(user='root', password='w_f1216570180',
                                   host='localhost', port=3306, db=db)

    def save_data(self, table, data):
        self.action.save(table=table, data=data)

    def read_data(self, table):
        data = self.action.read(table)
        return data


class Df:
    def __init__(self, data):
        data['day'] = pd.to_datetime(data['day'])
        data = data.set_index('day')
        self.data = data.astype(float)

    def visual(self):
        style = ['-.', '--', '-', ':']
        self.data[['open', 'high', 'low', 'close']].plot(title='股票价格波动趋势图',
                                                         ylabel='prices', style=style)
        plt.show()
        self.data[['volume']].plot(title='股票成交量波动趋势图', ylabel='numbers')
        plt.show()

    def predict(self, number):
        columns = self.data.columns[:-1]
        predicts = []
        for column in columns:
            data = self.data[[column]]
            # data.plot(title='原始序列的时序图')
            # plot_acf(data, title='原始序列的自相关图')
            # plt.show()
            # print('原始序列的ADF检验结果为：\n', ADF(data))
            # 返回值依次为adf、pvalue、usedlag、nobs、critical values、icbest、regresults、resstore
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

        data = self.data[['volume']]
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


def main(db, table):
    url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/' \
          'CN_MarketData.getKLineData?symbol=sh600438&scale=60&ma=no&datalen=60'
    infos = get_html(url)  # 获取数据
    data = get_data(infos)  # 处理数据
    create_db(db=db)  # 创建数据库

    d = Data(db)
    d.save_data(table=table, data=data)  # 保存数据
    data = d.read_data(table=table)  # 读取数据

    df = Df(data)
    df.visual()  # 可视化
    df.predict(number=5)  # 预测,number=次数


if __name__ == "__main__":
    main(db='stock', table='prices')
