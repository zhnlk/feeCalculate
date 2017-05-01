# encoding:utf8
from __future__ import unicode_literals

import calendar
from datetime import date, datetime
from functools import wraps
from uuid import uuid4

from sqlalchemy import create_engine, Date, String, Boolean, Column, Float
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, relationship

from utils import StaticValue as SV

engine = create_engine(SV.SQLALCHEMY_DATABASE_URI, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)


def session_deco(func):
    @wraps(func)
    def __deco__(*args, **kwargs):
        session = Session()
        if SV.SESSION_KEY not in kwargs.keys():
            kwargs.update({SV.SESSION_KEY: session})
        ret = func(*args, **kwargs)
        session.flush()
        session.commit()
        return ret

    return __deco__


class MixinBase(Base):
    __abstract__ = True

    def __init__(self):
        self.id = uuid4().hex

    @declared_attr.cascading
    def id(cls):
        return Column(String(50), primary_key=True, default=uuid4().hex)

    time = Column(Float, default=calendar.timegm(datetime.now().timetuple()))
    date = Column(Date, default=date.today)
    is_active = Column(Boolean, default=True)

    @declared_attr
    def __tablename__(cls):
        return '%s%s' % ('TB_', cls.__name__.upper())


class MixinTotalBase(MixinBase):
    __abstract__ = True
    total_amount = Column(Float, default=0.0)


def init_db():
    Base.metadata.create_all(engine)


def tear_db():
    Base.metadata.drop_all(engine)
