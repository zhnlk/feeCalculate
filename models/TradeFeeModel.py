# encoding:utf8

from __future__ import unicode_literals

from sqlalchemy import Integer

from models.CommonModel import *

__all__ = ['TradeFee']


class TradeFee(MixinBase):
    amount = Column(Float, default=0.0)
    asset_trade = Column(String(50), default='')
    type = Column(Integer, default=0)

    def __init__(self, amount=0, asset_trade='', type=1):
        MixinBase.__init__(self)
        self.amount = amount
        self.asset_trade = asset_trade
        self.type = type

    def __repr__(self):
        return '<TradeFee id=%s, amount=%s, asset_trade=%s, type=%s>' % (
            self.id, self.amount, self.asset_trade, self.type)
