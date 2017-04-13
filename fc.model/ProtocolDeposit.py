# -*- coding: utf-8 -*-
import datetime
import uuid

from sqlalchemy import Column, engine, Boolean
from sqlalchemy import Date
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.exc import NoResultFound

from fcConstant import SQLALCHEMY_DATABASE_URI

BaseModel = declarative_base()

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
        self.protocol_deposit_amount = 0.00
        self.protocol_deposit_revenue = 0.00
        self.cash_to_protocol_deposit = 0.00
        self.protocol_deposit_to_cash = 0.00
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
        # protocolDeposit = session.query(ProtocolDeposit).filter(ProtocolDeposit.date == self.date).one()
        protocolDepositList = session.query(PdProjectList).filter(PdProjectList.date == self.date).all()
        for p in protocolDepositList:
            self.protocol_deposit_amount +=  p.pd_amount
            self.protocol_deposit_revenue += p.pd_interest
            self.cash_to_protocol_deposit += p.pd_cash_to_pd
            self.protocol_deposit_to_cash += p.pd_pd_to_cash

        # session.update(self)
        session.add(self)
        session.flush()
        session.commit()
        return self

    @classmethod
    def findByDate(self, date):
        try:
            return session.query(ProtocolDeposit).filter(ProtocolDeposit.date == date).one()
        except NoResultFound:
            return None


class PdProject(BaseModel):
    """构造器"""

    def __init__(self, pd_project_name, pd_project_rate, stage_rate, pd_stage_amount, pd_stage_rate):
        init_db()
        self.uuid = uuid.uuid1().__str__()
        self.pd_project_name = pd_project_name
        self.pd_project_rate = pd_project_rate
        self.stage_rate = stage_rate
        self.pd_stage_amount = pd_stage_amount
        self.pd_stage_rate = pd_stage_rate

    __tablename__ = 'pd_pro_table'

    uuid = Column(String(32), primary_key=True)
    """协存项目"""
    pd_project_name = Column(String)
    pd_project_rate = Column(Float, default=0.00)
    stage_rate = Column(Boolean, default=False)
    pd_stage_amount = Column(Float, default=0.00)
    pd_stage_rate = Column(Float, default=0.00)

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

    def __init__(self, date, interest_to_principal, cash_to_pd, pd_to_cash):
        init_db()
        self.date = date
        self.uuid = uuid.uuid1().__str__()
        self.pd_amount = 0.00
        self.pd_interest_to_principal = interest_to_principal
        self.pd_cash_to_pd = cash_to_pd
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

    @classmethod
    def listByDate(self, date):
        return session.query(PdProjectList).filter(PdProjectList.date == date).all()

    def getPdProjectInfo(self):
        # 获取协存项目名称
        pd_project = session.query(PdProject).filter(PdProject.uuid == self.pd_obj_uuid).one()
        if pd_project is not None:
            return pd_project.pd_project_name, pd_project.pd_project_rate
        else:
            return '名称暂无', '0.00'

    def save(self, uuid):
        today = self.date

        yesterday = today - datetime.timedelta(days=1)
        print('today is :' + today.strftime('%Y-%m-%d'))

        try:
            yesterday_pd_amount = session.query(PdProjectList.pd_amount).filter(PdProjectList.date == yesterday.strftime('%Y-%m-%d')).one()
            yesterday_pd_principal = session.query(PdProjectList.pd_principal).filter(PdProjectList.date == yesterday.strftime('%Y-%m-%d')).one()
        except:
            session.rollback()
            yesterday_pd_amount = (0.00,)
            yesterday_pd_principal = (0.00,)
        finally:
            session.close()
        pd_obj = session.query(PdProject).filter(PdProject.uuid == uuid).one()
        rate = pd_obj.pd_project_rate

        if pd_obj.stage_rate:
            if self.pd_amount > pd_obj.pd_stage_amount:
                rate = pd_obj.pd_stage_rate

        self.pd_principal = float(yesterday_pd_principal[0]) \
                            + float(self.pd_cash_to_pd) \
                            - float(self.pd_pd_to_cash) \
                            + float(self.pd_interest_to_principal)
        self.pd_interest = float(self.pd_principal) \
                           * float(rate) \
                           / 360
        self.pd_amount = float(yesterday_pd_amount[0]) \
                         + float(self.pd_cash_to_pd) \
                         - float(self.pd_pd_to_cash) \
                         + float(self.pd_interest)
        self.pd_obj_uuid = uuid
        print(session.__dict__)
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
    init_db()

    date = datetime.date(2017,3,10)

    protocolDepositList = session.query(PdProjectList).filter(PdProjectList.date == date).all()
    try:
        pd = session.query(ProtocolDeposit).filter(ProtocolDeposit.date == date).one()
    except:
        pd = ProtocolDeposit(date)
    print(pd.__dict__)
    # for pd in protocolDepositList:
    #     print(pd.__dict__)
    for p in protocolDepositList:
        pd.protocol_deposit_amount += p.pd_amount
        pd.protocol_deposit_revenue += p.pd_interest
        pd.cash_to_protocol_deposit += p.pd_cash_to_pd
        pd.protocol_deposit_to_cash += p.pd_pd_to_cash

    # # session.update(self)
    session.add(pd)
    session.flush()
    session.commit()

    # d = datetime.date.today()
    # protocolDeposit = ProtocolDeposit(datetime.date(d.year, d.month, d.day - 1))
    # print(protocolDeposit)
    # protocolDeposit.save()
    # protocolDeposit.update(datetime.date(d.year, d.month, d.day - 1))

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
