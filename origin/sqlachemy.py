from sqlalchemy import create_engine

config = {'db': db,
          'user': user,
          }


engine = create_engine('%s://%s:%s@%s/%s?charset=utf8' % (db, user, passwd, ip, dbname,))

#存入数据库
df.to_sql('tick_data', engine)
