import pandas as pd
from datasync.origin import DataOrigin, props_to_sql


class OracleOrigin(object):
    def __init__(self, db_config):
        self.conn = None
        self.db_config = db_config
        self.connect()

    def connect(self):
        import cx_Oracle
        try:
            # _string = 'bigfish/bigfish@0824@172.16.100.175:1521/orcl'
            self.conn = cx_Oracle.connect(self.db_config['user'],
                                       self.db_config['password'],
                                       self.db_config['addr'])
        except:
            raise ValueError('数据库连接失败，请检查配置信息是否正确')

    def read(self,props=None, sql=None):
        if sql is None:
            sql = props_to_sql(props, date_type='datetime')[:-1]
        data = pd.read_sql(sql, self.conn)
        return data


def test_oracle():
    db_config = {'addr': "192.168.0.102:1520/xe",
                 'user': "FXDAYU",
                 'password': "Xinger520"}

    props = {'start_date': 20140801,
             'end_date': 20140906,
             'fields': '',
             'view': 'ZYYX2.CON_FORECAST_STK',
             'DATE_NAME': 'TDATE'}

    origin = OracleOrigin(db_config)
    origin.read(props)
    return origin.read(props=props)