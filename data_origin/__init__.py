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
        for i in flt:
            try:
                k, v = i.split('=')
                res[k] = v
            except:
                raise ValueError('%s type error' % (i))
    return res


def props_to_sql(props,date_type = 'int'):
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

    sql = '''SELECT %s FROM %s WHERE 1 = 1 ''' % (fields, view)

    for k, v in props.items():
        if v == '':
            continue

        if k == 'start_date':
            if date_type == 'int':
                sql += '''AND %s >= %s ''' % (DATE_NAME, v)
            elif date_type == 'datetime':
                sql += '''AND %s >= cast('%s' as datetime) ''' % (DATE_NAME, v)

        elif k == 'end_date':
            if date_type == 'int':
                sql += '''AND %s >= %s ''' % (DATE_NAME, v)
            elif date_type == 'datetime':
                sql += '''AND %s >= cast('%s' as datetime) ''' % (DATE_NAME, v)

        elif ',' in v:
            values = tuple(v.split(','))
            sql += '''AND %s in %s ''' % (k, values)

        else:
            sql += '''AND %s='%s' ''' % (k, v)

    sql = sql[:-1] + ';'
    return sql

def sql_to_mongo():
    pass

def props_to_mongo(props):
    flt = {'object_id':0}

class DataOrigin(object):
    def __init__(self,db_config):
        self.db_config = db_config

    def connect(self):
        '''
        初始化连接数据库
        :return:
        '''
        pass

    def read(self,):
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