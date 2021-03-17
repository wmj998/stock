import requests
import pymysql
import matplotlib.pyplot as plt

# 获取数据
def getHTMLText(url):
    try:
        data = requests.get(url)
        print("获取数据成功")
        return data.text
    except:
        print("Error-getHTMLText")
        return ""

# 存储数据
def addData(information):
    try:
        con = pymysql.Connect("localhost", "root", "123456", "gp")  # 连接mysql（用户名，密码，库名）
        cur = con.cursor()  # 获取游标
        cur.execute("insert into shares(day,open,high,low,close,volume) values(%s,%s,%s,%s,%s,%s)", information)
        con.commit()  # 提交
        print("存储数据成功")
    except:
        print("Error-addData")
        return ""

# 处理数据
def getData(html,num):
    try:
        alls = []
        for i in range(0, 6 * num):  # 属性个数* 数量    提取数据
            all = html.split('"')[3 + 4 * i]
            alls.append(all)

        for i in range(0, num):  # 分隔数据
            datas = []
            for j in range(0, 6):
                data = alls[j + i * 6]
                datas.append(data)
            addData(datas)
        print("处理数据成功")
    except:
        print("Error-getData")
        return ""

# 导出数据
def takeData():
    try:
        con = pymysql.Connect("localhost", "root", "123456", "gp")  # 连接mysql
        cur = con.cursor()  # 获取游标
        cur.execute("select * from shares")  # ""引号内sql查询语句
        print("导出数据成功")
        return cur.fetchall()  # 获取记录集
    except:
        print("Error-takeData")
        return ""

# 绘图
def Drawing(rs):
    try:
        x = []  # day
        y1 = []  # open
        y2 = []  # high
        y3 = []  # low
        y4 = []  # close
        for one in rs:
            x.append(one[0])
            y1.append(float(one[1]))
            y2.append(float(one[2]))
            y3.append(float(one[3]))
            y4.append(float(one[4]))
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决plt中文显示的问题
        plt.rcParams['axes.unicode_minus'] = False  # 解决plt负号显示的问题
        plt.title("股票价格波动趋势")
        plt.xlabel("时间")
        plt.ylabel("价格")
        # plt.scatter(x, y1)  # 散点图
        # plt.scatter(x, y2)  # 散点图
        # plt.scatter(x, y3)  # 散点图
        # plt.scatter(x, y4)  # 散点图
        plt.plot(x, y1, label="open", linewidth=1, linestyle=':')   # 折线图
        plt.plot(x, y2, label="high", linewidth=1, linestyle='-.')  # 折线图
        plt.plot(x, y3, label="low", linewidth=1, linestyle='--')   # 折线图
        plt.plot(x, y4, label="close", linewidth=1, linestyle='-')  # 折线图
        plt.legend()  # 图例
        plt.show()
        print("绘图成功")
    except:
        print("Error-Drawing")
        return ""

def main():
    num = int(input("请输入数量："))
    time = input("请输入时间间隔（分钟）：")
    url = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sh600438&scale=" + time + "&ma=no&datalen=" + str(num)
    html = getHTMLText(url)
    getData(html,num)
    rs = takeData()
    Drawing(rs)

if __name__ == "__main__":
    main()
