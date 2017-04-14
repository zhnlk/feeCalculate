# encoding:utf8
from __future__ import unicode_literals

import calendar
from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import create_engine, Date, String, Boolean, Column, Float
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import Session, sessionmaker

from fcConstant import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
session = Session()
Base = declarative_base()


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


def init_db():
    Base.metadata.create_all(engine)


def tear_db():
    Base.metadata.drop_all(engine)
