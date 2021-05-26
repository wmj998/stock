import requests
import pandas as pd
import matplotlib.pyplot as plt
from relation_mysql import action_db
from pd_mysql import action_table


def get_html(url):
    try:
        response = requests.get(url=url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.json()
    except:
        print('Error_get_html')
        return " "


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
    def __init__(self):
        self.action = action_table(user='root', password='w_f1216570180',
                                   host='localhost', port=3306, db='stock')

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
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决plt中文显示的问题
        plt.rcParams['axes.unicode_minus'] = False  # 解决plt负号显示的问题
        linestyle = ['-.', '--', '-', ':']
        self.data[['open', 'high', 'low', 'close']].plot(title='股票价格波动趋势',
                                                         ylabel='prices', style=linestyle)
        self.data[['volume']].plot(title='股票成交量波动趋势', ylabel='numbers')
        plt.show()

    # def predict(self):
    #     model = Prophet().fit(self.data)
    #     future = model.make_future_dataframe(freq='D', periods=365)
    #     forecast = model.predict(future)
    #     return forecast


def main():
    url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/' \
          'CN_MarketData.getKLineData?symbol=sh600438&scale=60&ma=no&datalen=200'
    infos = get_html(url)
    data = get_data(infos)
    create_db(db='stock')
    Data().save_data(table='prices', data=data)
    data = Data().read_data(table='prices')
    df = Df(data)
    df.visual()


if __name__ == "__main__":
    main()
