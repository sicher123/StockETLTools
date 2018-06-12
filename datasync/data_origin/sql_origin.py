import pandas as pd
from datasync.data_origin import DataOrigin,props_to_sql

class MSSqlOrigin(DataOrigin):
    def __init__(self,db_config):
        super(MSSqlOrigin, self).__init__(db_config)
        self.conn = None
        self.connect()

    def connect(self):
        import pymssql as sqldb
        db_config = self.db_config
        try:
            self.conn = sqldb.connect(db_config['addr'],db_config['user'],db_config['password'])
        except:
            raise ValueError('数据库连接失败，请检查配置信息是否正确')

    def read(self,props=None,sql=None):
        if sql is None:
            sql = props_to_sql(props)
        data = pd.read_sql(sql, self.conn)
        return data

    def read_id(self,view):
        return self.read('select OBJECT_ID from %s;'%(view))

    def get_fields(self,view):
        c = self.conn.cursor()
        c.execute('''Select Name FROM SysColumns Where id=Object_Id('%s')''' % (view))
        cols = [i[0] for i in c.fetchall()]
        return cols

class OracleOrigin(DataOrigin):
    def __init__(self,props):
        super(OracleOrigin, self).__init__(props)
        self.conn = None
        self.connect()

    def connect(self):
        import cx_Oracle as oracle
        props = self.props
        try:
            self.conn = oracle.connect('bigfish/bigfish@172.16.55.54:1521/ORCL2')
        except:
            raise ValueError('数据库连接失败，请检查配置信息是否正确')

    def read(self):
        props = self.props
        sql = props.get('sql')
        if sql is None:
            print (props)
            sql = props_to_sql(props)
        data = pd.read_sql(sql, self.conn)
        return data

def test():
    db_config = {'addr':"172.16.100.7",
                 'user':"bigfish01",
                 'password':"bigfish01@0514"}

    props =  {'_filter':'start_date=20170101&end_date=20180101&S_INFO_WINDCODE=000001.SZ',
             'fields':'',
             'view':'ASHAREEODPRICES',
             'DATE_NAME':'TRADE_DT'}
    origin = MSSqlOrigin(db_config)
    return origin.read(props=props)
