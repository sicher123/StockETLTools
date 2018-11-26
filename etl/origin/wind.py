import pandas as pd
from WindPy import w
from datetime import datetime
from etl.origin import DataOrigin
from etl.utils import trans_symbol

now = datetime.now()

sectorID = {}
sectorID['all'] = 'a001010100000000'     # u"全部A股"
sectorID['SME'] = 'a001010400000000'     # u"中小板"
sectorID['GEM'] = 'a001010r00000000'     # u"创业板 "
sectorID['HS300'] = 'a001030201000000'   # u'沪深300'
sectorID['ZZ500'] = 'a001030208000000'   # u'中证500'


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

    def get_index(self):
        pass

    def get_all_symbol(self,sector = 'all',dtype = 'exchange'):
        _id = sectorID.get(sector)
        data = self.w.wset("SectorConstituent", date=now, sectorId=_id).Data[1]
        return [trans_symbol(d, dtype=dtype) for d in data]

    def data(self, props):
        symbol = props.get('symbol')
        field = props.get('field')
        start_date = props.get('start_date')
        end_date = props.get('end_date')
        setting = props.get('setting')

        d = w.wsd(symbol, field, start_date, end_date, setting)

        if d.ErrorCode == 0:
            data = pd.DataFrame(data=d.Data, index=d.Fields, columns=d.Times).T.reset_index()

            return data
        else:
            print("找不到{}合约数据".format(symbol))

