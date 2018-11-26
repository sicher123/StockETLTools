# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:34:50 2018

@author: xinger
"""
import os
from datetime import datetime


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


def int2datetime(str_time):
    return datetime.strptime(str_time.format(dir[2:10]),'%Y%m%d %H:%M:%S')


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


def check_log(path, _string):
    res = {}
    lst = []
    with open(path, mode='r') as file:
        for row in list(file):
            lst.append(row) if _string in row else 1
    return lst


'''
path = r'C:\\Users\\xinger\Desktop\dyupdater.log'
_str = 'Update finish'
info = check_log(path, _str)
'''

