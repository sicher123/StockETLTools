import os
import pandas as pd


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