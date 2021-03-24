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

# 解析数据
def processing(rs):
    try:
        x = []  # day
        y1 = []  # open
        y2 = []  # high
        y3 = []  # low
        y4 = []  # close
        y5 = []  # volume
        for one in rs:
            x.append(one[0])
            y1.append(float(one[1]))
            y2.append(float(one[2]))
            y3.append(float(one[3]))
            y4.append(float(one[4]))
            y5.append(float(one[5]))
        print("解析数据成功")
        return x, y1, y2, y3, y4, y5
    except:
        print("Error-processing")
        return ""

# 数据预测
def forecast(x, y1, y2, y3, y4, y5):
    try:
        df = pd.DataFrame([y1, y2, y3, y4, y5], index=['open', 'high', 'low', 'close', 'volume'], columns=x)

        train_x = df[x[:int(len(x) / 2) - 1]]
        train_y = df[[x[int(len(x) / 2) - 1]]]
        test_x = df[x[int(len(x) / 2):len(x) - 1]]

        x_train = np.array(train_x)
        y_train = np.array(train_y)
        x_test = np.array(test_x)

        # knn拟合预测
        # knn = KNeighborsClassifier(n_neighbors=6)
        # knn.fit(x_train, y_train.astype('str'))
        # y_test = knn.predict(x_test)

        # svc拟合预测
        # svc = SVC(kernel='rbf', probability=True)
        # svc.fit(x_train, y_train.astype('str'))
        # y_test = svc.predict(x_test)

        # 感知器分类
        # ppn = Perceptron()
        # ppn.fit(x_train, y_train.astype('str'))
        # y_test = ppn.predict(x_test)

        # logistic分类
        # lr = LogisticRegression(C=1000.0, random_state=0)
        # lr.fit(x_train, y_train.astype('str'))
        # y_test = lr.predict(x_test)

        # 决策树分类
        # tree = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=0)
        # tree.fit(x_train, y_train.astype('str'))
        # y_test = tree.predict(x_test)

        # 随机森林分类
        forest = RandomForestClassifier(criterion='entropy', n_estimators=10, random_state=1, n_jobs=2)
        forest.fit(x_train, y_train.astype('str'))
        y_test = forest.predict(x_test)

        print('open:', y_test[0], '\nhigh:', y_test[1], '\nlow:', y_test[2], '\nclose:', y_test[3], '\nvolume:',y_test[4])
    except:
        print("Error-forecast")
        return ""

# 绘图
def Drawing(x, y1, y2, y3, y4, y5):
    try:

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

        plt.title("股票volume波动图")
        plt.xlabel("时间")
        plt.ylabel("volume")
        plt.plot(x, y5, label="close")  # 折线图
        plt.legend()  # 图例
        plt.show()

        print("绘图成功")
    except:
        print("Error-Drawing")
        return ""

def main():
    num = int(input("请输入数量："))
    time = input("请输入时间间隔（分钟）：")  # 30
    url = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sh600438&scale=" + time + "&ma=no&datalen=" + str(num)
    html = getHTMLText(url)
    getData(html,num)
    rs = takeData()
    Tuple = processing(rs)
    L = list(Tuple)
    forecast(L[0],L[1],L[2],L[3],L[4],L[5])
    Drawing(L[0],L[1],L[2],L[3],L[4],L[5])

if __name__ == "__main__":
    main()
