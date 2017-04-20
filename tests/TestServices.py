# encoding:utf8

from __future__ import unicode_literals

import logging
import sys
import unittest
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.AssetClassModel import AssetClass
from models.AssetFeeRateModel import AssetFeeRate
from models.CashModel import Cash
from models.CommonModel import tear_db, init_db
from services.CommonService import save, get_asset_by_name, get_obj_by_id, purchase, get_cash_by_asset_and_type, \
    get_trade_by_asset_and_type, get_trade_fee_by_asset_and_type, redeem, get_asset_trade_change, get_cash_trade_change
from utils import StaticValue as SV


class TestService(unittest.TestCase):
    def setUp(self):
        global engine, Base, Session
        engine = create_engine('sqlite:///test.db', echo=True)
        Session = sessionmaker(bind=engine, autocommit=False, autoflush=True)
        # Session.configure()
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

    def test_get_obj_by_id(self):
        asset = get_asset_by_name(name='浦发理财一号')
        asset_id = asset.id
        asset = get_obj_by_id(obj=AssetClass, obj_id=asset.id)
        self.assertEqual(asset_id, asset.id)
        self.assertTrue(asset)

    def test_get_asset_by_name(self):
        asset = get_asset_by_name(name='余额宝')
        self.assertTrue(asset)
        self.assertEqual(asset.name, '余额宝')
        self.assertEqual(asset.code, '10001')

    def test_purchase_no_fee(self):
        asset = get_asset_by_name(name='余额宝')
        purchase(asset=asset, amount=10000)
        cash = get_cash_by_asset_and_type(asset_id=asset.id, trade_type=SV.CASH_TYPE_PURCHASE)
        # self.assertWarns(type(cash))
        self.assertTrue(cash)
        self.assertTrue(cash[0].amount == 10000)
        self.assertEqual(cash[0].type, SV.CASH_TYPE_PURCHASE)
        self.assertTrue(cash.count(), 1)
        trade_asset = get_trade_by_asset_and_type(asset_id=asset.id, trade_type=SV.ASSET_TYPE_PURCHASE)
        self.assertTrue(trade_asset)
        self.assertEqual(trade_asset.count(), 1)
        self.assertEqual(trade_asset[0].type, SV.ASSET_TYPE_PURCHASE)
        self.assertEqual(trade_asset[0].amount, 10000)

    def test_purchase_fee(self):
        asset = get_asset_by_name(name='联顺泰')
        purchase(asset=asset, amount=10000)

        cash = get_cash_by_asset_and_type(asset_id=asset.id, trade_type=SV.CASH_TYPE_PURCHASE)

        self.assertTrue(cash)
        self.assertEqual(cash.count(), 1)
        self.assertEqual(cash[0].amount, 10000)
        self.assertEqual(cash[0].type, SV.CASH_TYPE_PURCHASE)

        trade_asset = get_trade_by_asset_and_type(asset_id=asset.id, trade_type=SV.ASSET_TYPE_PURCHASE)
        self.assertTrue(trade_asset)
        self.assertEqual(trade_asset.count(), 1)
        self.assertEqual(trade_asset[0].type, SV.ASSET_TYPE_PURCHASE)
        self.assertEqual(trade_asset[0].amount, 10000)
        # self.assertEqual(trade_asset[0].id, '')
        fees = get_trade_fee_by_asset_and_type(asset_trade_id=trade_asset[0].id, fee_type=SV.FEE_TYPE_PURCHASE)
        self.assertTrue(fees)
        self.assertEqual(fees.count(), 1)
        self.assertTrue(fees[0])
        self.assertEqual(fees[0].amount, 20)
        self.assertEqual(fees[0].type, SV.FEE_TYPE_PURCHASE)

    def test_redeem_no_fee(self):
        asset = get_asset_by_name(name='余额宝')
        redeem(asset=asset, amount=10000)
        cash = get_cash_by_asset_and_type(asset_id=asset.id, trade_type=SV.CASH_TYPE_REDEEM)
        self.assertTrue(cash)
        self.assertTrue(cash[0].amount == 10000)
        self.assertEqual(cash[0].type, SV.CASH_TYPE_REDEEM)
        self.assertTrue(cash.count(), 1)
        trade_asset = get_trade_by_asset_and_type(asset_id=asset.id, trade_type=SV.ASSET_TYPE_REDEEM)
        self.assertTrue(trade_asset)
        self.assertEqual(trade_asset.count(), 1)
        self.assertEqual(trade_asset[0].type, SV.ASSET_TYPE_REDEEM)
        self.assertEqual(trade_asset[0].amount, 10000)

    def test_redeem_fee(self):
        asset = get_asset_by_name(name='联顺泰')
        redeem(asset=asset, amount=10000)

        cash = get_cash_by_asset_and_type(asset_id=asset.id, trade_type=SV.CASH_TYPE_REDEEM)

        self.assertTrue(cash)
        self.assertEqual(cash.count(), 1)
        self.assertEqual(cash[0].amount, 10000)
        self.assertEqual(cash[0].type, SV.CASH_TYPE_REDEEM)

        trade_asset = get_trade_by_asset_and_type(asset_id=asset.id, trade_type=SV.ASSET_TYPE_REDEEM)
        self.assertTrue(trade_asset)
        self.assertEqual(trade_asset.count(), 1)
        self.assertEqual(trade_asset[0].type, SV.ASSET_TYPE_REDEEM)
        self.assertEqual(trade_asset[0].amount, 10000)
        fees = get_trade_fee_by_asset_and_type(asset_trade_id=trade_asset[0].id, fee_type=SV.FEE_TYPE_REDEEM)
        self.assertTrue(fees)
        self.assertEqual(fees.count(), 1)
        self.assertTrue(fees[0])
        self.assertEqual(fees[0].amount, 150)
        self.assertEqual(fees[0].type, SV.FEE_TYPE_REDEEM)

    def test_get_asset_trade_change(self):
        asset = get_asset_by_name(name='余额宝')
        redeem(asset=asset, amount=10000)
        purchase(asset=asset, amount=20000)
        redeem(asset=asset, amount=10000)
        purchase(asset=asset, amount=20000)
        trade_records = get_asset_trade_change(cal_date=date.today(), asset_type=SV.ASSET_CLASS_FUND,
                                               trade_type=SV.ASSET_TYPE_PURCHASE)
        self.assertTrue(trade_records)
        self.assertEqual(len(trade_records), 2)
        self.assertListEqual(list1=list(map(lambda x: x.amount, trade_records)), list2=[20000, 20000])

        trade_records = get_asset_trade_change(cal_date=date.today(), asset_type=SV.ASSET_CLASS_FUND,
                                               trade_type=SV.ASSET_TYPE_REDEEM)
        self.assertTrue(trade_records)
        self.assertEqual(len(trade_records), 2)
        self.assertListEqual(list1=list(map(lambda x: x.amount, trade_records)), list2=[10000, 10000])

    def test_get_cash_trade_change(self):
        asset = get_asset_by_name(name='余额宝')
        redeem(asset=asset, amount=10000)
        purchase(asset=asset, amount=21000)
        redeem(asset=asset, amount=10000)
        purchase(asset=asset, amount=26000)
        cashes = get_cash_trade_change(cal_date=date.today(), asset_type=SV.ASSET_CLASS_FUND,
                                       trade_type=SV.CASH_TYPE_PURCHASE)
        self.assertTrue(cashes)
        self.assertEqual(len(cashes), 2)
        self.assertListEqual(list1=list(map(lambda x: x.amount, cashes)), list2=[21000, 26000])
        cashes = get_cash_trade_change(cal_date=date.today(), asset_type=SV.ASSET_CLASS_FUND,
                                       trade_type=SV.CASH_TYPE_REDEEM)
        self.assertTrue(cashes)
        self.assertEqual(len(cashes), 2)
        self.assertListEqual(list1=list(map(lambda x: x.amount, cashes)), list2=[10000, 10000])

    def test_check_reconciliation(self):
        asset = get_asset_by_name(name='余额宝')
        purchase(asset=asset, amount=21000)
        trade_records = get_asset_trade_change(cal_date=date.today(), asset_type=SV.ASSET_CLASS_FUND,
                                               trade_type=SV.ASSET_TYPE_PURCHASE)
        cashes = get_cash_trade_change(cal_date=date.today(), asset_type=SV.ASSET_CLASS_FUND,
                                       trade_type=SV.CASH_TYPE_PURCHASE)
        self.assertTrue(trade_records)
        self.assertTrue(cashes)
        self.assertEqual(len(trade_records), 1)
        self.assertEqual(len(cashes), 1)
        self.assertEqual(trade_records[0].amount, cashes[0].amount)
        self.assertAlmostEqual(trade_records[0].time, cashes[0].time, places=4)

        redeem(asset=asset, amount=10000)
        trade_records = get_asset_trade_change(cal_date=date.today(), asset_type=SV.ASSET_CLASS_FUND,
                                               trade_type=SV.ASSET_TYPE_REDEEM)
        cashes = get_cash_trade_change(cal_date=date.today(), asset_type=SV.ASSET_CLASS_FUND,
                                       trade_type=SV.CASH_TYPE_REDEEM)
        self.assertTrue(trade_records)
        self.assertTrue(cashes)
        self.assertEqual(len(trade_records), 1)
        self.assertEqual(len(cashes), 1)
        self.assertEqual(trade_records[0].amount, cashes[0].amount)
        self.assertAlmostEqual(trade_records[0].time, cashes[0].time, places=4)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout)
    logging.getLogger("LOG")
    unittest.main()