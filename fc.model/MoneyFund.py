# -*- coding: utf-8 -*-
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

from DataEngine import DataEngine
from EventEngine import EventEngine
from fcFunction import loadSqliteSetting

BaseModel = declarative_base()

SQLALCHEMY_DATABASE_URI, logging = loadSqliteSetting()
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


class MoneyFund(BaseModel):
    # 构造器
    def __init__(self, date):
        self.uuid = uuid.uuid1().__str__()
        self.date = date

    # 表的名字:
    __tablename__ = 'mf_table'

    uuid = Column(String(32), primary_key=True)

    date = Column(Date)
    money_fund_amount = Column(Float, nullable=True)
    money_fund_revenue = Column(Float, nullable=True)


class MfProject(BaseModel):
    def __init__(self, mf_project_name):
        self.uuid = uuid.uuid1().__str__()
        self.mf_project_name = mf_project_name

    def set_params(self, mf_subscribe_normal, mf_subscribe_from_assert_mgt, mf_subscribe_from_cash,
                   mf_redeem_normal, mf_redeem_to_assert_mgt, mf_redeem_to_cash,
                   mf_carry_forward_amount, mf_not_carry_forward_amount, mf_redeem_fee):
        self.mf_subscribe_normal = mf_subscribe_normal
        self.mf_subscribe_from_assert_mgt = mf_subscribe_from_assert_mgt
        self.mf_subscribe_from_cash = mf_subscribe_from_cash
        self.mf_redeem_normal = mf_redeem_normal
        self.mf_redeem_to_assert_mgt = mf_redeem_to_assert_mgt
        self.mf_redeem_to_cash = mf_redeem_to_cash
        self.mf_carry_forward_amount = mf_carry_forward_amount
        self.mf_not_carry_forward_amount = mf_not_carry_forward_amount
        self.mf_redeem_fee = mf_redeem_fee

    __tablename__ = 'mf_pro_table'

    uuid = Column(String(32), primary_key=True)

    mf_project_name = Column(String)

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

    mf_obj_uuid = Column(ForeignKey('mf_table.uuid'))
    mf_obj = relationship(MoneyFund, backref=backref('mf_pro_table',
                                                     cascade='all,delete-orphan'))


if __name__ == '__main__':
    init_db()
    eventEngine = EventEngine()
    dataEngine = DataEngine(eventEngine)
    dataEngine.dbConnect()

    session = Session(bind=engine)

    # INSERT
    mf_project_name = '广发基金'
    mfProject = MfProject(mf_project_name)
    dataEngine.dbInsert(mfProject)

    # QUERY
    # for i in dataEngine.dbQuery(MfProject):
    #     print(i.uuid)
    #     print(i.mf_project_name)

    # DELETE
    # 731055ac-123e-11e7-8cdf-a45e60d89519
    # uud = '731055ac-123e-11e7-8cdf-a45e60d89519'
    # for i in session.query(MfProject).filter(MfProject.uuid == uud).all():
    #     session.delete(i)
    # session.flush()
    # session.commit()
