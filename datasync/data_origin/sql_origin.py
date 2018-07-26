import pandas as pd
import cx_Oracle as oracle
from datasync.data_origin import DataOrigin, props_to_sql


class MSSqlOrigin(DataOrigin):
    def __init__(self, db_config):
        super(MSSqlOrigin, self).__init__(db_config)
        self.conn = None
        self.connect()

    def connect(self):
        import pymssql as sqldb
        db_config = self.db_config
        try:
            self.conn = sqldb.connect(db_config['addr'], db_config['user'], db_config['password'])
        except:
            raise ValueError('数据库连接失败，请检查配置信息是否正确')

    def read(self, props=None, sql=None):
        if sql is None:
            sql = props_to_sql(props)
        data = pd.read_sql(sql, self.conn)
        return data

    def read_multi(self, props):
        if isinstance(props, list):
            data = pd.conat([self.read(props=i) for i in props])
            return data

    def read_id(self, view):
        return self.read('select OBJECT_ID from %s;' % (view,))

    def get_fields(self, view):
        c = self.conn.cursor()
        c.execute('''Select Name FROM SysColumns Where id=Object_Id('%s')''' % (view,))
        cols = [i[0] for i in c.fetchall()]
        return cols


class OracleOrigin(DataOrigin):
    def __init__(self, db_config):
        super(OracleOrigin, self).__init__(db_config)
        self.conn = None
        self.connect()
        self.db_config = db_config

    def connect(self):
        try:
            #_string = 'bigfish/bigfish@172.16.55.54:1521/ORCL'
            _string = '%s/%s@%s' % (self.db_config['user'],
                                    self.db_config['password'],
                                    self.db_config['addr'])

            self.conn = oracle.connect(_string)
        except:
            raise ValueError('数据库连接失败，请检查配置信息是否正确')

    def read(self, props=None, sql=None):
        if sql is None:
            sql = props_to_sql(props, datetype='datetime')[:-1]
        data = pd.read_sql(sql, self.conn)
        return data


def test_mssql():
    db_config = {'addr': "192.168.0.101",
                 'user': "SA",
                 'password': "Xinger520"}

    props = {'start_date': 20140801,
             'end_date': 20140906,
             'fields': '',
             'view': 'dbo.dbo.ASHAREEODDERIVATIVEINDICATOR',
             'DATE_NAME': 'TRADE_DT'}
    origin = MSSqlOrigin(db_config)
    return origin.read(props=props)


def test_oracle():
    db_config = {'addr': "172.16.55.54:1521/ORCL",
                 'user': "bigfish",
                 'password': "bigfish"}

    props = {'start_date': 20140801,
             'end_date': 20140906,
             'fields': '',
             'view': 'ZYYX2.CON_FORECAST_STK',
             'DATE_NAME': 'TDATE'}

    origin = OracleOrigin(db_config)
    origin.read(props)
    return origin.read(props=props)
