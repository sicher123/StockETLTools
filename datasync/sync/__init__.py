import numpy as np
import pandas as pd
from copy import copy
from datetime import datetime, timedelta
import datasync.utils as utils
import warnings
import math
warnings.filterwarnings("ignore")

def distribute(props):
    start_date = props.pop('start_date')
    end_date = props.pop('end_date')
    num = math.floor((end_date - start_date) / 10000)

    props_list = []

    for i in range(num):
        p = copy(props)
        p['start_date'] = start_date + i * 10000
        p['end_date'] = start_date + (i + 1) * 10000
        props_list.append(p)
    return props_list

config_example = {}


class SyncBase(object):
    def __init__(self,config,**kwargs):
        self.config = config
        self.cleansing_func = kwargs.get('cleansing_func')
        fp = config.pop('folder_path')
        view = config.pop('view')
        db_config = config.pop('db_config')
        origin_name = config.pop('origin')
        db_name = config.pop('db')

        self.props = config
        self.db = globals()[db_name](fp,view)
        self.origin = globals()[origin_name](db_config)
        self.logger = utils.logger(fp)

    def __str__(self):
        pass

    def get_props(self):
        return copy(self.props)

    def read(self):
        pass

    def write(self):
        pass

    def sync(self):
        pass

class DailyDataSync(SyncBase):
    def __init__(self,props):
        super(DailyDataSync, self).__init__(props)
        self.index_name = props.pop('index_name')
        self.columns_name = props.pop('columns_name')


class SingleFieldSync(DailyDataSync):
    def __init__(self):
        super(MultiFieldSync, self).__init__(db_config)

    def __call__(self, *args, **kwargs):
        return self.sync()

    def get_update_date(self):
        date = self.db.get_update_info('date')
        if date:
            self.props['start_date'] = date

    def sync(self):
        props = copy(self.config.pop())
        data = self.read(props)
        self.write(data)

    def concat_read(self,props):
        try:
            view = self.props['view']
            self.logger.info('%s start query' % (view), exc_info=True)
            df1 = self.origin.read(props=props)
            df2 = self.origin.read(props=index_config)
            df = pd.concat([df1, df2])
        except Exception as e:
            self.logger.error('%s query failed ,error as %s' % (view, e), exc_info=True)

    def read(self,props):
        try:
            view = props['view']
            self.logger.info('%s start query' % (view), exc_info=True)

            df = self.origin.read(props=props)
        except Exception as e:
            self.logger.error('%s query failed ,error as %s' % (view, e), exc_info=True)
            df = None
        return df

    def write(self,df):
        for i in df.columns:
            data = df.pivot(index='trade_date', columns='symbol', values=i)
            try:
                self.db.update_a_file(data, i)
                self.logger.info('%s - %s data has been updated' % (self.view, i), exc_info=True)
            except Exception as e:
                self.logger.error('%s - %s update failed ,error as %s' % (self.view, i, e), exc_info=True)

    def get_props(self):
        pass

class MultiFieldSync(DailyDataSync):
    def __init__(self,config):
        super(MultiFieldSync, self).__init__(config)

    def write(self,view,df):
        for i in df.columns:
            data = df.pivot(index=self.index_name, columns=self.columns_name, values=i)
            try:
                data = df.pivot(index=self.index_name, columns=self.columns_name, values=i)
                self.db.update_a_file(data, i)
                self.db.set_attr({i: today})
                self.logger.info('%s -  %s data has been updated' % (view, i), exc_info=True)
            except Exception as e:
                print(i, 'fail')
                self.logger.error('%s - %s update failed ,error as %s' % (view, i, e), exc_info=True)


class LBDataSync(SyncBase):
    def __init__(self):
        super(LBDataSync, self).__init__(db_config)


def SyncFactory(view,):
    MAP = {'guojin_daily': MultiFieldSync,
           'jaqs_index_member': LBDataSync,
           'guojin_uqer_factors': SingleFieldSync,
           'guojin_zyyx_forecast': LBDataSync,
           'jaqs_daily:': MultiFieldSync}

    return MAP.get(view)()