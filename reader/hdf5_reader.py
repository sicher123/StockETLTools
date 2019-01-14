import os
import h5py
import numpy as np
import pandas as pd


class DataNotFoundError(Exception):
    pass


class HDF5Base(object):
    def __init__(self, fp, dbname):
        self.fp = fp
        self.path = self.get_db(dbname)

    def get_db(self, dbname):
        path = self.fp + '//' + dbname
        if not os.path.exists(path):
            os.mkdir(path)
        #            with h5py.File(path + '//dbInfo.h5') as file:
        #                file.attrs['last_updated_time'] = str(datetime.now())
        return path

    def get_info(self, field):
        with h5py.File(self.path + '//dbInfo.h5') as file:
            data = file.attrs[field]
            return data

    def get_attr(self, field, name='dbInfo'):
        with h5py.File(self.path + '//%s.h5' % (name, )) as file:
            if field in file.attrs.keys():
                return file.attrs[field]
            else:
                return None

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


class HDF5DailyReader(HDF5Base):
    def __init__(self, fp, dbname):
        super(HDF5DailyReader, self).__init__(fp, dbname)

    def read_single(self, file_name, start_date, end_date, symbol):
        if isinstance(symbol, str):
            symbol = symbol.split(',')

        _dir = os.path.join(self.path, file_name + '.hd5')
        with h5py.File(_dir, 'r') as file:
            # noinspection PyBroadException
            try:
                dset = file['data']
                exist_symbol = file['symbol_flag'][:, 0].astype(str)
                exist_dates = file['date_flag'][:, 0].astype(int)
            except Exception:
                raise DataNotFoundError('empty hdf5 file')

            if start_date not in exist_dates or end_date not in exist_dates:
                raise ValueError('起止日期超限')

            _symbol = [x for x in symbol if x in exist_symbol]
            symbol_index = [np.where(exist_symbol == i)[0][0] for i in _symbol]
            symbol_index.sort()
            sorted_symbol = [exist_symbol[i] for i in symbol_index]

            start_index = np.where(exist_dates == start_date)[0][0]
            end_index = np.where(exist_dates == end_date)[0][0] + 1

            if len(symbol_index) == 0:
                return None

            data = dset[start_index:end_index, symbol_index]
            _index = exist_dates[start_index:end_index]

            if data.dtype not in ['float', 'float32', 'float16', 'int']:
                data = data.astype(str)
            if file_name == 'trade_date' and data.dtype in ['float', 'float32', 'float16']:
                data = data.astype(float).astype(int)
            cols_multi = pd.MultiIndex.from_product([[file_name], sorted_symbol], names=['fields', 'symbol'])
            return pd.DataFrame(columns=cols_multi, index=_index, data=data)

    def read_multi(self, file_names, start_date, end_date, symbol):
        if isinstance(file_names, str):
            file_names = file_names.split(',')
        data = [self.read_single(name, start_date, end_date, symbols) for name in file_names]
        data = pd.concat(data, axis=1)
        data.index.name = 'trade_date'
        data = data.stack(dropna=False).reset_index()
        return data


if __name__ == '__main__':
    reader = HDF5DailyReader(r'C:\Users\xinger\Sync\data', 'Stock_D')
    symbols = '000001.SZ'
    df = reader.read_single('freq', 20180104, 20180810, symbols)
    df = reader.read_multi('trade_date,symbol,adjust_factor,freq', 20180104, 20180810, symbols)
    print(df)
