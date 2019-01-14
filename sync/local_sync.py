# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:34:50 2018

@author: xinger
"""
import os
import ast
import math
import numpy as np
import pandas as pd
from datasync.props.guojin_props import read_config
from datasync.origin.sql_origin import *
from datasync.storage.hdf5 import DailyDB
import datasync.utils as utils
from datetime import datetime, timedelta
from datasync.storage.sqlite import SqliteDB
from datasync.origin.jaqs_origin import DataServiceOrigin
from datasync.check import check_n_rollback, auto_backup


today = int(datetime.strftime(datetime.now(), '%Y%m%d'))
yestoday = int(datetime.strftime(datetime.now() - timedelta(days=1), '%Y%m%d'))

lb_views = ['lb.secIndustry', 'jz.instrumentInfo', 'lb.indexWeightRange']
daily_views = ['dbo.AINDEXEODPRICES', 'dbo.ASHAREEODDERIVATIVEINDICATOR', 'dbo.ASHAREEODPRICES']
zyyx_views = ['ZYYX.CON_FORECAST_STK', 'ZYYX.CON_RATING_STK']


def add_date(_date, n=1):
    d = datetime.strptime(str(_date), '%Y%m%d')
    d = d + timedelta(days=n)
    d = datetime.strftime(d, '%Y%m%d')
    return d


def get_props(db, origin, props, limit=20):
    '''
    分段同步数据；
    从db获取本地文件更新记录；
    从origin获取数据源更新记录；
    比较时间，更新props
    '''
    start_date = props.get('start_date')
    end_date = props.get('end_date', today)
    view = props.get('view')
    is_distribute = props.pop('distribute')

    if type(origin).__name__ == 'MongodbOrigin':
        mongo_log = origin.get_last_log()
        if view.replace('.', '_') in mongo_log.columns:
            update_flag = mongo_log[view.replace('.', '_')][0]
            if update_flag <= 0:
                return
            else:
                end_date = int(mongo_log.index[0])

    #info = db.get_update_info(view)
    date_info = db.get_update_info()
    if date_info:
        # print(info)
        start_date = int(add_date(date_info))

    if isinstance(view['start_date'], int) and isinstance(view['end_date'], int):
        if view['start_date'] > view['end_date']:
            logger.info('date -- %s ,view -- %s data is the newest' % (view['start_date'], view))
            return

    if is_distribute:
        new_props = []
        num = math.floor((end_date - start_date) / 10000) + 1
        for i in range(int(num)):
            props['start_date'] = start_date + i * 10000
            if start_date + (i + 1) * 10000 < end_date:
                props['end_date'] = start_date + (i + 1) * 10000
            else:
                props['end_date'] = end_date
            new_props.append(props.copy())
    else:
        new_props = props
        new_props['start_date'] = start_date
        new_props['end_date'] = end_date
    return new_props


def spc_treatment(view, df):
    '''
    需要特殊处理的表
    '''
    if view == 'dbo.ASHAREEODPRICES':
        df = df[~df['OBJECT_ID'].isin(['{56FBE7CC-D183-11E6-A487-6C0B84A6895D}', '{56FBE85B-D183-11E6-A487-6C0B84A6895D}'])]

        if 'S_DQ_TRADESTATUS' in df.columns.values:
            df['S_DQ_TRADESTATUS'] = df['S_DQ_TRADESTATUS'].apply(lambda x: x.encode('latin1').decode('gbk') if isinstance(x, str) else x)
            df['S_DQ_TRADESTATUS'][df['S_DQ_TRADESTATUS'] == '交易'] = '1'
            df['S_DQ_TRADESTATUS'][df['S_DQ_TRADESTATUS'] == '停牌'] = '0'
            df['S_DQ_TRADESTATUS'] = df['S_DQ_TRADESTATUS'].replace('XR', '1').replace('XD', '1').replace('DR', '1')

    if view == 'dbo.AINDEXEODPRICES':
        if 'S_DQ_TRADESTATUS' in df.columns:
            df = df.drop('S_DQ_TRADESTATUS', axis=1)
        df['S_DQ_TRADESTATUS'] = '1'

    if 'ZYYX' in view:
        df['STOCK_CODE'] = utils.trans_symbol(list(df['STOCK_CODE'].values))
        '''
        df['CON_DATE'] = df['CON_DATE'].apply(
            lambda x: datetime.strftime(x.to_datetime(), '%Y%m%d') if x != pd.NaT else 'NaT')

        def func(x):
            if len(x) == 10:
                return x[:4] + x[5:7] + x[-2:]
            else:
                return x

        for field in ['CON_OR_HISDATE', 'CON_NP_HISDATE', 'CON_EPS_HISDATE', 'ENTRYTIME', 'UPDATETIME']:
            if field in df.columns:
                df[field] = df[field].astype(str)
                df[field] = df[field].apply(lambda x: func(x))
        '''
    return view, df


class Updater(object):
    '''
    一个种更新模式对应一个updater
    '''
    def __init__(self):
        pass

    def __call__(self, db, view, df, **kargs):
        if view in lb_views:
            self.lb_updater(df, view, if_exists=kargs.get('if_exists'))

        if view in daily_views:
            self.daily_updater(db, view, df)

        if view in zyyx_views:
            self.zyyx_updater(db, view, df)

    @staticmethod
    def daily_updater(db, view, df):
        df['TRADE_DT'] = df['TRADE_DT'].astype(int)
        view, df = spc_treatment(view, df)

        for i in df.columns:
            try:
                data = df.pivot(index='TRADE_DT', columns='S_INFO_WINDCODE', values=i)

                if i in ['TRADE_DT', 'S_INFO_WINDCODE']:
                    pass
                else:
                    db.update_a_file(data, i)
                logger.info('%s -  %s data has been updated' % (view, i), exc_info=True)
            except Exception as e:
                print(view, i, 'fail')
                logger.error('%s - %s update failed ,error as %s' % (view, i, e), exc_info=True)

    @staticmethod
    def lb_sql_updater(db, view, df, if_exists='append'):
        view, df = spc_treatment(view, df)

        spc_list = ['jz.instrumentInfo', 'jz.apiParam', 'jz.secTradeCal', 'lb.indexCons', 'lb.secIndustry',
                    'lb.indexWeightRange']
        try:
            if view in spc_list:
                db.update_table(view, df, if_exists='replace')
            else:
                db.update_table(view, df, if_exists='append')
                db.set_attr(view)
                db.conn.close()
        except Exception as e:
            print('updated failed', view, e)
            pass

    @staticmethod
    def lb_hdf5_updater(db, view, df, if_exists='append'):
        view, df = spc_treatment(view, df)
        try:
            db.append(view + '_static', df)
        except Exception as e:
            print('updated failed', view, e)
            pass

    @staticmethod
    def zyyx_updater(db, view, df, if_exists='replace'):
        try:
            start_year = int(df['CON_DATE'].min().strftime('%Y%m%d')[:4])
            end_year = int(df['CON_DATE'].max().strftime('%Y%m%d')[:4])
            num = end_year - start_year

            if num > 1:
                for i in range(num):
                    s = int(str(start_year + i) + '0101')
                    e = int(start_year + (i + 1) + '0101')
                    # data = store.select('data', "CON_DATE>=%s & CON_DATE<=%s" % (s, e))
                    data = df.query("CON_DATE>=%s & CON_DATE<=%s" % (s, e))
                    datetime_col = [col for col, type in data.dtypes.to_dict().items() if 'datetime' in type.name]
                    for col in datetime_col:
                        data[col] = data[col].apply(lambda x: x.strftime('%Y%m%d') if x not in [pd.NaT, np.NaN, None] else np.NaN)

                    table_name = str(s)[:4]
                    db.update_table(table_name, data, if_exists=if_exists)
                    logger.info('%s data has been updated in table %s' % (view, table_name), exc_info=True)
            else:
                datetime_col = [col for col, type in df.dtypes.to_dict().items() if 'datetime' in type.name]
                for col in datetime_col:
                    df[col] = df[col].apply(lambda x: x.strftime('%Y%m%d') if x not in [pd.NaT, np.NaN, None] else np.NaN)

                table_name = str(start_year)
                db.update_table(table_name, df, if_exists='append')
                db.conn.close()
                logger.info('%s data has been updated in table %s' % (k, table_name), exc_info=True)
        except Exception as e:
            logger.error('%s update failed ,error as %s' % (k, e), exc_info=True)



'''
def sync_daily(view, origin, large_data=False):
            if view == 'dbo.ASHAREEODPRICES':
                symbol_df = origin.read(props=view)
                index_df = origin.read(props=index_config)
                df = pd.concat([index_df, symbol_df])
            else:
                df = origin.read(props=view)
'''


def run(configs):
    '''
    if 'index_config' not in globals():
        global index_config
    index_config = config.pop('dbo.AINDEXEODPRICES')
    index_config.pop('db_config')
    index_config.pop('origin')
    index_config.pop('folder_path')
    index_config['view'] = 'dbo.AINDEXEODPRICES'
    '''

    for config in configs.values():
        view = config.get('view')

        _db = eval(config.pop('db'))
        db = _db(config.pop('folder_path'), view)
        _origin = eval(config.pop('origin'))
        db_config = ast.literal_eval(config.pop('db_config'))
        origin = _origin(db_config)

        config['distribute'] = True
        nprops = get_props(db, origin, config)

        if isinstance(nprops, list):
            for p in nprops:
                try:
                    print(p)
                    df = origin.read(p)
                    updater = Updater()

                    if 'df' in dir() and len(df) > 0:
                        updater(db, view, df)
                    else:
                        logger.info('%s data not been updated' % (view), exc_info=True)

                except Exception as ValueError:
                    print('empty dataframe')
                    continue

        elif not nprops:
            print('newest')
        else:
            df = origin.read(nprops)
            Updater(db, view, df)


if __name__ == "__main__":
    log_path = os.path.abspath(os.path.expanduser('~/Desktop/hdf5_docs'))
    logger = utils.logger(today, log_path)
    config_path = os.path.abspath(os.path.join(os.getcwd(), "../config/config.xlsx"))
    config = read_config('Sheet1', config_path=config_path)
    run(config)
    flag = check_n_rollback(logger, config=config['dbo.ASHAREEODPRICES'], execute=True)
    auto_backup(logger)


