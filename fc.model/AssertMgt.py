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

from BasicWidget import BasicCell
from EventEngine import EventEngine


BaseModel = declarative_base()

SQLALCHEMY_DATABASE_URI, logging = loadSqliteSetting()
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


class AssertMgt(BaseModel):
    """资管基本信息"""

    def __init__(self):
        pass

    __tablename__ = 'am_table'

    uuid = Column(String(32), primary_key=True)

    substain_amount = Column(Float, nullable=True)
    substain_pricipal = Column(Float, nullable=True)
    today_revenue = Column(Float, nullable=True)
    total_output = Column(Float, nullable=True)
    total_input = Column(Float, nullable=True)
    normal_input = Column(Float, nullable=True)
    cash_input = Column(Float, nullable=True)
    expire_output = Column(Float, nullable=True)

    # relationship()


class AmProject(BaseModel):
    def __init__(self):
        pass

    __tablename__ = 'am_table'

    uuid = Column(String(32), primary_key=True)

    class DelegateElement(BaseModel):
        def __init__(self):
            pass

        __tablename__ = 'am_de_table'

        uuid = Column(String(32), primary_key=True)
        short_for_borrower = Column(Float, nullable=True)
        funds_source = Column(Float, nullable=True)
        loan_amount = Column(Float, nullable=True)
        delegate_rate = Column(Float, nullable=True)
        bearing_days = Column(Float, nullable=True)
        value_date = Column(Float, nullable=True)
        due_date = Column(Float, nullable=True)
        duration = Column(Float, nullable=True)
        delegate_interest = Column(Float, nullable=True)

    class DelegateBankFee(BaseModel):
        def __init__(self):
            pass

        __tablename__ = 'am_dbf_table'

        uuid = Column(String(32), primary_key=True)
        delegate_bank_rate = Column(Float, nullable=True)
        bearing_days = Column(Float, nullable=True)
        delegate_bank_fee = Column(Float, nullable=True)

    class AssertMgtPlanFee(BaseModel):
        def __init__(self):
            pass

        __tablename__ = 'am_ampf_table'

        uuid = Column(String(32), primary_key=True)
        assert_channel_rate = Column(Float, nullable=True)
        bearing_days = Column(Float, nullable=True)
        assert_mgt_fee = Column(Float, nullable=True)

    class AssertMgtPlanRevenue(BaseModel):
        def __init__(self):
            pass

        __tablename__ = 'am_ampr_table'

        uuid = Column(String(32), primary_key=True)
        assert_mgt_total_revenue = Column(Float, nullable=True)
        assert_mgt_daily_revenue = Column(Float, nullable=True)

    class ValuationAdjust(BaseModel):
        def __init__(self):
            pass

        __tablename__ = 'am_va_table'

        uuid = Column(String(32), primary_key=True)
        normal_assert_mgt_daily_revenue_valuation = Column(Float, nullable=True)
        expire_out_to_fund = Column(Float, nullable=True)
        delegate_to_assert = Column(Float, nullable=True)

        class AdjustRecord:
            def __init__(self):
                pass

            __tablename__ = 'am_va_ar_table'

            uuid = Column(String(32), primary_key=True)
            adjust_date = Column(Float, nullable=True)
            trans_fee = Column(Float, nullable=True)
            check_fee = Column(Float, nullable=True)
            total_adjust_fee = Column(Float, nullable=True)
            adjust_result = Column(Float, nullable=True)


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

