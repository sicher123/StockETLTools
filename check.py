import os
import ast
import h5py
import shutil
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from datasync.storage.hdf5 import DailyDB
from datasync.storage.sqlite import SqliteDB
from datasync.props.guojin_props import read_config


def backup(source_dir, target_dir, file_name=None):
    if file_name:
        if isinstance(file_name, str):
            file_name = [file_name]

        file_names = list(set(file_name) & set(os.listdir(source_dir)))

        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)

        for file in file_names:
            source_file = os.path.join(source_dir, file)
            target_file = os.path.join(target_dir, file)
            if os.path.isfile(source_file) and source_file.endswith('hd5'):
                shutil.copy(source_file, target_file)
                print('File %s has been backuped to %s' % (file, target_dir))
    else:
        if os.path.isdir(target_dir):
            shutil.rmtree(target_dir)

        if os.path.isdir(source_dir):
            shutil.copytree(source_dir, target_dir)
            print('Dir %s has been backuped to %s' % (source_dir, target_dir))
        else:
            print('%s error' % (source_dir,))


def check_daily(dir):
    res = {}
    for name in os.listdir(dir):
        if name.endswith('hd5'):
            field = name.split('.')[0]

            try:
                with h5py.File(dir + '//%s' % (name,)) as file:
                    k = file.keys()
            except Exception as e:
                res[field] = 'file error'
                continue

            with h5py.File(dir + '//%s' % (name,)) as file:
                keys = list(file.keys())

                try:
                    assert set(keys) == set(['data', 'symbol_flag', 'date_flag'])
                except Exception as e:
                    res[field] = 'keys error'
                    continue

                try:
                    dates = file['date_flag'][:, -1]
                    symbols = file['symbol_flag'][:, -1]
                    data = file['data'][:]
                except Exception as e:
                    res[field] = 'data error'
                    continue

            dates_copy = dates.copy()
            dates.sort()
            if not (dates == dates_copy).all():
                res[field] = 'date sort error'
    return res


def check_n_rollback(logger=None, config=None, execute=False):
    if not config:
        config = read_config('daily_data')
        config.pop('dbo.AINDEXEODPRICES')

    res = {}
    for k, v in config.items():
        fp = v.get('folder_path')
        origin_dir = os.path.join(fp, k)
        copy_dir = os.path.join(fp + '_copy', k)
        error_dict = check_daily(origin_dir)
        if len(error_dict) == 0:
            res[k] = True
            print(origin_dir, 'no bug')
        else:
            res[k] = False
            if execute:
                for m, n in error_dict.items():
                    backup(copy_dir, origin_dir, file_name=m)
                    logger.info('file %s.hd5 reseted,%s' % (m, n), exc_info=True)
            else:
                print(error_dict)
    return res


def auto_backup(logger, config=None):
    if not config:
        config = read_config('daily_data')
        config.pop('dbo.AINDEXEODPRICES')

    flag = check_n_rollback()
    for k, v in config.items():
        fp = v.get('folder_path')
        origin_dir = os.path.join(fp, k)
        copy_dir = os.path.join(fp+'_copy', k)
        if flag[k]:
            print(k)
            backup(origin_dir, copy_dir, file_name=None)
            logger.info('file has been backuped from %s to %s' % (origin_dir, copy_dir), exc_info=True)
        else:
            print('backup fail')
            logger.info('backup fail,flag:%s' % (flag, ), exc_info=True)

# backup(r'D:\error_data', r'E:\error_data', file_name='S_DQ_MV.hd5')
# check_daily(r'E:\hdf5_data\dbo.ASHAREEODDERIVATIVEINDICATOR')