# -*- coding: utf-8 -*-
"""
Created on Wed May  9 22:34:50 2018

@author: xinger
"""
import pandas as pd
from datetime import datetime
import openpyxl
import os

path = os.path.abspath(os.path.expanduser('~/Desktop/hdf5_docs'))
daily_db = ['dbo.ASHAREEODPRICES','dbo.ASHAREEODDERIVATIVEINDICATOR','dbo.AINDEXEODPRICES']
lb_db = 'dbo.AINDEXMEMBERS','dbo.ASHAREBALANCESHEET', 'dbo.ASHARECALENDAR','dbo.ASHARECASHFLOW','dbo.ASHAREDESCRIPTION',\
        'dbo.ASHAREDIVIDEND','dbo.ASHAREFINANCIALINDICATOR','dbo.ASHAREINCOME','dbo.ASHAREPROFITEXPRESS','dbo.ASHARETRADINGSUSPENSION'

index = ['000906.SH','000009.SH','000008.SH','399004.SZ','399333.SZ','399107.SZ',
         '399001.SZ','399100.SZ','399008.SZ','000002.SH','000003.SH','000017.SH',
         '399006.SZ','000012.SH','399003.SZ','000001.SH','000905.SH','000016.SH',
         '000011.SH','399106.SZ','399108.SZ','399606.SZ','000010.SH','399101.SZ',
         '399005.SZ','000300.SH','399002.SZ','399102.SZ','000852.SH']

start_date = 20080101

mssql_config = {'addr': "172.16.100.7",
             'user': "bigfish01",
             'password': "bigfish01@0514"}

oracle_config = {'addr': "172.16.55.54:1521/ORCL",
             'user': "bigfish",
             'password': "bigfish"}

addr = "tcp://data.tushare.org:8910"
name = "13243828068"
passwd = "eyJhbGciOiJIUzI1NiJ9.eyJjcmVhdGVfdGltZSI6IjE1MTUwNDk5MzI2MDAiLCJpc3M" \
         "iOiJhdXRoMCIsImlkIjoiMTMyNDM4MjgwNjgifQ.KpmnMkuO7ApTWvBAwgvHwWDkmoas" \
         "BIdQHl2gQJVmqIA"

remote_jaqs_config = {'addr': addr,
                      'name': name,
                      'password': passwd}


def set_config():
    dic = {}
    for i in daily_db:
        dic[i] = {}
        data = pd.read_excel(r'datasync/config/name_map.xlsx')
        fields = data['windColumnName'][data['windTableName'] == i].values
        dic[i]['fields'] = ','.join(set(list(fields) + ['S_INFO_WINDCODE', 'TRADE_DT','OBJECT_ID']))
        dic[i]['db_config'] = mssql_config
        dic[i]['start_date'] = start_date
        dic[i]['origin'] = 'MSSqlOrigin'
        dic[i]['folder_path'] = path
        dic[i]['DATE_NAME'] = 'TRADE_DT'
        dic[i]['S_INFO_WINDCODE'] = ''
        if i == 'dbo.AINDEXEODPRICES':
            dic[i]['S_INFO_WINDCODE'] = ','.join(index)
    return dic

factors = []
def set_oracle_config():
    data = pd.read_excel(r'datasync/config/name_map.xlsx')

    dic = {}
    for i in factors:
        dic[i] = {}
        fields = data['windColumnName'][data['windTableName'] == i].values
        dic[i]['fields'] = ','.join(['SYMBOLCODE', 'TDATE','RAWVALUE'])
        dic[i]['db_config'] = oracle_config
        dic[i]['start_date'] = start_date
        dic[i]['origin'] = 'OracleOrigin'
        dic[i]['folder_path'] = path
        dic[i]['DATE_NAME'] = 'TDATE'
        dic[i]['S_INFO_WINDCODE'] = ''
        if i == 'dbo.AINDEXEODPRICES':
            dic[i]['S_INFO_WINDCODE'] = ','.join(index)
    return dic


def set_lb_config():
    dic = {
            'lb.indexWeightRange': {'db_config':remote_jaqs_config,
                                    'view': 'lb.indexWeightRange',
                                    'origin': 'DataServiceOrigin',
                                    'start_date': 20080101,
                                    'folder_path': r'D:/sqlite_data'},
            'jz.instrumentInfo': {'db_config': remote_jaqs_config,
                                  'view': 'jz.instrumentInfo',
                                  'origin': 'DataServiceOrigin',
                                  'folder_path': r'D:/sqlite_data'},
            'ZYYX2.CON_FORECAST_STK' : {'db_config':oracle_config,
                                        'view': 'jz.instrumentInfo',
                                        'origin': 'OracleOrigin',
                                        'folder_path': r'D:/sqlite_data'}
           }
    return dic


def config_to_excel():
    daily_config = set_config()
    lb_config = set_lb_config()
    _path = path + '\\hdf5_docs\\config.xlsx'
    excel_writer = pd.ExcelWriter(_path)

    pd.DataFrame(daily_config).to_excel(excel_writer, sheet_name='daily_data')
    pd.DataFrame(lb_config).to_excel(excel_writer, sheet_name='lb_data')
    excel_writer.save()


def read_config(sheet_name, config_path=None):
    if config_path == None:
        config_path = os.path.abspath(os.path.expanduser('~/Desktop')) + '\\hdf5_docs\\config.xlsx'
    config = pd.read_excel(config_path, sheet_name=sheet_name)
    config = config.fillna('')
    return config.to_dict()
