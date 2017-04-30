# encoding:utf8

from __future__ import unicode_literals

from models.CommonModel import *

__all__ = ['DailyFee']


class DailyFee(MixinTotalBase):
    amount = Column(Float, default=0.0)

    def __init__(self, amount=0.0, total_amount=0.0, cal_date=date.today()):
        self.amount = amount
        self.total_amount = total_amount
        self.date = cal_date

    def __repr__(self):
        return '<DailyFee id=%s, amount=%s, total_amount=%s, date=%s>' % (
            self.id, self.amount, self.total_amount, self.date)
