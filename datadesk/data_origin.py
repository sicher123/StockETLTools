import pandas as pd

def filter_Parser(filter):
    '''
    parser jaqs origin filter
    str --->>>   dict
    '''
    res = {}
    flt = filter.split('&')

    if flt == ['']:
        res = None
    else:
        for i in flt:o
            try:
                k, v = i.split('=')
                res[k] = v
            except:
                raise ValueError('%s type error' % (i))
    return res


def filter_to_sql(props):
    '''
    parser jaqs origin filter
    str --->>>   dict
    '''
    for k,v in props.items():
       locals()[k] = v
    #assert ('filter' in locals()) and ('fields' in locals()) and ('view' in locals()) ,'查询信息缺失，请检查配置文件'
    #_filter = props.get('_filter')
    fields = props.pop('fields')
    view = props.pop('view')
    DATE_NAME = props.pop('DATE_NAME')

    #res = filter_Parser(_filter)
    if fields == '':
        fields = '*'

    sql = '''SELECT %s FROM %s WHERE OBJECT_ID is not null ''' % (fields, view)

    for k, v in props.items():
        if v == '':
            continue
        if k == 'start_date':
            sql += '''AND %s >= %s ''' % (DATE_NAME, v)
        elif k == 'end_date':
            sql += '''AND %s <= %s ''' % (DATE_NAME, v)
        elif ',' in v:
            values = '("' + '","'.join(v.split(',')) + '")'
            sql += '''AND %s in '%s' ''' % (k, values)
        else:
            sql += '''AND %s='%s' ''' % (k, v)

    sql = sql[:-1] + ';'
    return sql

def sql_to_mongo():
    pass

def props_to_mongo():
    pass

class DataOrigin(object):
    def __init__(self,db_config):
        self.db_config = db_config

    def connect(self):
        '''
        初始化连接数据库
        :return:
        '''
        pass

    def read(self):
        '''
        查询数据
        :return: dataframe
        '''
        pass

    def view(self):
        '''
        查询数据库下一级别对象的结构与内容
        :return:
        '''

class MongodbOrigin(DataOrigin):
    def __init__(self,db_config):
        super(MSSqlOrigin, self).__init__(db_config)
        self.conn = None
        self.connect()
        
    def connect(self):
        import pymongo
        db_config = self.db_config
        try:
            self.conn = pymongo.MongoClient(db_config['host'],db_config['port'])
        except:
            raise ValueError('数据库连接失败，请检查配置信息是否正确')
        
    def read(self,props=None,sql=None):
        from .. import mongoreader

        
        return data

class MSSqlOrigin(DataOrigin):
    def __init__(self,db_config):
        super(MSSqlOrigin, self).__init__(db_config)
        self.conn = None
        self.connect()

    def connect(self):
        import pymssql as sqldb
        db_config = self.db_config
        try:
            self.conn = sqldb.connect(db_config['host'],db_config['user'],db_config['password'])
        except:
            raise ValueError('数据库连接失败，请检查配置信息是否正确')

    def read(self,props=None,sql=None):
        if sql is None:
            sql = filter_to_sql(props)
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
            sql = filter_to_sql(props)
        data = pd.read_sql(sql, self.conn)
        return data

def test():
    db_config = {'host':"172.16.100.7",
                 'user':"bigfish01",
                 'password':"bigfish01@0514"}

    props =  {'_filter':'start_date=20170101&end_date=20180101&S_INFO_WINDCODE=000001.SZ',
             'fields':'',
             'view':'ASHAREEODPRICES',
             'DATE_NAME':'TRADE_DT'}
    origin = MSSqlOrigin(db_config)
    return origin.read(props=props)
