# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:34:50 2018

@author: xinger
"""
import os
import json
import errno
import codecs
import pathlib
from jaqs_fxdayu.data.dataservice import LocalDataService


def trans_symbol(symbols, dtype='standard'):
    assert dtype in ['standard', 'exchange', 'code'], 'dtype must in [standard, exchange, code]'

    def func(_symbol):
        code_list = _symbol.split('.')
        num = _symbol[0]
        try:
            int(num)
        except:
            return _symbol

        symbol = ''
        if len(code_list) == 1:
            if dtype == 'standard':
                if num == '0' or num == '3':
                    symbol = code_list[0] + '.SZ'
                elif num == '6':
                    symbol = code_list[0] + '.SH'

            elif dtype == 'exchange':
                if num == '0' or num == '3':
                    symbol = code_list[0] + '.XSHE'
                elif num == '6':
                    symbol = code_list[0] + '.XSHG'

            elif dtype == 'code':
                if num in ['0', '3', '6']:
                    symbol = code_list[0]

            return symbol

        else:
            if dtype == 'standard':
                if code_list[-1].upper() == 'SZ' or code_list[-1] == 'XSHE':
                    symbol = code_list[0] + '.SZ'
                elif code_list[-1].upper() == 'SH' or code_list[-1] == 'XSHG':
                    symbol = code_list[0] + '.SH'

            elif dtype == 'exchange':
                if code_list[-1].upper() == 'SZ' or code_list[-1] == 'XSHE':
                    symbol = code_list[0] + '.XSHE'
                elif code_list[-1].upper() == 'SH' or code_list[-1] == 'XSHG':
                    symbol = code_list[0] + '.XSHG'

            elif dtype == 'code':
                if num in ['0', '3', '6']:
                    symbol = code_list[0]

            return symbol

    if isinstance(symbols, str):
        return func(symbols)
    else:
        return [func(i) for i in symbols if func(i) != '']


def logger(date, path):
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    path = path + '//log'
    if not os.path.exists(path):
        os.makedirs(path)
    handler = logging.FileHandler(path + "//%s_log.txt"%(date))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def create_dir(filename):
    """
    Create dir if directory of filename does not exist.

    Parameters
    ----------
    filename : str

    """
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def read_json(fp):
    """
    Read JSON file to dict. Return None if file not found.

    Parameters
    ----------
    fp : str
        Path of the JSON file.

    Returns
    -------
    dict

    """
    content = dict()
    with codecs.open(fp, 'r', encoding='utf-8') as f:
        content = json.load(f)
    return content


def save_json(serializable, file_name):
    """
    Save an serializable object to JSON file.

    Parameters
    ----------
    serializable : object
    file_name : str

    """
    fn = os.path.abspath(file_name)
    create_dir(fn)

    with codecs.open(fn, 'w', encoding='utf-8') as f:
        json.dump(serializable, f, separators=(',\n', ': '))


def get_json_config(path):
    default_config = {
        "fp": os.path.join(path, "Sync", "data"),
        "mongo_db_config": {'addr': '192.168.0.104'},
        "lb_update_type": "add",
        "default_start_date": 19990101,
        "default_future_date": 20200101,
        "lb_views": ['lb.cashFlow', 'lb.income', 'lb.balanceSheet', 'lb.finIndicator',
                     'lb.indexCons', 'jz.secTradeCal', 'lb.secIndustry', 'jz.apiParam',
                     'lb.profitExpress', 'lb.secDividend', 'lb.indexWeightRange',
                     'jz.instrumentInfo', 'lb.secAdjFactor'],
        "daily_views": ['Stock_D', 'SecDailyIndicator']
    }
    config_path = path / "config" / "config.json"
    print (config_path)
    config = read_json(config_path)
    if not config:
        config = default_config
    return config


def set_predefine(fp, view):
    import os
    import sqlite3
    import pandas as pd

    conn = sqlite3.connect(fp+'//data.sqlite')
    data = pd.read_sql('''select * from "help.predefine";''', conn)
    file_names = [i.split('.')[0] for i in os.listdir(r'D:\data1year\%s' % (view, ))]

    for name in file_names:
         df = pd.DataFrame(data={'api': view,
                          'comment': '',
                          'dtype': 'Double',
                          'must': 'N',
                          'param': name,
                          'pname': '',
                          'ptype': 'OUT'},index=[0])
         data = data.append(df)
    data = data.reset_index(drop=True)
    data.to_sql("help.predefine", conn, if_exists='replace')


if __name__ == '__main__':
    get_json_config()
