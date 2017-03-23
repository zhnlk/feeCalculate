# -*- coding: utf-8 -*-
import uuid
from datetime import datetime, date

from sqlalchemy import Column, engine
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper

from DataEngine import DataEngine
from EventEngine import EventEngine
from fcFunction import loadSqliteSetting

# dataEngine = DataEngine(eventEngine=)
# dataEngine.dbConnect()
# dataEngine.


BaseModel = declarative_base()

# engine = create_engine(DB_CONNECT_STRING, echo=True)
SQLALCHEMY_DATABASE_URI, logging = loadSqliteSetting()
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


class Cash(BaseModel):

    # 构造器
    def __init__(self, date, cash_to_investor, investor_to_cash):
        self.date = date
        self.cash_to_investor = cash_to_investor
        self.investor_to_cash = investor_to_cash
        self.uuid = uuid.uuid1().__str__()

    # 表的名字:
    __tablename__ = 'cash_table'

    uuid = Column(String(32), primary_key=True)

    date = Column(Date)
    total_cash = Column(Float,nullable=True)
    cash_to_assert_mgt = Column(Float,nullable=True)
    cash_to_money_fund = Column(Float,nullable=True)
    cash_to_protocol_deposit = Column(Float,nullable=True)
    cash_to_investor = Column(Float,nullable=True)
    assert_mgt_to_cash = Column(Float,nullable=True)
    money_fund_to_cash = Column(Float,nullable=True)
    protocol_deposit_to_cash = Column(Float,nullable=True)
    investor_to_cash = Column(Float,nullable=True)


if __name__ == '__main__':
    init_db()
    cash = Cash(date=date(2017,3,22), cash_to_investor=12.00,investor_to_cash=16.00)
    eventEngine = EventEngine()
    dataEngine = DataEngine(eventEngine)
    # init_db(dataEngine.)
    dataEngine.dbConnect()
    dataEngine.dbInsert(cash)


