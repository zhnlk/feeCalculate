# -*- coding: utf-8 -*-
import uuid
from datetime import datetime

from sqlalchemy import Column, engine
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper

from DataEngine import DataEngine
from fcFunction import loadSqliteSetting

# dataEngine = DataEngine(eventEngine=)
# dataEngine.dbConnect()
# dataEngine.


uri, logging = loadSqliteSetting()
engine = create_engine(uri, echo=True)
BaseModel = declarative_base()

# engine = create_engine(DB_CONNECT_STRING, echo=True)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


class Cash(BaseModel):
    # 表的名字:
    def __init__(self,date,total_cash):
        self.date=date
        self.total_cash = total_cash
        self.uuid = uuid.uuid1()
    __tablename__ = 'Cash'

    uuid = Column(String(32), primary_key=True)

    date = Column(Date)
    total_cash = Column(Float)
    cash_to_assert_mgt = Column(Float)
    cash_to_money_fund = Column(Float)
    cash_to_protocol_deposit = Column(Float)
    cash_to_investor = Column(Float)
    assert_mgt_to_cash = Column(Float)
    money_fund_to_cash = Column(Float)
    protocol_deposit_to_cash = Column(Float)
    investor_to_cash = Column(Float)

# mapper(Cash,Cash)

if __name__ == '__main__':
    # init_db()
    cash = Cash(date=datetime, total_cash=1000)
    session.add(cash)
    session.commit()

    query = session.query(Cash)
    print(query)