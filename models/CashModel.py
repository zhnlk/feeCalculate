# encoding:utf8

from __future__ import unicode_literals

from sqlalchemy import Integer

from models.CommonModel import *

__all__ = ['Cash']


class Cash(MixinBase):
    amount = Column(Float, default=0.0)
    type = Column(Integer, default=1)

    def __init__(self, type=1, amount=0.0):
        MixinBase.__init__(self)
        self.type = type
        self.amount = amount

    def __repr__(self):
        return '<Cash id=%s, amount=%s, type=%s>' % (self.id, self.amount, self.type)
