# -*- coding: utf-8 -*-
import datetime
import uuid

from sqlalchemy import Column, engine
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, backref
from sqlalchemy.orm import relationship

from fcConstant import SQLALCHEMY_DATABASE_URI

BaseModel = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
session = Session(bind=engine)

def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


class MoneyFund(BaseModel):
    # 构造器
    def __init__(self, date):
        init_db()
        self.uuid = uuid.uuid1().__str__()
        self.date = date

    # 表的名字:
    __tablename__ = 'mf_table'

    uuid = Column(String(32), primary_key=True)

    date = Column(Date)
    money_fund_amount = Column(Float, nullable=True)
    money_fund_revenue = Column(Float, nullable=True)

    def update(self):
        try:
            moneyFund = session.query(MoneyFund).filter(MoneyFund.date == self.date).one()
            mfProjectList = session.query(MfProjectList).filter(MfProjectList.date == self.date).all()

            for p in mfProjectList:
                moneyFund.money_fund_amount += p.pd_amount
                moneyFund.protocol_deposit_revenue += p.pd_interest
                moneyFund.cash_to_protocol_deposit += p.pd_cash_to_pd
                moneyFund.protocol_deposit_to_cash += p.pd_pd_to_cash

            session.flush()
            session.commit()
        except:
            pass



class MfProject(BaseModel):
    def __init__(self, mf_project_name):
        init_db()
        self.uuid = uuid.uuid1().__str__()
        self.mf_project_name = mf_project_name

    __tablename__ = 'mf_pro_table'

    uuid = Column(String(32), primary_key=True)
    mf_project_name = Column(String)

    def save(self):
        session.add(self)
        session.flush()
        session.commit()
        return self

    @classmethod
    def listAll(self):
        return session.query(MfProject).all()


class MfProjectList(BaseModel):
    """每日的记录"""

    def __init__(self, date, mf_subscribe_normal, mf_subscribe_from_assert_mgt, mf_subscribe_from_cash,
                 mf_redeem_normal, mf_redeem_to_assert_mgt, mf_redeem_to_cash,
                 mf_carry_forward_amount, mf_not_carry_forward_amount, mf_redeem_fee):
        init_db()
        self.uuid = uuid.uuid1().__str__()

        self.date = date
        self.mf_subscribe_normal = mf_subscribe_normal
        self.mf_subscribe_from_assert_mgt = mf_subscribe_from_assert_mgt
        self.mf_subscribe_from_cash = mf_subscribe_from_cash
        self.mf_redeem_normal = mf_redeem_normal
        self.mf_redeem_to_assert_mgt = mf_redeem_to_assert_mgt
        self.mf_redeem_to_cash = mf_redeem_to_cash
        self.mf_carry_forward_amount = mf_carry_forward_amount
        self.mf_not_carry_forward_amount = mf_not_carry_forward_amount
        self.mf_redeem_fee = mf_redeem_fee

    __tablename__ = 'mf_pro_list_table'

    uuid = Column(String(32), primary_key=True)

    """每日的记录"""
    date = Column(Date)
    mf_amount = Column(Float, nullable=True)
    mf_revenue = Column(Float, nullable=True)
    mf_subscribe_amount = Column(Float, nullable=True)

    mf_redeem_amount = Column(Float, nullable=True)
    mf_subscribe_normal = Column(Float, nullable=True)
    mf_subscribe_from_assert_mgt = Column(Float, nullable=True)
    mf_subscribe_from_cash = Column(Float, nullable=True)
    mf_redeem_normal = Column(Float, nullable=True)
    mf_redeem_to_assert_mgt = Column(Float, nullable=True)
    mf_redeem_to_cash = Column(Float, nullable=True)
    mf_carry_forward_amount = Column(Float, nullable=True)
    mf_not_carry_forward_amount = Column(Float, nullable=True)
    mf_redeem_fee = Column(Float, nullable=True)

    mf_obj_uuid = Column(ForeignKey('mf_pro_table.uuid'))
    mf_obj = relationship(MfProject, backref=backref('mf_pro_list_table',
                                                     cascade='all,delete-orphan'))

    @classmethod
    def listAll(self):
        return session.query(MfProjectList).all()


    def save(self, uuid):

        today = self.date

        yesterday = today - datetime.timedelta(days=1)
        print('today is :' + today.strftime('%Y-%m-%d'))

        try:
            # 昨日未结转收益
            yesterday_ncfa = session.query(MfProjectList.mf_not_carry_forward_amount).filter(
                MfProjectList.date == yesterday.strftime('%Y-%m-%d')).one()
            yesterday_mf_amount = session.query(MfProjectList.mf_amount).filter(MfProjectList.date == yesterday.strftime('%Y-%m-%d')).one()
        except:
            session.rollback()
            yesterday_ncfa = (0.00,)
            yesterday_mf_amount = (0.00,)
        finally:
            session.close()

        # rate = session.query(MfProject.pd_project_rate).filter(MfProject.uuid == uuid).one()
        # 收益
        self.mf_revenue = float(self.mf_not_carry_forward_amount) \
                          - float(yesterday_ncfa[0]) \
                          + float(self.mf_carry_forward_amount)
        # 申购总额
        self.mf_subscribe_amount = float(self.mf_subscribe_normal) \
                                   + float(self.mf_subscribe_from_assert_mgt) \
                                   + float(self.mf_subscribe_from_cash)
        # 赎回总额
        self.mf_redeem_amount = float(self.mf_redeem_normal) \
                                + float(self.mf_redeem_to_assert_mgt) \
                                + float(self.mf_redeem_to_cash) \
                                + float(self.mf_redeem_fee)
        # 金额
        self.mf_amount = float(yesterday_mf_amount[0]) \
                         + float(self.mf_revenue) \
                         + float(self.mf_subscribe_amount) \
                         - float(self.mf_redeem_amount)

        session.add(self)
        session.flush()
        session.commit()
        return self


if __name__ == '__main__':


    # INSERT
    mf_project_name = '广发基金'
    mfProject = MfProject(mf_project_name)
    print(mfProject.save())

    # QUERY

    # DELETE
    # 731055ac-123e-11e7-8cdf-a45e60d89519
    # uud = '731055ac-123e-11e7-8cdf-a45e60d89519'
    # for i in session.query(MfProject).filter(MfProject.uuid == uud).all():
    #     session.delete(i)
    # session.flush()
    # session.commit()
