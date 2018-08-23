import pymongo
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from datasync.utils import trans_symbol
from datasync.data_origin import DataOrigin


class NoImplementError(Exception):
    pass


class MongodbOrigin(DataOrigin):
    def __init__(self, db_config):
        super(MongodbOrigin, self).__init__(db_config)
        self.conn = None
        self.connect(db_config)

    def connect(self, db_config):
        if ':' in db_config:
            host, port = db_config['addr'].split(':')
        else:
            host = db_config['addr']
            port = 27017
        try:
            self.conn = pymongo.MongoClient(host, int(port))
        except:
            raise ValueError('数据库连接失败，请检查配置信息是否正确')

    def get_update_log(self, date=None):
        db = self.conn['log']
        if not date:
            date = datetime.now().date()

        if isinstance(date, int):
            date = datetime.strptime(str(date), '%Y%m%d').date()

        str_date = datetime.strftime(date, '%Y%m%d')

        #lb
        cs1 = db['lb_daily'].find({'trade_date': str_date}, {'_id': 0, 'trade_date': 0})
        log1 = pd.DataFrame(list(cs1))
        if len(log1) == 0:
            log = pd.DataFrame()
        else:
            log = log1
            log.index = [str_date]

        # Stock_D
        cs2 = db['sinta'].find({'date': str(date)},
                               {'_id': 0, 'date': 1, 'symbol': 1, 'D': 1})
        log2 = pd.DataFrame(list(cs2))
        if len(log2) > 0:
            condi = [True for i in log2['D'] if i == 1]
            if True in condi:
                log['Stock_D'] = condi.count(True)

        # dailyIndicator
        cs3 = db['dailyIndicator'].find({'trade_date': str_date}, {'_id': 0, 'trade_date': 0})
        try:
            log3 = list(cs3)[0]
            condi = [True for i in log3.values() if i == 1.0]
            if True in condi:
                log['SecDailyIndicator'] = condi.count(True)
        except:
            pass

        return log

    def get_last_log(self):
        n = 0
        today = datetime.now().date()

        while True:
            log = self.get_update_log(date=today-timedelta(days=n))
            if len(log) >= 1:
                return log
            else:
                n += 1

    def props_to_mongo(self, props):
        start_date = props.get('start_date')
        end_date = props.get('end_date')
        fields = props.get('fields')
        view = props.get('view')
        dbname, clname = view.split('.')

        doc = self.conn[dbname][clname].find_one({})
        exist_fields = list(doc.keys())

        date_names = [i for i in exist_fields if i in ['trade_date', 'datetime', 'ann_date', 'in_date']]
        if len(date_names) == 1:
            date_name = date_names[0]
            proj = {'_id': 0, date_name: 1}

            date_type = type(doc[date_name])
            if date_type == int:
                flt = {date_name: {'$gte': int(start_date), '$lte': int(end_date)}}
            elif date_type == str:
                flt = {date_name: {'$gte': str(start_date), '$lte': str(end_date)}}
            elif 'datetime' in date_type:
                flt = {date_name: {'$gte': datetime.strptime(str(start_date), '%Y%m%d'),
                                   '$lte': datetime.strptime(str(end_date), '%Y%m%d')}}
        else:
            proj = {'_id': 0}
            flt = {}

        proj = {'_id': 0} if fields is None else [proj.update({x: 1}) for x in fields]
        return flt, proj

    @staticmethod
    def identify(string_list):
        string_list = trans_symbol(string_list)
        # 数字
        is_num = [i.isdigit() for i in string_list]
        i_is_num = [i[0].isdigit() for i in string_list]
        # 字母
        is_string = [i.isalpha() for i in string_list if '_' not in i]
        i_is_string = [i[0].isalpha() for i in string_list if '_' not in i]
        # 数字+字母
        is_num_n_string = [(not (i.isalpha() or i.isdigit())) for i in string_list]

        if (len(is_num) - is_num.count(True)) <= 2:
            res = 'symbol'
        elif (len(is_string) - is_string.count(True)) <= 2:
            res = 'fields'
        elif (len(is_num_n_string) - is_num_n_string.count(True)) <= 2:
            res = 'symbol'
        elif (len(i_is_string) - i_is_string.count(True)) <= 2:
            res = 'fields'
        else:
            raise ValueError('cant identify')

        return res

    def read(self, props, is_filter=True):
        view = props.get('view')
        if '.' in view:
            return self.read_table(props, is_filter=is_filter)
        else:
            clnames = self.conn[view].collection_names()
            columns = list(self.conn[view][clnames[0]].find_one({}).keys())
            columns.remove('_id')
            [columns.remove(i) for i in columns if 'date' in i]

            collection_type = self.identify(clnames)
            columns_type = self.identify(columns)
            data = self.read_db(props, collection_type, columns_type)

            if collection_type == 'fields' and columns_type == 'symbol':
                data = data.set_index(['fields', 'trade_date']).stack(0).unstack(0).reset_index()

            data['symbol'] = [trans_symbol(i) for i in data['symbol']]

            if data['trade_date'].dtype.name == 'int':
                pass
            elif data['trade_date'].dtype.name == 'str':
                data['trade_date'] = data['trade_date'].astype('int')
            elif data['trade_date'].dtype.name == 'object':
                data['trade_date'] = data['trade_date'].astype('int')
            else:
                data['trade_date'] = data['trade_date'].apply(lambda x: int(datetime.strftime(x, '%Y%m%d')))

        return data

    def read_table(self, props, is_filter=True):
        dbname, clname = props.get('view').split('.')
        flt, proj = self.props_to_mongo(props)
        if is_filter:
            cs = self.conn[dbname][clname].find(flt, proj)
        else:
            cs = self.conn[dbname][clname].find({}, {'_id': 0})
        data = pd.DataFrame(list(cs))
        return data

    def read_db(self, props, collection_type, columns_type):
        view = props.get('view')

        db = self.conn[view]
        cl_names = db.collection_names()
        colls = props.get(collection_type)
        colls = list(set(cl_names) & set(colls.split(','))) if colls is not None else cl_names

        doc = db[cl_names[0]].find_one({})
        date_name = [i for i in doc.keys() if 'date' in i.lower()][0]

        proj = {'_id': 0, date_name: 1}
        condi = props.get(columns_type)
        [proj.update({x: 1}) for x in condi.split(',')] if condi is not None else proj.pop(date_name)
        if view == 'SecDailyIndicator':
            proj['trade_date_int'] = 0

        start_date = props.get('start_date')
        end_date = props.get('end_date')

        date_type = type(doc[date_name])

        if date_type == int:
            flt = {date_name: {'$gte': int(start_date), '$lte': int(end_date)}}
        elif date_type == str:
            flt = {date_name: {'$gte': str(start_date), '$lte': str(end_date)}}
        elif date_type == object:
            flt = {date_name: {'$gte': str(start_date), '$lte': str(end_date)}}
        elif 'datetime' in str(date_type):
            start_date = str(start_date) + ' 15:00:00'
            end_date = str(end_date) + ' 15:00:00'
            flt = {date_name: {'$gte': datetime.strptime(start_date, '%Y%m%d %H:%M:%S'),
                               '$lte': datetime.strptime(end_date, '%Y%m%d %H:%M:%S')}}

        def func(name):
            cs = db[name].find(flt, proj)
            df = pd.DataFrame(list(cs))
            df[collection_type] = name
            return df

        data = pd.concat([func(name) for name in colls])
        if len(data) == 0:
            raise ValueError('found a empty dataframe')

        data = data.rename({date_name: 'trade_date'}, axis=1)
        data.columns.name = columns_type
        return data


if __name__ == '__main__':
    db_config = {'addr': '192.168.0.104'}
    origin = MongodbOrigin(db_config)

    props = {'view': 'lb.income',
             'start_date': 20170101,
             'end_date': 20180101}
    '''
    props = {'view': 'Stock_D',
             'start_date': 20170101,
             'end_date': 20180101,
             'fields': 'trade_date,symbol,open,high'}
             
    props = {'view': 'fxdayu_factors',
             'start_date': 20170101,
             'end_date': 20180201,
             'fields': 'A010001A'}
    '''
    # data = origin.read_db(props, 'symbol', 'fields')
    data = origin.read(props)
