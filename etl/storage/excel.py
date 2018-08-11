import os
import openpyxl
import pandas as pd
from stockds.storage import FileStorageBase

def dataframe_to_rows:
    pass

class Excel(FileStorageBase):
    def __init__(self, root, dir_name):
        self.root = root
        self.dir_name = dir_name

    def path(self, doc_name):
        if not os.path.exists(self.root + '\\' + self.dir_name):
            os.mkdir(self.root + '\\' + self.dir_name)
        return self.root + '\\' + self.dir_name + '\\' + doc_name + '.xlsx'

    def insert(self, df, names):
        if type(names) == str:
            names = names.split(',')
        for i in range(len(names)):
            path = self.path(names[i])
            df[i].to_excel(path)
            print('{}.xlsx已写完'.format(names[i]))

    def update(self, df, names):
        if type(names) == str:
            names = names.split(',')
        for i in range(len(names)):
            path = self.path(names[i])

            wb = openpyxl.load_workbook(path)
            ws = wb['Sheet1']

            [ws.append(r) for r in dataframe_to_rows(df[i], index=True, header=False)]
            wb.save(path)

        print('{}.xlsx数据更新完成'.format(doc_name))

    def find(self, prop):
        symbols = prop['symbol'].split(',')
        fields = prop['fields'].split(',')
        start_date = prop['start_date']
        end_date = prop['end_date']

        data = []
        for s in symbols:
            doc_name = self.root + '\\' + self.dir_name + '\\' + s + '.xlsx'
            dt = pd.read_excel(doc_name).set_index('trade_date')
            data.append(dt.loc[start_date:end_date, fields])
        return pd.concat(data)

    def delete(self):
        pass


def test():
    db_config = {}
    from stockds.origin.mongodb_origin import MongodbOrigin
    origin = MongodbOrigin()
