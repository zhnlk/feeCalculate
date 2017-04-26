# encoding:utf8

from __future__ import unicode_literals

import unittest
from datetime import date

from models.AssetClassModel import AssetClass
from models.AssetTradeModel import AssetTrade
from models.CashModel import Cash
from services.CommonService import purchase, query, redeem
from tests.TestBase import TestBase
from utils import StaticValue as SV


class TestService(TestBase):
    def test_purchase(self):
        asset = query(AssetClass).filter(AssetClass.type == SV.ASSET_CLASS_AGREEMENT).one()
        purchase(asset=asset, amount=10005, cal_date=date(2018, 1, 1))
        cash = query(Cash).filter(Cash.asset_class == asset.id, Cash.type == -SV.ASSET_CLASS_AGREEMENT).one()
        self.assertTrue(cash)
        self.assertEqual(cash.amount, 10005)
        self.assertEqual(cash.total_amount, 10005)
        self.assertEqual(cash.type, -SV.ASSET_CLASS_AGREEMENT)
        self.assertEqual(cash.date, date(2018, 1, 1))

        asset_trade = query(AssetTrade).filter(AssetTrade.type == SV.ASSET_TYPE_PURCHASE,
                                               AssetTrade.asset_class == asset.id).one()

        self.assertTrue(asset_trade)
        self.assertEqual(asset_trade.amount, 10005)
        self.assertEqual(asset_trade.total_amount, 10005)
        self.assertEqual(asset_trade.date, date(2018, 1, 1))
        self.assertEqual(asset_trade.type, SV.ASSET_TYPE_PURCHASE)

        purchase(asset=asset, amount=10000, cal_date=date(2018, 1, 2))
        cash = query(Cash).filter(Cash.asset_class == asset.id, Cash.type == -SV.ASSET_CLASS_AGREEMENT,
                                  Cash.date == date(2018, 1, 2)).one()

        self.assertTrue(cash)
        self.assertEqual(cash.amount, 10000)
        self.assertEqual(cash.total_amount, 20005)

        asset_trade = query(AssetTrade).filter(AssetTrade.type == SV.ASSET_TYPE_PURCHASE,
                                               AssetTrade.asset_class == asset.id,
                                               AssetTrade.date == date(2018, 1, 2)).one()
        self.assertTrue(asset_trade)
        self.assertEqual(asset_trade.amount, 10000)
        self.assertEqual(asset_trade.total_amount, 20005)

        cash = query(Cash).filter(Cash.asset_class == asset.id, Cash.type == -SV.ASSET_CLASS_AGREEMENT)
        self.assertEqual(cash.count(), 2)
        self.assertEqual(cash[0].amount, 10005)

    def test_redeem(self):
        asset = query(AssetClass).filter(AssetClass.type == SV.ASSET_CLASS_AGREEMENT).one()
        redeem(asset=asset, amount=10005, cal_date=date(2018, 1, 1))
        cash = query(Cash).filter(Cash.asset_class == asset.id, Cash.type == SV.ASSET_CLASS_AGREEMENT).one()
        self.assertTrue(cash)
        self.assertEqual(cash.amount, 10005)
        self.assertEqual(cash.total_amount, 10005)
        self.assertEqual(cash.type, SV.ASSET_CLASS_AGREEMENT)
        self.assertEqual(cash.date, date(2018, 1, 1))

        asset_trade = query(AssetTrade).filter(AssetTrade.type == SV.ASSET_TYPE_REDEEM,
                                               AssetTrade.asset_class == asset.id).one()

        self.assertTrue(asset_trade)
        self.assertEqual(asset_trade.amount, 10005)
        self.assertEqual(asset_trade.total_amount, 10005)
        self.assertEqual(asset_trade.date, date(2018, 1, 1))
        self.assertEqual(asset_trade.type, SV.ASSET_TYPE_REDEEM)

        redeem(asset=asset, amount=10000, cal_date=date(2018, 1, 2))

        cash = query(Cash).filter(Cash.asset_class == asset.id, Cash.type == SV.ASSET_CLASS_AGREEMENT)
        self.assertTrue(cash)
        self.assertEqual(cash.count(), 2)
        self.assertEqual(cash[1].amount, 10000)
        self.assertEqual(cash[1].total_amount, 20005)
        self.assertEqual(cash[0].amount, 10005)
        self.assertEqual(cash[0].total_amount, 10005)


if __name__ == '__main__':
    unittest.main()
