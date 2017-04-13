# -*- coding: utf-8 -*-
# @Author:zhnlk
# @Date:  2017/4/10
# @Email: dG9tbGVhZGVyMDgyOEBnbWFpbC5jb20=  
# @Github:github/zhnlk

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
from sqlalchemy.sql.functions import count

from Cash import Cash
from MoneyFund import MoneyFund
from ProtocolDeposit import ProtocolDeposit
from fcConstant import SQLALCHEMY_DATABASE_URI

BaseModel = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
session = Session(bind=engine)


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


class Valuation(BaseModel):
    # 构造器
    def __init__(self, date):
        init_db()
        self.date = date
        self.uuid = uuid.uuid1().__str__()
        self.total_assert_net_value = 0.00
        self.cash = 0.00
        self.protocol_deposit = 0.00
        self.money_fund = 0.00
        self.assert_mgt = 0.00
        self.liquid_assert_ratio = 0.00
        self.today_total_revenue = 0.00
        self.fee_1 = 0.00
        self.fee_2 = 0.00
        self.fee_3 = 0.00
        self.fee_4 = 0.00
        self.today_product_revenue = 0.00
        self.fee_accual = 0.00

    # 表的名字:
    __tablename__ = 'valuation_table'

    uuid = Column(String(32), primary_key=True)

    date = Column(Date)
    total_assert_net_value = Column(Float, default=0.00)
    cash = Column(Float, default=0.00)
    protocol_deposit = Column(Float, default=0.00)
    money_fund = Column(Float, default=0.00)
    assert_mgt = Column(Float, default=0.00)
    liquid_assert_ratio = Column(Float, default=0.00)
    today_total_revenue = Column(Float, default=0.00)
    fee_1 = Column(Float, default=0.00)
    fee_2 = Column(Float, default=0.00)
    fee_3 = Column(Float, default=0.00)
    fee_4 = Column(Float, default=0.00)
    today_product_revenue = Column(Float, default=0.00)
    fee_accual = Column(Float, default=0.00)

    def update(self):
        session.commit()
        return self

    def save(self):
        date = self.date
        v = Valuation.findByDate(date)
        if v:
            return v

        # valuation = Valuation(date)
        # 现金的总额
        cash = Cash.findByDate(date)
        if cash is None:
            self.cash = 0.00
        else:
            self.cash = cash.getTodayTotalCash(date)

        # 协存
        pd = ProtocolDeposit.findByDate(date)
        if pd is None:
            self.protocol_deposit = 0.00
            pd_revenue = 0.00
        else:
            self.protocol_deposit = pd.protocol_deposit_amount
            pd_revenue = pd.protocol_deposit_revenue

        # 货基
        mf = MoneyFund.findByDate(date)
        if mf is None:
            self.money_fund = 0.00
            mf_revenue = 0.00
        else:
            self.money_fund = mf.money_fund_amount
            mf_revenue = mf.money_fund_revenue

            # 资管
            self.assert_mgt = 0.00
        am_revenue = 0.00

        # 总资产净值 = 现金 + 协存 + 货基 + 资管
        self.total_assert_net_value = self.cash \
                                      + self.protocol_deposit \
                                      + self.money_fund \
                                      + self.assert_mgt

        # 流动资产比例 = (现金 + 协存 + 货基)/总资产净值
        if self.total_assert_net_value == 0:
            self.liquid_assert_ratio = (self.cash
                                        + self.protocol_deposit
                                        + self.money_fund)
        else:
            self.liquid_assert_ratio = (self.cash
                                        + self.protocol_deposit
                                        + self.money_fund) \
                                       / self.total_assert_net_value
        # 当日总收益 = 协存当日总收益 + 货基当日总收益 + 资管当日总收益
        self.today_total_revenue = pd_revenue \
                                   + mf_revenue \
                                   + am_revenue

        rate, duration = self.getFeeConstrant()

        self.fee_1 = self.total_assert_net_value * eval(rate[0].replace('%', '/100')) / float(duration[0])
        self.fee_2 = self.total_assert_net_value * eval(rate[1].replace('%', '/100')) / float(duration[1])
        self.fee_3 = self.total_assert_net_value * eval(rate[2].replace('%', '/100')) / float(duration[2])
        self.fee_4 = self.today_total_revenue \
                     - self.today_product_revenue \
                     - self.fee_1 \
                     - self.fee_2 \
                     - self.fee_3

        session.merge(self)
        session.flush()
        session.commit()

    @classmethod
    def listAll(self):
        return session.query(Valuation).all()

    def getFeeConstrant(self):
        rate = ['0.02%', '0.30%', '0.04%']
        duration = ['360', '360', '365']
        return rate, duration

    @classmethod
    def findByDate(self, date):
        try:
            return session.query(Valuation).filter(Valuation.date == date).one()
        except NoResultFound:
            return None


if __name__ == '__main__':
    d = datetime.date.today()

    date = datetime.date(2017,3,10)
    v = Valuation(date)
    v.save()
    # v = Valuation(datetime.date(d.year, 3, 27))
    # v.save()

