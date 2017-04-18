# encoding:utf8

from __future__ import unicode_literals

from sqlalchemy import ForeignKey, Integer

from models.CommonModel import *

__all__ = ['TradeRet']


class TradeRet(MixinBase):
    asset_trade = Column(String(50), ForeignKey('TB_ASSETTRADE.id'), index=True, nullable=True)
    ret_amount = Column(Float, default=0.0)
    carry_amount = Column(Float, default=0.0)
    carry_to = Column(Integer, default=0)

    asset_trade_obj = relationship('AssetTrade', lazy='joined', cascade='all')
