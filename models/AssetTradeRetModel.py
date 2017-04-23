# encoding:utf8

from __future__ import unicode_literals

from sqlalchemy import ForeignKey, Integer

from models.CommonModel import *

__all__ = ['TradeRet']


class AssetTradeRet(MixinTotalBase):
    asset_class = Column(String(50), ForeignKey('TB_ASSETCLASS.id'), index=True, nullable=True)
    amount = Column(Float, default=0.0)
    type = Column(Integer, default=0)

    asset_class_obj = relationship('AssetClass', lazy='joined', cascade='all')

    def __init__(self, asset_class='', amount=0, type=0, total_amount=0.0, cal_date=date.today()):
        MixinBase.__init__(self)
        self.asset_class = asset_class
        self.amount = amount
        self.type = type
        self.date = cal_date
        self.total_amount = total_amount

    def __repr__(self):
        return '<TradeRet id=%s, amount=%s, type=%s>' % (self.id, self.amount, self.type)
