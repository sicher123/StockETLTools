import os
import openpyxl
import numpy as np
import pandas as pd


class ExcelStorage(object):
    def __init__(self, path):
        self.path = path
        self.file_name = None

    def insert(self, df, names):
        if type(names) == str:
            names = names.split(',')
        for i in range(len(names)):
            path = self.path(names[i])
            df[i].to_excel(path)
            print('{}.xlsx已写完'.format(names[i]))

    def update(self, df):
        df.to_excel(self.path)
        print('{}.xlsx数据更新完成'.format(self.file_name))

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


class CSVFile(object):
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @property
    def sheet_names(self):
        return [i[1:] for i in self.store.keys()]

    def write(self, df, sheet_name='data'):
        try:
            df.to_csv(self.path, mode='w', sheet_name=sheet_name)
        except Exception as e:
            return e

    def append(self, df, sheet_name='data'):
        try:
            df.to_csv(self.path, mode='a', sheet_name=sheet_name)
        except Exception as e:
            return e

    def curtail(self):
        pass

    def get_update_info(self):
        pass


class CSVStorage(object):
    def __init__(self, fp):
        self.fp = fp

    def path_generater(self, doc_name):
        if not os.path.exists(self.fp):
            os.mkdir(self.fp)
        return self.fp + '\\' + doc_name + '.csv'

    def update(self, df):
        pass

