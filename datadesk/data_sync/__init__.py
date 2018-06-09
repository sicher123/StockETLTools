import numpy as np
import pandas as pd
from copy import copy
from datetime import datetime, timedelta
from jaqs.data.dataview import DataView
import warnings

warnings.filterwarnings("ignore")
from DataSync.datadesk.utils import trans_symbol


class data_sync(DataView):
    def __init__(self, fp, dv_props, ds_props):
        super(data_sync, self).__init__()
        ds = self.set_data_api(ds_props)
        self.fp = fp
        self.init_from_config(dv_props, data_api=ds)
        self.symbol = self.all_symbol
        self.indi_field = dv_props['indi_field']
        self.daily_field = dv_props['daily_field']
        self.adj_field = dv_props['adj_field']
        self.factors = dv_props['factors']
        global today
        today = int(datetime.strftime(datetime.today(), '%Y%m%d'))
        # self.conn = self.connect(data_source)

    def set_data_api(self, ds_props):
        from jaqs.data.dataservice import RemoteDataService
        ds = RemoteDataService()
        ds.init_from_config(ds_props)

    @property
    def all_symbol(self, dtype='list'):
        symbol = self.data_api.query_index_member('000001.SH', self.extended_start_date_d,
                                                  self.end_date) + self.data_api.query_index_member('399106.SZ',
                                                                                                    self.extended_start_date_d,
                                                                                                    self.end_date)
        symbol = [trans_symbol(i) for i in symbol]

        if dtype == 'list':
            return symbol

        elif dtype == 'str':
            return ",".join(symbol)

    @property
    def index(self):
        cs = self.client['lb']['indexCons'].find({}, {'_id': 0, 'index_code': 1})
        return set([i['index_code'] for i in cs])

    def n_dates(self, start_date, end_date=None):
        if not end_date:
            end_date = today
        return self.data_api.query_trade_dates(start_date, end_date)

    def normalize(self, df):
        for symbol in set(self.symbol) - set(df.columns):
            df[symbol] = np.nan

        return df.loc[self.dates, self.symbol]
