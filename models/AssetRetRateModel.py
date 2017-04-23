# encoding:utf8


from __future__ import unicode_literals

from sqlalchemy import ForeignKey

from models.CommonModel import *

__all__ = ['AssetRetRate']


class AssetRetRate(MixinBase):
    asset_class = Column(String(50), ForeignKey('TB_ASSETCLASS.id'), index=True, nullable=True)
    ret_rate = Column(Float, default=0.03)
    threshold = Column(Float, default=0.0)

    asset_class_obj = relationship('AssetClass', cascade='all')

    def __init__(self, asset_id='', ret_rate=0.03, threshold=0.0, cal_date=date.today()):
        MixinBase.__init__(self)
        self.asset_class = asset_id
        self.ret_rate = ret_rate
        self.threshold = threshold
        self.date = cal_date

    def __repr__(self):
        return '<AssetRetRate id=%s, asset_class=%s, ret_rate=%s, threshold=%s>' % (
            self.id, self.asset_class, self.ret_rate, self.threshold)
