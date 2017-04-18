# encoding:utf8

from __future__ import unicode_literals

from sqlalchemy import Integer, ForeignKey

from models.CommonModel import *

__all__ = ['Cash']


class Cash(MixinBase):
    amount = Column(Float, default=0.0)
    type = Column(Integer, default=1)
    asset_class = Column(String(50), ForeignKey('TB_ASSETCLASS.id'), index=True, nullable=True)
    asset_class_obj = relationship('AssetClass', lazy='joined', cascade='all')

    def __init__(self, asset_class='', type=1, amount=0.0):
        MixinBase.__init__(self)
        self.type = type
        self.amount = amount
        self.asset_class = asset_class

    def __repr__(self):
        return '<Cash id=%s, amount=%s, type=%s>' % (self.id, self.amount, self.type)
