import pymysql
import pandas as pd


# 数据库
class action_db:
    def __init__(self, host, user, password, port):
        self.connect = pymysql.connect(host=host, user=user, password=password, port=port)
        self.cursor = self.connect.cursor()

    # 创建数据库
    def create(self, db):
        sql = f"CREATE DATABASE {db}"
        self.cursor.execute(sql)
        self.connect.close()

    # 删除数据库
    def drop(self, db):
        sql = f"DROP DATABASE {db}"
        self.cursor.execute(sql)
        self.connect.close()


# 数据表
class action_table:
    def __init__(self, host, user, password, port, db):
        self.connect = pymysql.connect(host=host, user=user, password=password, port=port, db=db)
        self.cursor = self.connect.cursor()

    # 创建数据表
    def create(self, table, information):
        sql = f"CREATE TABLE {table} ({information})"
        self.cursor.execute(sql)
        self.connect.close()

    # 删除数据表
    def drop(self, table):
        sql = f"DROP TABLE {table}"
        self.cursor.execute(sql)
        self.connect.close()

    # 查询数据
    def query(self, table, what):
        sql = f'SELECT {what} FROM {table}'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        description = self.cursor.description
        self.connect.close()
        columns = []
        for column in description:
            columns.append(column[0])
        data = list(map(list, data))
        data = pd.DataFrame(data, columns=columns)
        print(data)

    # 插入数据
    def insert(self, table, keys, values):
        keys = ','.join(keys)
        values = tuple(values)
        sql = f"INSERT INTO {table}({keys}) VALUES{values}"
        self.cursor.execute(sql)
        self.connect.commit()
        self.connect.close()

    # 修改数据
    def update(self, table, set, where):
        sql = f"UPDATE {table} SET {set} WHERE {where}"
        self.cursor.execute(sql)
        self.connect.commit()
        self.connect.close()

    # 删除数据
    def delete(self, table, where):
        sql = f"DELETE FROM {table} WHERE {where}"
        self.cursor.execute(sql)
        self.connect.commit()
        self.connect.close()
