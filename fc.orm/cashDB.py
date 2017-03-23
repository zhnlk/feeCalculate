# -*- coding: utf-8 -*-
import os
import uuid

import datetime

import sqlite3
from sqlalchemy import Column, String, create_engine
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 初始化数据库连接:/Users/eranchang/PycharmProjects/feeCalculate/fc.misc/cashdb.db
import fcFunction
from fcConstant import DB_FILENAME

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir,DB_FILENAME))

SQLALCHEMY_DATABASE_URI ,logging = fcFunction.loadSqliteSetting()

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

# print(__file__)
# print(basedir)
# print(SQLALCHEMY_DATABASE_URI)

# 创建对象的基类:
Base = declarative_base()
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# # 建表
# metadata = MetaData()
# metadata.create_all(engine)
#
# user = Table('users', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name', String(50)),
#     Column('fullname', String(50)),
#     Column('password', String(100))
# )

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'User'

    # 表的结构:
    uuid = Column(String(32), primary_key=True)
    date = Column(Date)
    total_cash = Column(Float, )
    cash_to_assert_mgt = Column(Float)
    cash_to_money_fund = Column(Float)
    cash_to_protocol_deposit = Column(Float)
    cash_to_investor = Column(Float)
    assert_mgt_to_cash = Column(Float)
    money_fund_to_cash = Column(Float)
    protocol_deposit_to_cash = Column(Float)
    investor_to_cash = Column(Float)

    Base.metadata.create_all(engine)

    def __repr__(self):
        return "<User(uuid='%s', date='%s')>" % (self.uuid, self.date)


def insertDB():
    # Base.metadata.create_all(engine)

    # 创建session对象:
    session = DBSession()
    # 创建新User对象:
    new_user = User(uuid=str(uuid.uuid1()), date=datetime.date(2017, 3, 18))
    # 添加到session:
    session.add(new_user)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()


def queryDB():
    # 创建Session:
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    user = session.query(User).filter().all()
    # 打印类型和对象的name属性:
    print('type:', type(user))
    for u in user:
        print('uuid:', u.uuid)
    # 关闭Session:
    session.close()


def tPath():
    print(SQLALCHEMY_DATABASE_URI)
    print(os.path.join(os.path.dirname(__file__), os.pardir,DB_FILENAME))
    print(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir,DB_FILENAME)))
    print(os.path.dirname(__file__))
    print(os.path.abspath(os.path.dirname(__file__)))
    print(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    print(os.path.join(os.path.abspath(os.path.dirname(__file__)),os.pardir,DB_FILENAME))

if __name__ == '__main__':
    # insertDB()
    # queryDB()
    tPath()
