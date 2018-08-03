import pandas as pd
from WindPy import w
from stockds.origin import DataOrigin


class WindOrigin(DataOrigin):
    def __init__(self):
        self.signinWind()
        self.conn = None

    def connect(self):
        """登录wind"""
        w.start()
        self.conn = w
        if self.conn.isconnected():
            print("WIND API connected successfully")
        else:
            print("WIND API connected failed")

    def data(self, props):

        d = w.wsd(symbol, field, start_date, end_date, setting)

        if d.ErrorCode == 0:
            data = pd.DataFrame(data=d.Data, index=d.Fields, columns=d.Times).T.reset_index()

            return data
        else:
            print("找不到{}合约数据".format(symbol))

