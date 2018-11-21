import pandas as pd
import numpy as np
import h5py
import os
import json


class LocalFileSystem(object):
    def __init__(self, fp):
        self.fp = fp
        if not os.path.exists(fp):
            os.mkdir(fp)
            with h5py.File(fp + '//sysInfo.h5') as file:
                file.attrs['user'] = 'xinger'
                file.attrs['password'] = 'Xinger520'

    def get_db(self, dbname):
        path = self.fp + '//' + dbname
        if not os.path.exists(path):
            os.mkdir(path)
#            with h5py.File(path + '//dbInfo.h5') as file:
#                file.attrs['last_updated_time'] = str(datetime.now())
        return path


class Store(object):
    def __init__(self, db_path, view):
        file_path = os.path.join(db_path, '%s.pdhd5' % (view,))
        if not os.path.exists(db_path):
            os.mkdir(db_path)

        if os.path.exists(file_path):
            store = pd.HDFStore(file_path, mode='a')
        else:
            store = pd.HDFStore(file_path, complevel=9, mode='w')
        self.store = store

    def check(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @property
    def group_names(self):
        return [i[1:] for i in self.store.keys()]

    @staticmethod
    def filter_parser(_filter):
        filter_dict = {}
        filter_dict['condi'] = []
        filter_list = _filter.split('&')

        if filter_list == ['']:
            filter_dict = None
        else:
            for i in filter_list:
                if '=' in i and '==' not in i and '>' not in i and '<' not in i:
                    k, v = i.split('=')
                    if ',' in v:
                        v = v.split(',')
                    filter_dict[k] = v
                else:
                    filter_dict['condi'].append(i)
        return filter_dict

    def trans_filter(self, _filter=None, fields=None, date_field='trade_date'):
        if isinstance(fields, str):
            fields = fields.split(',')
        filter_dict = self.filter_parser(_filter)
        condition_list = filter_dict.pop('condi')

        if fields != ['']:
            flt = '''columns=%s & ''' % (str(fields))
        else:
            flt = ''''''
        if filter_dict.get('start_date'):
            flt += '%s >= %s & ' % (date_field, filter_dict.pop('start_date'))
        if filter_dict.get('end_date'):
            flt += '%s <= %s & ' % (date_field, filter_dict.pop('end_date'))

        for k, v in filter_dict.items():
            flt += '%s=%s & ' % (k, v)
        for i in condition_list:
            flt += '%s & ' % (i, )
        return flt[:-3]

    def set_attr(self, key, value):
        self.store.root.data.table.attrs[key] = value

    def get_update_info(self):
        indexes = self.store.root.data.table.attrs['indexes']
        symbol_field = indexes.get('symbol', None)
        date_field = indexes.get('date', None)
        if not symbol_field and not date_field:
            raise AttributeError('indexes not set')
        all_dates = self.query('%s="000001.SZ"' % (symbol_field,), fields=date_field)
        max_date = all_dates.max()[date_field]

        if max_date.__class__.__name__ in ['Timestamp', 'datetime']:
            max_date = int(max_date.strftime('%Y%m%d'))
        if type(max_date) != 'int':
            max_date = int(max_date)
        return max_date

    def replace_update(self, view, df):
        if not df or len(df) == 0:
            raise ValueError('no new data to update')

        single = view in self.store.keys()
        multi_views = [i for i in self.store.keys() if view in i]
        multi = len(multi_views) > 0

        if single:
            self.append(df)
        elif multi:
            exist = self.store.query('dynamic')
            data = pd.concat([exist, df])
        else:
            self.append(view, df)

    def _query(self, group, _filter, fields=None, filter_type='pandas'):
        if filter_type == 'jaqs':
            flt = self.trans_filter(_filter, fields)
        elif filter_type == 'pandas':
            flt = _filter
        return self.store.select(group, where=flt)

    def query(self, _filter, fields=None, filter_type='pandas'):
        if 'data' not in self.group_names:
            data = pd.concat([self._query(group, _filter, fields) for group in self.group_names])
        else:
            data = self._query('data', _filter, fields, filter_type=filter_type)
        return data

    def append(self, group, df):
        try:
            self.store.append(group, df, data_columns=True)
        except Exception as e:
            print('append Error', e)

    def close(self):
        self.store.close()


class PdHdf5DB(object):
    def __init__(self, db_path):
        self.path = db_path
        if not os.path.exists(db_path):
            os.mkdir(db_path)

    def __setitem__(self, view, data):
        self.append(view, data)

    def __getitem__(self, view):
        return Store(self.path, view)

    @property
    def views(self):
        return [i.split('.')[0] for i in os.listdir(self.path) if i.endswith('pdhd5')]

    def query(self, view, _filter, fields):
        with Store(self.path, view) as store:
            data = store.query(_filter, fields, filter_type='jaqs')
            return data

    def append(self, view, df, indexes=None):
        with Store(self.path, view) as store:
            store.append('data', df)
            if indexes:
                store.set_attr('indexes', indexes)
                print('set indexes in view {}'.format(view))

    def get_update_info(self, view=None):
        if not view:
            res = {}
            for view in self.views:
                with Store(self.path, view) as store:
                    info = store.get_update_info()
                    res[view] = info
        else:
            with Store(self.path, view) as store:
                res = store.get_update_info()
        return res

    def curtail(self):
        pass

    def delete(self):
        pass


class DailyDB(LocalFileSystem):
    def __init__(self, fp, dbname):
        super(DailyDB, self).__init__(fp)
        self.path = self.get_db(dbname)

    def get_attr(self, field):
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

        elif file_name == 'all':
            dic = {}
            for file_name in os.listdir(self.path):
                with h5py.File(self.path + '//%s' % (file_name,)) as file:
                    try:
                        view = file_name.split('.')[0]
                        dic[view] = int(file['date_flag'][-1][0])
                    except:
                        pass
            return dic

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
            with h5py.File(file_name, 'r+') as file:
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
    from datasync.data_origin.sql_origin import test
    df = test()

    for i in df.columns:
        try:
            data = df.pivot(index='TRADE_DT', columns='S_INFO_WINDCODE', values=i)
            db.update_a_file(data, i)
        except Exception as e:
            print(i, 'failed', e)
'''