# encoding:utf8

from __future__ import unicode_literals

from sqlalchemy.types import Integer

from models.CommonModel import *

__all__ = ['AssetClass']


class AssetClass(MixinBase):
    name = Column(String(50), default='')
    code = Column(String(50), default='')
    type = Column(Integer, default=1)
    ret_rate = Column(Float, default=0.0)
    start_date = Column(Date, default=date.today)
    expiry_date = Column(Date, default=date.today)
    asset_fee_rate_list = relationship('AssetFeeRate', cascade='all', lazy='subquery')
    asset_trade_list = relationship('AssetTrade', cascade='all', lazy='subquery')
    cash_list = relationship('Cash', cascade='all', lazy='subquery')

    def __init__(self, name='', code='', type=1, ret_rate=0):
        MixinBase.__init__(self)
        self.name = name
        self.type = type
        self.ret_rate = ret_rate
        self.code = code

    def __repr__(self):
        return '<AssetClass id=%s, name=%s, type=%s>' % (self.id, self.name, self.type)
