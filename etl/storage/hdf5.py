import pandas as pd
import numpy as np
import h5py
import os
import json
from etl.storage import StorageBase
from jaqs.data import DataView

class LocalFileSystem(object):
    def __init__(self, fp):
        self.fp = fp
        if not os.path.exists(fp):
            os.mkdir(fp)

    @property
    def table_names(self):
        return [i for i in os.listdir(self.fp) if os.isfile(i)]

    def get_db(self,dbname):
        path = self.fp + '//' + dbname
        if not os.path.exists(path):
            os.mkdir(path)
#            with h5py.File(path + '//dbInfo.h5') as file:
#                file.attrs['last_updated_time'] = str(datetime.now())
        return path


class DailyDB(LocalFileSystem):
    def __init__(self, fp, dbname):
        super(DailyDB, self).__init__(fp)
        self.path = self.get_db(dbname)

    def get_info(self, field):
        with h5py.File(self.path + '//dbInfo.h5') as file:
            data = file.attrs[field]
            return data

    def set_attr(self, name, info):
        with h5py.File(self.path + '//%s.hd5' % (name,)) as file:
            file.attrs['meta'] = json.dumps(info)

    def get_update_info(self, file_name=None):
        lst = []
        if not file_name:
            for file_name in os.listdir(self.path):
                with h5py.File(self.path + '//%s' % (file_name,)) as file:
                    try:
                        lst.append(int(file['date_flag'][-1][0]))
                    except:
                        pass
            return min(lst) if len(lst) > 0 else None
        else:
            with h5py.File(self.path + '//%s.hd5' % (file_name,)) as file:
                return int(file['date_flag'][-1][0])

    def get_file(self, colname):
        return h5py.File(self.path + '//' + colname + '.hd5')

    @staticmethod
    def _convert_string_array(dt, encoding, itemsize=None):
        from pandas._libs import lib
        from pandas.core.dtypes.common import _ensure_object

        if dt.dtype.name == 'object':
            # encode if needed
            if encoding is not None and len(dt):
                dt = pd.Series(dt.ravel()).str.encode(encoding).values.reshape(dt.shape)

            # create the sized dtype
            if itemsize is None:
                itemsize = lib.max_len_string_array(_ensure_object(dt.ravel()))

            dt = np.asarray(dt, dtype="S%d" % itemsize)
            return dt
        else:
            return dt

    def get_flag(self, colname):
        flag = {}
        file = self.get_file(colname)
        for k in file.keys():
            if '_flag' in k:
                flag[k] = file[k][:, 0]
        return flag

    @property
    def exist_fields(self):
        file_names = os.listdir(self.path)
        fields = [i[:-4] for i in file_names]
        return fields

    def _update_flag(self, data, name, h5_obj=None):
        flag = pd.DataFrame(data).values
        flag = self._convert_string_array(flag, None)
        if len(data) == 0:
            return
        if h5_obj is None:
            colname = data.name
            file = self.get_file(colname)
            file.create_dataset(name, data=flag, chunks=True, maxshape=(10000, 1), compression="gzip")
        elif name in h5_obj.keys():
            num = len(flag)
            dset = h5_obj[name]
            new_shape = (dset.shape[0] + num, dset.shape[1])
            dset.resize(new_shape)
            dset[-num:, :] = flag.astype(dset.dtype)
        else:
            h5_obj.create_dataset(name, data=flag, maxshape=(10000, 1), chunks=True)
            return flag

    def _create_a_file(self,data, field):
        if field not in self.exist_fields:
            file = self.get_file(field)
            dt = self._convert_string_array(data.values,None)
            file.create_dataset('data', data=dt, chunks=True, maxshape=(10000, 10000), compression="gzip")

            self._update_flag(data.columns, 'symbol_flag', h5_obj=file)
            self._update_flag(data.index, 'date_flag', h5_obj=file)
            file.close()
            print(field, 'ok!')

    def curtail(self, num=1):
        files = [os.path.join(self.path, i) for i in os.listdir(self.path)]
        for file_name in files:
            with h5py.File(file_name, 'r') as file:
                if 'data' in file.keys() and 'date_flag' in file.keys():
                    dset = file['date_flag']
                    new_shape = (dset.shape[0] - num, dset.shape[1])
                    dset.resize(new_shape)

                    data_dset = file['data']
                    new_shape = (data_dset.shape[0] - num, data_dset.shape[1])
                    data_dset.resize(new_shape)

    def update_a_file(self, data, field, how='append'):
        '''
        :param data: dataframe
        :param field: str
        :param how: append or replace
        :return: None
        '''
        assert how in ['append', 'replace']
        if field not in self.exist_fields:
            self._create_a_file(data, field)
            return

        if how == 'replace':
            os.remove(self.path+'//' + field + '.hd5')
            self._create_a_file(data, field)
            return

        data.index = data.index.values.astype(int)
        new_symbol = list(data.columns.values.astype(str))
        new_date = list(data.index.values.astype(int))

#       with h5py.File(_dir) as file:
        file = self.get_file(field)
        flag = self.get_flag(field)

        exist_symbol = list(flag['symbol_flag'].astype(str))
        exist_date = list(flag['date_flag'].astype(int))

        symbol = list(set(new_symbol) - set(exist_symbol))
        date = list(set(new_date) - set(exist_date))
        symbol.sort()
        date.sort()

        if len(date) == 0 and len(symbol) == 0:
            print ('%s data is the latest' % (field,))
        else:
            date.sort()
            symbol.sort()
            dset = file['data']

            if len(symbol) > 0:
                new_shape = (dset.shape[0], dset.shape[1] + len(symbol))
                dset.resize(new_shape)
                if len(set(exist_date) & set(new_date)) == 0:
                    data.loc[exist_date[-1]] = np.NAN
                dt = self._convert_string_array(data.loc[exist_date, symbol].values, None)
                dset[:, -len(symbol):] = dt

                exist_symbol = exist_symbol+symbol

            if len(date) > 0:
                new_shape = (dset.shape[0] + len(date), dset.shape[1])
                dset.resize(new_shape)
                dt = self._convert_string_array(data.loc[date, exist_symbol].values, None)
                dset[-len(date):, :] = dt

            self._update_flag(symbol, 'symbol_flag', file)
            self._update_flag(date, 'date_flag', file)
            print(field, 'data has been updated,new date %s ,new symbol %s' % (len(date), len(symbol)))

def test_write():
    fp = r'C:\Users\siche\Desktop\data'
    db = DailyDB(fp, 'daily')

'''
    from datasync.origin.sql_origin import test
    df = test()

    for i in df.columns:
        try:
            data = df.pivot(index='TRADE_DT', columns='S_INFO_WINDCODE', values=i)
            db.update_a_file(data, i)
        except Exception as e:
            print(i, 'failed', e)
'''