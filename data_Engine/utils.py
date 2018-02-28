# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 14:37:32 2018

@author: xinger
"""
import pandas as pd
import numpy as np
import pymongo
from time import time
from datetime import datetime, timedelta

now = datetime.now()
str_now = datetime.strftime(now,"%Y%m%d")
#datetime
start = datetime(2017, 5, 10, 0, 0)
end = datetime(2018, 1, 22, 0, 0)

#str_datetime
start = '20170101'
end = '20180101'


def float_or_string(value):
    try:
        ret = float(value)
    except Exception:
        ret = value
    return ret

def trans_symbol(_symbol,dtype = 'standard'):
    assert dtype in  ['standard','exchange','code']
    code_list = _symbol.split('.')
    
    if dtype == 'standard':   
        if code_list[1] == 'XSHE':
            symbol = code_list[0] + '.SZ'
        elif code_list[1] == 'XSHG':
            symbol = code_list[0] + '.SH'
        else:
            raise Exception('wrong symbol type !', symbol)
    elif dtype == 'exchange':
        if code_list[1] == 'SZ' or code_list[1] == 'sz':
            symbol = code_list[0] + '.XSHE'
        elif code_list[1] == 'SH' or code_list[1] == 'sh':
            symbol = code_list[0] + '.XSHG'
        else:
            raise Exception('wrong symbol type !', symbol)
    elif dtype == 'code':
        symbol = code_list[0]
    return symbol


def dataformat(df):
    '''
    Input : DataFrame    concat-axis = 0   
    '''
    
    num = df.columns.unique()
    symbol = []
    for i in df['symbol'][:num].T.values[0]:
         symbol += list(i)
    
    arrays = [symbol,list(df.columns)]
    df.columns = pd.MultiIndex.from_arrays(arrays, names=('symbol', 'fields'))
    return df



















'''
def parseConfigure():
    """读取configure内容"""
    import ConfigParser
    config = ConfigParser.ConfigParser()
    try:
        config.read('configure.py')
        sections = config.sections()
        field = []
        for section in sections[:3]:
            field.extend(config.options(section))
        field = field
    
        other  = None
    except Exception as e:
        print ("parse configure failed".format(e))
    else:
        print ("parse configure successfully")
'''
