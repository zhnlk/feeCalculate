# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import create_engine

from Cash import Cash
from DataEngine import DataEngine
from fcFunction import loadSqliteSetting

# dataClient = DataEngine()


# c = Cash()
# dataClient.dbConnect()
# dataClient.session.add(c)
# print(c.date)

uri, logging = loadSqliteSetting()



#定义引擎
engine = create_engine(uri,echo=True)
#绑定元信息
metadata = MetaData(engine)

#创建表格，初始化数据库
user = Table('User', metadata,
    Column('id', Integer, primary_key = True),
    Column('name', String(20)),
    Column('fullname', String(40)))
address = Table('Address', metadata,
    Column('id', Integer, primary_key = True),
    Column('user_id', None, ForeignKey('User.id')),
    Column('email', String(60), nullable = False),
)
#创建数据表，如果数据表存在则忽视！！！
metadata.create_all(engine)
#获取数据库链接，以备后面使用！！！！！
conn = engine.connect()

# user.