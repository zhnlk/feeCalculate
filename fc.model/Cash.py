# -*- coding: utf-8 -*-
import os
import uuid
from collections import OrderedDict

import datetime
from sqlalchemy import Column, engine, func
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from BasicWidget import BasicCell
from MoneyFund import MfProjectList
from ProtocolDeposit import ProtocolDeposit
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
    def __init__(self, date, cash_to_investor, extract_fee, investor_to_cash, cash_revenue):
        init_db()
        self.date = date
        self.cash_to_investor = cash_to_investor
        self.investor_to_cash = investor_to_cash
        self.cash_revenue = cash_revenue
        self.extract_fee = extract_fee
        self.uuid = uuid.uuid1().__str__()
        self.total_cash = 0.00
        self.cash_to_assert_mgt = 0.00
        self.cash_to_money_fund = 0.00
        self.cash_to_protocol_deposit = 0.00
        self.assert_mgt_to_cash = 0.00
        self.money_fund_to_cash = 0.00
        self.protocol_deposit_to_cash = 0.00

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
    cash_revenue = Column(Float, default=0.00)
    extract_fee = Column(Float, default=0.00)

    def save(self):
        # session.add(self)
        # self.total_cash = self.getTodayTotalCash(self.date)
        session.merge(self)
        session.flush()
        session.commit()

    @classmethod
    def listAll(self):
        print('SQLALCHEMY_DATABASE_URI:' + SQLALCHEMY_DATABASE_URI)
        return session.query(Cash).all()

    def getTodayTotalCash(self, date):
        # session = Session(bind=engine)
        # today = datetime.date.today()
        # today = datetime.date(2017,3,27)
        today = date
        yesterday = today - datetime.timedelta(days=1)
        # print(today.strftime('%Y-%m-%d'))
        try:
            yesterday_total_cash = session.query(Cash.total_cash).filter(Cash.date == yesterday.strftime('%Y-%m-%d')).one()
        except:
            yesterday_total_cash = (0.00,)
        # today_cash = session.query(Cash).filter(Cash.date == today.strftime('%Y-%m-%d')).one()
        print(self.__dict__)

        # 2017-04-07，增加现金收入与提取费用
        today_total_cash = yesterday_total_cash[0] \
                           - float(self.cash_to_assert_mgt) \
                           - float(self.cash_to_money_fund) \
                           - float(self.cash_to_protocol_deposit) \
                           - float(self.cash_to_investor) \
                           + float(self.assert_mgt_to_cash) \
                           + float(self.money_fund_to_cash) \
                           + float(self.protocol_deposit_to_cash) \
                           + float(self.investor_to_cash) \
                           + float(self.cash_revenue) \
                           - float(self.extract_fee)

        print('today_total_cash:............:' + str(today_total_cash))
        return today_total_cash

    def getRelatedData(self):
        today = self.date
        print(today)
        try:
            pd_sum = session.query(ProtocolDeposit).filter(ProtocolDeposit.date == today).one()
        except NoResultFound:
            pd_sum = None
        if pd_sum is not None:
            # 现金到协存
            self.cash_to_protocol_deposit = pd_sum.cash_to_protocol_deposit
            # 协存到现金
            self.protocol_deposit_to_cash = pd_sum.protocol_deposit_to_cash
        else:
            self.cash_to_protocol_deposit = 0.00
            self.protocol_deposit_to_cash = 0.00
        # 现金到货基
        try:
            cash_to_mf = session.query(func.sum(MfProjectList.mf_subscribe_from_cash)).filter(MfProjectList.date == today).scalar()
        except NoResultFound:
            cash_to_mf = None
        if cash_to_mf is not None:
            self.cash_to_money_fund = cash_to_mf
        else:
            self.cash_to_money_fund = 0.00
        # 货基到现金
        try:
            mf_to_cash = session.query(func.sum(MfProjectList.mf_redeem_to_cash)).filter(MfProjectList.date == today).scalar()
        except NoResultFound:
            mf_to_cash = NoResultFound
        if mf_to_cash is not None:
            self.money_fund_to_cash = mf_to_cash
        else:
            self.money_fund_to_cash = 0.00


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
