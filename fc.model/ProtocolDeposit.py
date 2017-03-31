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
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship, backref

from fcFunction import loadSqliteSetting

BaseModel = declarative_base()

SQLALCHEMY_DATABASE_URI, logging = loadSqliteSetting()
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
session = Session(bind=engine)


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


class ProtocolDeposit(BaseModel):
    # 构造器
    def __init__(self, date):
        init_db()
        self.uuid = uuid.uuid1().__str__()
        self.date = date
        session.commit()

    # 表的名字:
    __tablename__ = 'pd_table'

    uuid = Column(String(32), primary_key=True)

    date = Column(Date)
    protocol_deposit_amount = Column(Float, default=0.00)
    protocol_deposit_revenue = Column(Float, default=0.00)
    cash_to_protocol_deposit = Column(Float, default=0.00)
    protocol_deposit_to_cash = Column(Float, default=0.00)

    def save(self):
        """计算某日的协存汇总"""

        session.add(self)
        session.flush()
        session.commit()
        return self

    def update(self):
        protocolDeposit = session.query(ProtocolDeposit).filter(ProtocolDeposit.date == self.date).one()

        protocolDepositList = session.query(PdProjectList).filter(PdProjectList.date == self.date).all()
        for p in protocolDepositList:
            protocolDeposit.protocol_deposit_amount += p.pd_amount
            protocolDeposit.protocol_deposit_revenue += p.pd_interest
            protocolDeposit.cash_to_protocol_deposit += p.pd_cash_to_pd
            protocolDeposit.protocol_deposit_to_cash += p.pd_pd_to_cash

        session.flush()
        session.commit()

class PdProject(BaseModel):
    """构造器"""

    def __init__(self, pd_project_name, pd_project_rate):
        init_db()
        self.uuid = uuid.uuid1().__str__()
        self.pd_project_name = pd_project_name
        self.pd_project_rate = pd_project_rate

    __tablename__ = 'pd_pro_table'

    uuid = Column(String(32), primary_key=True)
    """协存项目"""
    pd_project_name = Column(String)
    pd_project_rate = Column(Float)

    @classmethod
    def findByUUID(self, uuid):
        pdp = session.query(PdProject).filter(PdProject.uuid == uuid).one()
        return pdp

    @classmethod
    def listAll(self):
        return session.query(PdProject).all()

    def update(self):
        session.commit()
        return self

    def save(self):
        session.add(self)
        session.commit()
        return self


class PdProjectList(BaseModel):
    """构造器"""

    def __init__(self, date, interest_to_principal, investor_to_pd, cash_to_pd, pd_to_investor, pd_to_cash):
        init_db()
        self.date = date
        self.uuid = uuid.uuid1().__str__()
        self.pd_interest_to_principal = interest_to_principal
        self.pd_investor_to_pd = investor_to_pd
        self.pd_cash_to_pd = cash_to_pd
        self.pd_pd_to_investor = pd_to_investor
        self.pd_pd_to_cash = pd_to_cash
        print('set_params success')

    __tablename__ = 'pd_pro_list_table'

    uuid = Column(String(32), primary_key=True)

    """每日的记录"""
    date = Column(Date)
    pd_amount = Column(Float, default=0.00)
    pd_principal = Column(Float, default=0.00)
    pd_interest = Column(Float, default=0.00)
    pd_interest_to_principal = Column(Float, default=0.00)
    pd_investor_to_pd = Column(Float, default=0.00)
    pd_cash_to_pd = Column(Float, default=0.00)
    pd_pd_to_investor = Column(Float, default=0.00)
    pd_pd_to_cash = Column(Float, default=0.00)
    pd_obj_uuid = Column(ForeignKey('pd_pro_table.uuid'))
    pd_obj = relationship(PdProject, backref=backref('pd_pro_list_table',
                                                     cascade='all,delete-orphan'))

    @classmethod
    def listAll(self):
        return session.query(PdProjectList).all()

    def save(self, uuid):
        today = self.date

        yesterday = today - datetime.timedelta(days=1)
        print('today is :' + today.strftime('%Y-%m-%d'))

        try:
            yesterday_pd_amount = session.query(PdProjectList.pd_amount).filter(PdProjectList.date == yesterday.strftime('%Y-%m-%d')).one()
            # session.commit()
            yesterday_pd_principal = session.query(PdProjectList.pd_principal).filter(PdProjectList.date == yesterday.strftime('%Y-%m-%d')).one()
            # session.commit()
        except:
            # print('++++++++++'+e)
            session.rollback()
            yesterday_pd_amount = (0.00,)
            yesterday_pd_principal = (0.00,)
        finally:
            session.close()

        rate = session.query(PdProject.pd_project_rate).filter(PdProject.uuid == uuid).one()

        self.pd_principal = float(yesterday_pd_principal[0]) \
                            + float(self.pd_cash_to_pd) \
                            + float(self.pd_investor_to_pd) \
                            - float(self.pd_pd_to_cash) \
                            - float(self.pd_pd_to_investor) \
                            + float(self.pd_interest_to_principal)
        self.pd_interest = float(self.pd_principal) \
                           * float(rate[0]) \
                           / 360
        self.pd_amount = float(yesterday_pd_amount[0]) \
                         + float(self.pd_cash_to_pd) \
                         + float(self.pd_investor_to_pd) \
                         - float(self.pd_pd_to_cash) \
                         - float(self.pd_pd_to_investor) \
                         + float(self.pd_interest)

        session.add(self)
        session.flush()
        session.commit()
        return self


# 显示声明外键
# 1
# PdProject.pd_obj = relationship('ProtocolDeposit')
# ProtocolDeposit.pd_list = relationship('PdProject')
# 2
# 增加级联关系
# PdProject.artist = relationship(ProtocolDeposit, backref=backref('pd_pro_table', cascade='all'))

if __name__ == '__main__':
    d = datetime.date.today()
    protocolDeposit = ProtocolDeposit(datetime.date(d.year, d.month, d.day-1))
    # print(protocolDeposit)
    # protocolDeposit.save()
    protocolDeposit.update(datetime.date(d.year, d.month, d.day-1))

    # INSERT
    # pd = ProtocolDeposit()
    # pd_project_name = '习惯性晚睡银行协存'
    # pd_project_rate = 0.03
    # pdProject = PdProject(pd_project_name, pd_project_rate)

    # QUERY
    #     print(i.uuid)
    #     print(i.pd_project_name)
    #     print(i.pd_project_rate)

    # DELETE
    # 196c21d0-1215-11e7-9dea-a45e60d89519
    # uud = '196c21d0-1215-11e7-9dea-a45e60d89519'
    # for i in session.query(PdProject).filter(PdProject.uuid == uud).all():
    #     session.delete(i)
    # session.flush()
    # session.commit()
