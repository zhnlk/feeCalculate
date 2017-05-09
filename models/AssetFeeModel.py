# encoding:utf8

from __future__ import unicode_literals

from sqlalchemy import Integer, ForeignKey

from models.CommonModel import *

__all__ = ['AssetFee']


class AssetFee(MixinTotalBase):
    amount = Column(Float, default=0.0)
    asset_class = Column(String(50), ForeignKey('TB_ASSETCLASS.id'), index=True, nullable=True)
    type = Column(Integer, default=0)
    method = Column(Integer, default=0)
    asset_class_obj = relationship('AssetClass', cascade='all')

    def __init__(self, amount=0, asset_class='', type=1, total_amount=0.0, method=1, cal_date=date.today()):
        MixinBase.__init__(self)
        self.amount = amount
        self.asset_class = asset_class
        self.type = type
        self.date = cal_date
        self.total_amount = total_amount
        self.method = method

    def __repr__(self):
        return '<TradeFee id=%s, amount=%s, asset_trade=%s, type=%s>' % (
            self.id, self.amount, self.asset_trade, self.type)
