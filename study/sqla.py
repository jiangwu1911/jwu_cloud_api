from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import mapper

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '',
    'db': 'cloudui',
    'charset': 'utf8'
}

engine = create_engine('mysql://%s:%s@%s/%s?charset=%s'%(db_config['user'],
                                                         db_config['passwd'],
                                                         db_config['host'],
                                                         db_config['db'],
                                                         db_config['charset']), 
                                                         echo=True)

metadata = MetaData()
users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String(50)),
                    Column('fullname', String(50)),
                    Column('password', String(100))
              )
metadata.create_all(engine)



metadata = MetaData(engine)
users_table = Table('users', metadata, autoload=True)


insert =  users_table.insert()
insert.execute(name='leon', fullname='leon liang', password='leon123')



class User(object):pass  

mapper(User, users_table)


ed_user = User()
print 'username:', ed_user.name
print 'fullname:', ed_user.fullname
print 'password:', ed_user.password
print 'id:', str(ed_user.id)
