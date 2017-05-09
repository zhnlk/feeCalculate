# encoding:utf8

from __future__ import unicode_literals

from datetime import date, timedelta
from unittest import TestCase

from models.AssetClassModel import AssetClass
from models.AssetFeeRateModel import AssetFeeRate
from models.CommonModel import tear_db, init_db
from services.CommonService import save
from utils import StaticValue as SV


class TestBase(TestCase):
    def setUp(self):
        init_db()
        self.init_base_data()

    def tearDown(self):
        tear_db()

    def init_base_data(self):
        # save(Cash(amount=100000, type=SV.CASH_TYPE_DEPOSIT))
        save(AssetClass(name='余额宝', code='10001', type=SV.ASSET_CLASS_FUND))
        save(AssetClass(name='浦发理财一号', code='20007', type=SV.ASSET_CLASS_AGREEMENT))
        agree = AssetClass(name='联顺泰', code='20007', type=SV.ASSET_CLASS_MANAGEMENT,
                           ret_cal_method=SV.RET_TYPE_CASH_CUT_INTEREST, start_date=date.today(),
                           expiry_date=date.today() + timedelta(days=360))
        save(agree)
        save(AssetFeeRate(asset_class=agree.id, rate=20, type=SV.FEE_TYPE_PURCHASE,
                          method=SV.FEE_METHOD_RATIO_EVERY_DAY))
        save(AssetFeeRate(asset_class=agree.id, rate=0.015, type=SV.FEE_TYPE_REDEEM,
                          method=SV.FEE_METHOD_RATIO_ONE_TIME))
