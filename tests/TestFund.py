# encoding:utf8

from __future__ import unicode_literals

from models.AssetClassModel import AssetClass
from models.AssetTradeRetModel import AssetTradeRet
from models.CashModel import Cash
from services.AssetService import asset_ret_carry_to_cash
from services.CommonService import query
from tests.TestBase import TestBase
from utils import StaticValue as SV


class TestFund(TestBase):
    def test_asset_ret_carry_to_cash(self):
        asset = query(AssetClass).filter(AssetClass.type == SV.ASSET_CLASS_FUND).one()
        asset_ret_carry_to_cash(asset=asset, amount=1004)
        asset_trade_ret = query(AssetTradeRet).filter(AssetTradeRet.asset_class == asset.id,
                                                      AssetTradeRet.type == SV.RET_TYPE_CASH).one()

        self.assertTrue(asset_trade_ret)
        self.assertEqual(asset_trade_ret.amount, 1004)
        self.assertEqual(asset_trade_ret.total_amount, 1004)

        cash = query(Cash).filter(Cash.type == SV.CASH_TYPE_CARRY).one()

        self.assertTrue(cash)
        self.assertEqual(cash.amount, 1004)
        self.assertEqual(cash.total_amount, 1004)
        self.assertEqual(cash.type, SV.CASH_TYPE_CARRY)
