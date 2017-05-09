# encoding:utf8

from __future__ import unicode_literals

# from sqlalchemy.testing.fixtures import TestBase
#
import unittest

from datetime import date

from models.AssetClassModel import AssetClass
from models.AssetRetRateModel import AssetRetRate
from models.AssetTradeModel import AssetTrade
from models.AssetTradeRetModel import AssetTradeRet
from models.CashModel import Cash
from services.AssetService import asset_ret_carry_to_principal, get_asset_rate_by_amount, asset_ret_carry_to_cash, \
    add_agreement_daily_data
from services.CommonService import query, save
from tests.TestBase import TestBase
from utils import StaticValue as SV


class TestAgreement(TestBase):
    def test_asset_ret_carry_to_principal(self):
        asset = query(AssetClass).filter(AssetClass.is_active, AssetClass.type == SV.ASSET_CLASS_AGREEMENT).one()
        self.assertTrue(asset)
        asset_ret_carry_to_principal(asset=asset, amount=0)
        self.assertFalse(query(AssetTradeRet).filter(AssetTradeRet.is_active, AssetTradeRet.amount == 0).count())
        asset_ret_carry_to_principal(asset=asset, amount=10000)
        self.assertEqual(
            query(AssetTradeRet).filter(AssetTradeRet.is_active, AssetTradeRet.asset_class == asset.id).one().amount,
            10000
        )
        self.assertEqual(
            query(AssetTradeRet).filter(AssetTradeRet.is_active, AssetTradeRet.asset_class == asset.id).one().type,
            SV.RET_TYPE_PRINCIPAL
        )
        self.assertEqual(
            query(AssetTradeRet).filter(AssetTradeRet.is_active,
                                        AssetTradeRet.asset_class == asset.id).one().total_amount,
            10000
        )
        self.assertEqual(
            query(AssetTrade).filter(AssetTrade.is_active, AssetTrade.asset_class == asset.id).one().amount,
            10000
        )
        self.assertEqual(
            query(AssetTrade).filter(AssetTrade.is_active, AssetTrade.asset_class == asset.id).one().total_amount,
            10000
        )
        self.assertEqual(
            query(AssetTrade).filter(AssetTrade.is_active, AssetTrade.asset_class == asset.id).one().type,
            SV.ASSET_TYPE_RET_CARRY
        )

    def test_get_asset_rate_by_amount(self):
        asset = AssetClass(name='test_1', code='1001', type=SV.ASSET_CLASS_AGREEMENT)
        asset_ret_rate = AssetRetRate(asset_id=asset.id, ret_rate=0.03, threshold=0.0, interest_days=360)
        save(asset_ret_rate)
        asset_ret_rate = AssetRetRate(asset_id=asset.id, ret_rate=0.08, threshold=10000, interest_days=360)
        save(asset_ret_rate)
        asset_ret_rate = AssetRetRate(asset_id=asset.id, ret_rate=0.1, threshold=20000, interest_days=360)
        save(asset_ret_rate)
        save(asset)

        rate = get_asset_rate_by_amount(rates=asset.asset_ret_rate_list, amount=100)
        self.assertEqual(rate.ret_rate, 0.03)
        rate = get_asset_rate_by_amount(rates=asset.asset_ret_rate_list, amount=10000)
        self.assertEqual(rate.ret_rate, 0.08)
        rate = get_asset_rate_by_amount(rates=asset.asset_ret_rate_list, amount=20000)
        self.assertEqual(rate.ret_rate, 0.1)

    def test_asset_ret_carry_to_cash(self):
        asset = query(AssetClass).filter(AssetClass.is_active, AssetClass.type == SV.ASSET_CLASS_FUND).one()
        asset_ret_carry_to_cash(asset=asset, amount=10000)
        trade_ret = query(AssetTradeRet).filter(AssetTradeRet.is_active, AssetTradeRet.asset_class == asset.id).one()
        self.assertTrue(trade_ret)
        self.assertEqual(trade_ret.amount, 10000)
        self.assertEqual(trade_ret.total_amount, 10000)
        self.assertEqual(trade_ret.type, SV.RET_TYPE_CASH)

        cash = query(Cash).filter(Cash.is_active).one()
        self.assertTrue(cash)
        self.assertEqual(cash.amount, 10000)
        self.assertEqual(cash.total_amount, 10000)

    def test_add_agreement_daily_data(self):
        asset = query(AssetClass).filter(AssetClass.is_active, AssetClass.type == SV.ASSET_CLASS_AGREEMENT).one()

        add_agreement_daily_data(asset_id=asset.id, ret_carry_asset_amount=1001, purchase_amount=1002,
                                 redeem_amount=1003)
        trade_ret = query(AssetTradeRet).filter(AssetTradeRet.is_active, AssetTradeRet.type == SV.RET_TYPE_PRINCIPAL,
                                                AssetTradeRet.asset_class == asset.id).one()
        self.assertTrue(trade_ret)
        self.assertEqual(trade_ret.amount, 1001)
        self.assertEqual(trade_ret.total_amount, 1001)
        self.assertEqual(trade_ret.type, SV.RET_TYPE_PRINCIPAL)

        asset_trade = query(AssetTrade).filter(AssetTrade.is_active, AssetTrade.type == SV.ASSET_TYPE_RET_CARRY,
                                               AssetTrade.asset_class == asset.id).one()
        self.assertTrue(asset_trade)
        self.assertEqual(asset_trade.amount, 1001)
        self.assertEqual(asset_trade.total_amount, 1001)

        asset_trade = query(AssetTrade).filter(AssetTrade.is_active, AssetTrade.type == SV.ASSET_TYPE_PURCHASE,
                                               AssetTrade.asset_class == asset.id).one()
        self.assertTrue(asset_trade)
        self.assertEqual(asset_trade.amount, 1002)
        self.assertEqual(asset_trade.total_amount, 1002)
        self.assertEqual(asset_trade.type, SV.ASSET_TYPE_PURCHASE)

        cash = query(Cash).filter(Cash.is_active, Cash.type == -SV.ASSET_CLASS_AGREEMENT,
                                  Cash.asset_class == asset.id).one()

        self.assertTrue(cash)
        self.assertEqual(cash.amount, 1002)
        self.assertEqual(cash.total_amount, 1002)
        self.assertEqual(cash.date, date.today())
        self.assertEqual(cash.type, -SV.ASSET_CLASS_AGREEMENT)

        asset_trade = query(AssetTrade).filter(AssetTrade.is_active, AssetTrade.type == SV.ASSET_TYPE_REDEEM,
                                               AssetTrade.asset_class == asset.id).one()
        self.assertTrue(asset_trade)
        self.assertEqual(asset_trade.amount, 1003)
        self.assertEqual(asset_trade.total_amount, 1003)
        self.assertEqual(asset_trade.type, SV.ASSET_TYPE_REDEEM)

        cash = query(Cash).filter(Cash.is_active, Cash.type == SV.ASSET_CLASS_AGREEMENT,
                                  Cash.asset_class == asset.id).one()

        self.assertTrue(cash)
        self.assertEqual(cash.amount, 1003)
        self.assertEqual(cash.total_amount, 1003)
        self.assertEqual(cash.date, date.today())
        self.assertEqual(cash.type, SV.ASSET_CLASS_AGREEMENT)


if __name__ == '__main__':
    unittest.main()
