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
    start_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    asset_fee_rate_list = relationship('AssetFeeRate', cascade='all', lazy='subquery')
    asset_trade_list = relationship('AssetTrade', cascade='all', lazy='subquery')
    cash_list = relationship('Cash', cascade='all', lazy='subquery')
    trade_ret_list = relationship('AssetTradeRet', lazy='subquery', cascade='all')
    asset_fee_list = relationship('AssetFee', lazy='subquery', cascade='all')

    def __init__(self, name='', code='', start_date=None, expiry_date=None, type=1, ret_rate=0, cal_date=date.today()):
        MixinBase.__init__(self)
        self.name = name
        self.type = type
        self.ret_rate = ret_rate
        self.code = code
        self.start_date = start_date
        self.expiry_date = expiry_date
        self.date = cal_date

    def __repr__(self):
        return '<AssetClass id=%s, name=%s, type=%s>' % (self.id, self.name, self.type)

        # def cal_principal(self):
        #     pass
