# -*- coding: utf-8 -*-
import uuid
from collections import OrderedDict
from datetime import datetime, date

from sqlalchemy import Column, engine
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship, backref

from DataEngine import DataEngine
from EventEngine import EventEngine
from fcFunction import loadSqliteSetting

BaseModel = declarative_base()

# engine = create_engine(DB_CONNECT_STRING, echo=True)
SQLALCHEMY_DATABASE_URI, logging = loadSqliteSetting()
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

def init_db():
    BaseModel.metadata.create_all(engine)

def drop_db():
    BaseModel.metadata.drop_all(engine)

class ProtocolDeposit(BaseModel):
    # 构造器
    def __init__(self, date):
        self.uuid = uuid.uuid1().__str__()
        self.date = date

    # 表的名字:
    __tablename__ = 'pd_table'

    uuid = Column(String(32), primary_key=True)

    date = Column(Date)
    protocol_deposit_amount = Column(Float, nullable=True)
    protocol_deposit_revenue = Column(Float, nullable=True)
    cash_to_protocol_deposit = Column(Float, nullable=True)
    protocol_deposit_to_cash = Column(Float, nullable=True)


class PdProject(BaseModel):
    """构造器"""

    def __init__(self, pd_project_name, pd_project_rate):
        self.uuid = uuid.uuid1().__str__()
        self.pd_project_name = pd_project_name
        self.pd_project_rate = pd_project_rate

    @classmethod
    def set_params(self, date, interest_to_principal, investor_to_pd, cash_to_pd, pd_to_investor, pd_to_cash):
        self.date = date
        self.pd_interest_to_pricipal = interest_to_principal
        self.pd_investor_to_pd = investor_to_pd
        self.pd_cash_to_pd = cash_to_pd
        self.pd_pd_to_investor = pd_to_investor
        self.pd_pd_to_cash = pd_to_cash
        print('set_params success')

    __tablename__ = 'pd_pro_table'

    uuid = Column(String(32), primary_key=True)

    pd_project_name = Column(String)
    pd_project_rate = Column(Float)

    pd_amount = Column(Float, nullable=True)
    pd_pricipal = Column(Float, nullable=True)
    pd_interest = Column(Float, nullable=True)
    pd_interest_to_pricipal = Column(Float, nullable=True)
    pd_investor_to_pd = Column(Float, nullable=True)
    pd_cash_to_pd = Column(Float, nullable=True)
    pd_pd_to_investor = Column(Float, nullable=True)
    pd_pd_to_cash = Column(Float, nullable=True)
    pd_obj_uuid = Column(ForeignKey('pd_table.uuid'))
    pd_obj = relationship(ProtocolDeposit, backref=backref('pd_pro_table',
                                           cascade='all,delete-orphan'))

# 显示声明外键
# 1
# PdProject.pd_obj = relationship('ProtocolDeposit')
# ProtocolDeposit.pd_list = relationship('PdProject')
# 2
# 增加级联关系
# PdProject.artist = relationship(ProtocolDeposit, backref=backref('pd_pro_table', cascade='all'))

if __name__ == '__main__':
    init_db()
    eventEngine = EventEngine()
    dataEngine = DataEngine(eventEngine)
    dataEngine.dbConnect()

    session = Session(bind=engine)

    # INSERT
    pd = ProtocolDeposit()
    pd_project_name = '盛京银行协存'
    pd_project_rate = 0.03
    pdProject = PdProject(pd_project_name, pd_project_rate)
    dataEngine.dbInsert(pdProject)

    # QUERY
    # for i in dataEngine.dbQuery(PdProject):
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