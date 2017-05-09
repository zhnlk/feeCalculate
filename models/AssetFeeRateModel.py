# encoding:utf8

from __future__ import unicode_literals

from sqlalchemy import ForeignKey, Integer

from models.CommonModel import *

__all__ = ['AssetFeeRate']


class AssetFeeRate(MixinBase):
    asset_class = Column(String(50), ForeignKey('TB_ASSETCLASS.id'), index=True, nullable=True)
    rate = Column(Float, default='0.0')
    type = Column(Integer, default=-1)
    method = Column(Integer, default=0)
    fee_days = Column(Integer, default=360)

    asset_class_obj = relationship('AssetClass', cascade='all')

    def __init__(self, asset_class='', rate=0.0, type=1, method=1, fee_days=0, cal_date=date.today()):
        MixinBase.__init__(self)
        self.asset_class = asset_class
        self.rate = rate
        self.type = type
        self.method = method
        self.fee_days = fee_days
        self.date = cal_date

    def __repr__(self):
        return '<AssetRate id=%s, asset_class=%s, rate=%s, type=%s>' % (self.id, self.asset_class, self.rate, self.type)
