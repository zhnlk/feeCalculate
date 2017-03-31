# -*- coding: utf-8 -*-
import os
import uuid
from collections import OrderedDict

import datetime
from sqlalchemy import Column, engine
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from BasicWidget import BasicCell
from fcConstant import SQLALCHEMY_DATABASE_URI

BaseModel = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
session = Session(bind=engine)


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


class Cash(BaseModel):
    # 构造器
    def __init__(self, date, cash_to_investor, investor_to_cash):
        init_db()
        self.date = date
        self.cash_to_investor = cash_to_investor
        self.investor_to_cash = investor_to_cash
        self.uuid = uuid.uuid1().__str__()

    # 表的名字:
    __tablename__ = 'cash_table'

    uuid = Column(String(32), primary_key=True)

    date = Column(Date)
    total_cash = Column(Float, default=0.00)
    cash_to_assert_mgt = Column(Float, default=0.00)
    cash_to_money_fund = Column(Float, default=0.00)
    cash_to_protocol_deposit = Column(Float, default=0.00)
    cash_to_investor = Column(Float, default=0.00)
    assert_mgt_to_cash = Column(Float, default=0.00)
    money_fund_to_cash = Column(Float, default=0.00)
    protocol_deposit_to_cash = Column(Float, default=0.00)
    investor_to_cash = Column(Float, default=0.00)

    def save(self):
        session.add(self)
        session.flush()
        session.commit()

    @classmethod
    def listAll(self):
        print('SQLALCHEMY_DATABASE_URI:'+SQLALCHEMY_DATABASE_URI)
        return session.query(Cash).all()

    def getTodayTotalCash(self):

        session = Session(bind=engine)
        # today = datetime.date.today()
        today = datetime.date(2017,3,27)
        yesterday = today - datetime.timedelta(days=1)
        print(today.strftime('%Y-%m-%d'))
        yesterday_total_cash = session.query(Cash.total_cash).filter(Cash.date == yesterday.strftime('%Y-%m-%d')).first()
        today_cash = session.query(Cash).filter(Cash.date == today.strftime('%Y-%m-%d')).first()

        today_total_cash = yesterday_total_cash[0] - today_cash.cash_to_assert_mgt - today_cash.cash_to_money_fund - today_cash.cash_to_protocol_deposit - today_cash.cash_to_investor \
                           + today_cash.assert_mgt_to_cash + today_cash.money_fund_to_cash + today_cash.protocol_deposit_to_cash + today_cash.investor_to_cash
        print('today_total_cash:............:' + str(today_total_cash))
        return today_total_cash


if __name__ == '__main__':
    # TEST
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
    #
    # row = 0
    # for r in result:
    #     print(r.uuid)
    #     # for key in l2:
    #     #     contract = d[key]
    #     #     按照定义的表头，进行填充数据
    #
    #     for n, header in enumerate(d):
    #
    #         content = r.__getattribute__(header)
    #         cellType = d[header]['cellType']
    #         cell = cellType(content)
    #         print(header + ':' + cell.text())
    #
    #         # self.setItem(row, n, cell)
    #     row = row + 1

    # INSERT
    # d = datetime.today()
    # print(d.minute(1).__str__())

    # QUERY
    # session = Session(bind=engine)
    # Cash.getTodayTotalCash()
    # yesterday_total_cash = session.query(Cash.total_cash).filter(Cash.date == '2017-03-26').one()
    # today = session.query(Cash).filter(Cash.date == '2017-03-27').first()
    #
    # today_total_cash = yesterday_total_cash[0] - today.cash_to_assert_mgt - today.cash_to_money_fund - today.cash_to_protocol_deposit - today.cash_to_investor \
    #                    + today.assert_mgt_to_cash + today.money_fund_to_cash + today.protocol_deposit_to_cash + today.investor_to_cash
    # print('today_total_cash:............:' + str(today_total_cash))
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
    #
