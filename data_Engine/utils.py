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

def create_df(n_date = 100, n_code = 300,):
    date = pd.date_range('2012-01-01',periods=n_date)
    df1 = list(map(lambda x:pd.DataFrame({"code":str(60000+x),'date':date,'open':np.random.randn(n_date),'high':np.random.randn(n_date),'low':np.random.randn(n_date),'close':np.random.randn(n_date),'volume':np.random.randn(n_date),'ret':np.random.randn(n_date),'amt':np.random.randn(n_date)}),range(n_code)))
    df = pd.concat(df1)
    return df

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

def lastTradeDate():
    """获取最近一个交易日"""
    today = datetime.now()
    oneday = timedelta(1)
    
    if today.weekday() == 5:
        today = today -oneday
    elif today.weekday() == 6:
        today = today -oneday*2    
    return today.strftime("%Y%m%d")

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
