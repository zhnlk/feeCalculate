# encoding:utf8

from __future__ import unicode_literals

from sqlalchemy import Integer, ForeignKey

from models.CommonModel import *

__all__ = ['TradeFee']


class TradeFee(MixinBase):
    amount = Column(Float, default=0.0)
    asset_trade = Column(String(50), ForeignKey('TB_ASSETTRADE.id'), index=True, nullable=True)
    type = Column(Integer, default=0)
    asset_trade_obj = relationship('AssetTrade', lazy='joined', cascade='all')

    def __init__(self, amount=0, asset_trade='', type=1, cal_date=date.today()):
        MixinBase.__init__(self)
        self.amount = amount
        self.asset_trade = asset_trade
        self.type = type
        self.date = cal_date

    def __repr__(self):
        return '<TradeFee id=%s, amount=%s, asset_trade=%s, type=%s>' % (
            self.id, self.amount, self.asset_trade, self.type)
