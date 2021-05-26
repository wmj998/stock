import pandas as pd
from sqlalchemy import create_engine


class action_table:
    def __init__(self, user, password, host, port, db):
        self.engine = create_engine(
            f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4')

    def read(self, table):
        data = pd.read_sql(f'SELECT * FROM {table}', con=self.engine)
        return data

    def save(self, table, data):
        data.to_sql(table, con=self.engine, index=False)
