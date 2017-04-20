# encoding:utf8

from __future__ import unicode_literals

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.AssetClassModel import AssetClass
from models.AssetFeeRateModel import AssetFeeRate
from models.CashModel import Cash
from models.CommonModel import tear_db, init_db
from services.CommonService import save
from utils import StaticValue as SV


class TestCashService(unittest.TestCase):
    def setUp(self):
        global engine, Base, Session
        engine = create_engine('sqlite:///test.db', echo=True)
        Session = sessionmaker(bind=engine, autocommit=False, autoflush=True)
        init_db()
        save(Cash(amount=10000, type=SV.CASH_TYPE_DEPOSIT))
        save(AssetClass(name='余额宝', code='10001', type=SV.ASSET_CLASS_FUND, ret_rate=0.04))
        save(AssetClass(name='浦发理财一号', code='20007', type=SV.ASSET_CLASS_AGREEMENT_DEPOSIT, ret_rate=0.035))
        agree = AssetClass(name='联顺泰', code='20007', type=SV.ASSET_CLASS_MANAGEMENT, ret_rate=0.08)

        save(AssetFeeRate(asset_class=agree.id, rate=20, type=SV.FEE_TYPE_PURCHASE, method=SV.FEE_METHOD_TIMES))
        save(AssetFeeRate(asset_class=agree.id, rate=0.015, type=SV.FEE_TYPE_REDEEM, method=SV.FEE_METHOD_RATIO))
        save(agree)

    def tearDown(self):
        tear_db()

    def test_add_cash_daily_data(self):
        pass


if __name__ == '__main__':
    unittest.main()
