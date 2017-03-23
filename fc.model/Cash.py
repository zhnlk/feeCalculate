# -*- coding: utf-8 -*-
import uuid
from collections import OrderedDict
from datetime import datetime, date

from sqlalchemy import Column, engine
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper

from BasicWidget import BasicCell
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
    total_cash = Column(Float, nullable=True)
    cash_to_assert_mgt = Column(Float, nullable=True)
    cash_to_money_fund = Column(Float, nullable=True)
    cash_to_protocol_deposit = Column(Float, nullable=True)
    cash_to_investor = Column(Float, nullable=True)
    assert_mgt_to_cash = Column(Float, nullable=True)
    money_fund_to_cash = Column(Float, nullable=True)
    protocol_deposit_to_cash = Column(Float, nullable=True)
    investor_to_cash = Column(Float, nullable=True)

    def getDispAttr(self):
        var = self.__dict__
        varr = self.values
        print(varr)

        # d = {'.'.join([contract.exchange, contract.symbol]): contract for contract in l}


if __name__ == '__main__':
    # init_db()
    d = OrderedDict()
    d['date'] = {'chinese': '计算日', 'cellType': BasicCell}
    d['total_cash'] = {'chinese': '现金总额', 'cellType': BasicCell}
    d['cash_to_assert_mgt'] = {'chinese': '现金->资管', 'cellType': BasicCell}
    d['cash_to_money_fund'] = {'chinese': '现金->货基', 'cellType': BasicCell}
    d['cash_to_protocol_deposit'] = {'chinese': '现金->协存', 'cellType': BasicCell}
    d['cash_to_investor'] = {'chinese': '现金->兑付投资人', 'cellType': BasicCell}
    d['assert_mgt_to_cash'] = {'chinese': '资管->现金', 'cellType': BasicCell}
    d['money_fund_to_cash'] = {'chinese': '货基->现金', 'cellType': BasicCell}
    d['protocol_deposit_to_cash'] = {'chinese': '协存->现金', 'cellType': BasicCell}
    d['investor_to_cash'] = {'chinese': '投资人->现金', 'cellType': BasicCell}

    eventEngine = EventEngine()
    dataEngine = DataEngine(eventEngine)
    # init_db(dataEngine.)
    dataEngine.dbConnect()
    # dataEngine.dbInsert(cash)

    result = dataEngine.dbQuery(Cash)

    row = 0
    for r in result:
        print(r.uuid)
        # for key in l2:
        #     contract = d[key]
        #     按照定义的表头，进行填充数据

        for n, header in enumerate(d):
            # content = r.date
            # cellType = self.headerDict[header]['cellType']
            # cell = cellType(content)
            # self.setItem(row, n, cell)

            content = r.__getattribute__(header)
            print(content)
            cellType = d[header]['cellType']
            cell = cellType(content)

            # self.setItem(row, n, cell)

        row = row + 1

    # d = datetime.today()
    # cash = Cash(date=date(d.year, d.month, d.day), cash_to_investor=22.00, investor_to_cash=16.00)

    # for r in result:
    #     print(r.date)
    #     print(r.total_cash)
    #     print(r.cash_to_assert_mgt)
    #     print(r.cash_to_money_fund)
    #     print(r.cash_to_protocol_deposit)
    #     print(r.cash_to_investor)
    #     print(r.assert_mgt_to_cash)
    #     print(r.money_fund_to_cash)
    #     print(r.protocol_deposit_to_cash)
    #     print(r.investor_to_cash)
    #     print()

