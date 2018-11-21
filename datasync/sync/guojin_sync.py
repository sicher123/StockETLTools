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
from datasync.data_origin.sql_origin import *
#from datasync.sync import distributed
from datasync.dataReceiver.hdf5 import DailyDB, PdHdf5DB
import datasync.utils as utils
from datetime import datetime, timedelta
from datasync.dataReceiver.sqlite import sqlite_db
from datasync.data_origin.jaqs_origin import DataServiceOrigin
from datasync.check import check_n_rollback, auto_backup


today = int(datetime.strftime(datetime.now(), '%Y%m%d'))
yestoday = int(datetime.strftime(datetime.now() - timedelta(days=1), '%Y%m%d'))


def add_date(_date, n=1):
    d = datetime.strptime(str(_date), '%Y%m%d')
    d = d + timedelta(days=n)
    d = datetime.strftime(d, '%Y%m%d')
    return d


def write(db, view, df, date_field='TRADE_DT', symbol_field='S_INFO_WINDCODE'):
    df[date_field] = df[date_field].astype(int)
    df.sort_values([date_field, symbol_field])
    if view == 'dbo.ASHAREEODPRICES':
        df = df.drop_duplicates()

    if 'S_DQ_TRADESTATUS' in df.columns.values:
        # print (df['S_DQ_TRADESTATUS'])
        df['S_DQ_TRADESTATUS'] = df['S_DQ_TRADESTATUS'].apply(
            lambda x: x.encode('latin1').decode('gbk') if isinstance(x, str) else x)
        df['S_DQ_TRADESTATUS'][df['S_DQ_TRADESTATUS'] == '交易'] = '1'
        df['S_DQ_TRADESTATUS'][df['S_DQ_TRADESTATUS'] == '停牌'] = '0'
        df['S_DQ_TRADESTATUS'][df['S_DQ_TRADESTATUS'].isin(['XR', 'XD', 'DR', 'N'])] = '1'

    for i in df.columns:
        if i not in ['TRADE_DT']:
            try:
                data = df.pivot(index=date_field, columns=symbol_field, values=i)
                if len(data.dropna(how='all')) == 0:
                    logger.info('%s -  %s values all NaN,not been updated' % (view, i), exc_info=True)
                    continue

                db.update_a_file(data, i)
                # db.set_attr({i: yestoday})
                logger.info('%s -  %s data has been updated' % (view, i), exc_info=True)
            except Exception as e:
                print(i, 'fail')
                logger.error('%s - %s update failed ,error as %s'%(view,i,e), exc_info=True)


def sync_zyyx():
    config = read_config('zyyx_data')
    for k, v in config.items():
        try:
            view = k
            fp = v.pop('folder_path')
            db = eval(v.pop('db'))(fp, file_name=view)

            newest_table = max([int(i) for i in db.all_table_names])
            info = db.get_update_info(newest_table, date_field='CON_DATE')
            if info:
                v['start_date'] = int(add_date(info))
            v['end_date'] = int(today)
            print(v)
            logger.info('query_props : %s' % (v, ))

            if isinstance(v['start_date'], int) and isinstance(v['end_date'], int):
                if v['start_date'] > v['end_date']:
                    logger.info('date -- %s ,view -- %s data is the newest' % (v['start_date'], view))
                    continue

            db_config = ast.literal_eval(v.pop('db_config'))
            origin = globals()[v.pop('origin')](db_config)
            df = origin.read(props=v)

            if len(df) == 0:
                logger.info('%s data is a empty dataframe' % (view,), exc_info=True)
                continue

            df['STOCK_CODE'] = utils.trans_symbol(list(df['STOCK_CODE'].values))
            start = int(df['CON_DATE'].min().strftime('%Y%m%d'))
            end = int(df['CON_DATE'].max().strftime('%Y%m%d'))
            num = math.floor((end - start) / 10000)

            if num > 1:
                for i in range(num):
                    s = start + i * 10000
                    e = start + (i + 1) * 10000
                    # data = store.select('data', "CON_DATE>=%s & CON_DATE<=%s" % (s, e))
                    data = df.query("CON_DATE>=%s & CON_DATE<=%s" % (s, e))
                    datetime_col = [col for col, type in data.dtypes.to_dict().items() if 'datetime' in type.name]
                    for col in datetime_col:
                        data[col] = data[col].apply(lambda x: x.strftime('%Y%m%d') if x not in [pd.NaT, np.NaN, None] else np.NaN)

                    table_name = str(s)[:4]
                    db.update_table(table_name, data, if_exists='replace')
                    logger.info('%s data has been updated in table %s' % (k, table_name), exc_info=True)
            else:
                datetime_col = [col for col, type in df.dtypes.to_dict().items() if 'datetime' in type.name]
                for col in datetime_col:
                    df[col] = df[col].apply(lambda x: x.strftime('%Y%m%d') if x not in [pd.NaT, np.NaN, None] else np.NaN)

                table_name = str(start)[:4]
                db.update_table(table_name, df, if_exists='append')
                db.conn.close()
                logger.info('%s data has been updated in table %s' % (k, table_name), exc_info=True)
        except Exception as e:
            logger.error('%s update failed ,error as %s' % (k, e), exc_info=True)


def sync_daily(large_data=None):
    config = read_config('daily_data')

    index_config = config.pop('dbo.AINDEXEODPRICES')
    index_config.pop('db_config')
    index_config.pop('origin')
    index_config.pop('folder_path')
    index_config['view'] = 'dbo.AINDEXEODPRICES'

    for k, v in config.items():
        try:
            view = k
            fp = v.pop('folder_path')
            db_config = ast.literal_eval(v.pop('db_config'))
            origin = globals()[v.pop('origin')](db_config)
            db = DailyDB(fp, view)

            date = db.get_update_info()
            if date:
                v['start_date'] = date
                index_config['start_date'] = date
            v['end_date'] = yestoday
            index_config['end_date'] = today
            v['view'] = view
            print(v)

            logger.info('%s start query' % (view, ), exc_info=True)
            if large_data:
                from datasync.sync import distribute
                for props in distribute(v):
                    df = origin.read(props=props)
            else:
                if view == 'dbo.ASHAREEODPRICES':
                    symbol_df = origin.read(props=v)
                    index_df = origin.read(props=index_config)
                    index_df['S_DQ_TRADESTATUS'] = '1'
                    df = pd.concat([index_df, symbol_df])
                else:
                    df = origin.read(props=v)
        except Exception as e:
            if e:
                logger.error('%s query failed ,error as %s' % (view, e), exc_info=True)
            else:
                logger.error('%s query failed ,error as %s' % (view, e), exc_info=True)

        if 'df' in dir() and len(df) > 0:
            write(db, view, df)
        else:
            logger.info('%s data not been updated' % (view), exc_info=True)


def sync_lb():
    config = read_config('lb_data')
    for k, v in config.items():
        try:
            view = k
            fp = v.pop('folder_path')

            db = eval(v.pop('db'))(fp)
            info = db.get_update_info(view)
            if info:
                #print(info)
                v['start_date'] = int(add_date(info))
            v['end_date'] = int(today)

            if isinstance(v['start_date'], int) and isinstance(v['end_date'], int):
                if v['start_date'] > v['end_date']:
                    logger.info('date -- %s ,view -- %s data is the newest' % (v['start_date'], view))
                    continue

            db_config = ast.literal_eval(v.pop('db_config'))
            origin = globals()[v.pop('origin')](db_config)
            df = origin.read(props=v)

            if len(df) == 0:
                logger.info('%s data is a empty dataframe' % (view,), exc_info=True)

            spc_list = ['jz.instrumentInfo', 'jz.apiParam', 'jz.secTradeCal', 'lb.indexCons', 'lb.secIndustry']
            if k in spc_list:
                db.update_table(k, df, if_exists='replace')
            else:
                db.update_table(k, df, if_exists='append')
                db.conn.close()
            logger.info('%s data has been updated' % (k, ), exc_info=True)
        except Exception as e:
            logger.error('%s update failed ,error as %s' % (k, e), exc_info=True)


def run():
    global fp
    global logger
    log_path = os.path.abspath(os.path.expanduser('~/Desktop/hdf5_docs'))
    logger = utils.logger(today, log_path)
    sync_daily()
    flag = check_n_rollback(logger, execute=True)
    sync_daily() if not np.all(list(flag.values())) else None
    auto_backup(logger)
    sync_zyyx()
    sync_lb()


if __name__ == '__main__':
    run()
