# encoding:utf8

from __future__ import unicode_literals

import unittest

from models.CashModel import Cash
from services.CashService import add_cash_daily_data
from services.CommonService import query
from tests.TestBase import TestBase
from utils import StaticValue as SV


class TestCashService(TestBase):
    def test_add_cash_daily_data(self):
        add_cash_daily_data(draw_amount=10001, draw_fee=10.01, deposit_amount=1000000, ret_amount=4000)
        draw_record = query(Cash).filter(Cash.type == SV.CASH_TYPE_DRAW)
        self.assertTrue(draw_record)
        self.assertEqual(draw_record.count(), 1)
        self.assertEqual(draw_record.one().amount, 10001)

        # draw_fee_record = query(Cash).filter(Cash.type == SV.CASH_TYPE_FEE)
        # self.assertTrue(draw_fee_record)
        # self.assertEqual(draw_fee_record.count(), 1)
        # self.assertEqual(draw_fee_record.one().amount, 10.01)
        #
        # deposit_record = query(Cash).filter(Cash.type == SV.CASH_TYPE_DEPOSIT)
        # self.assertTrue(deposit_record)
        # # self.assertEqual(deposit_record.count(), 1)
        # self.assertEqual(deposit_record.one().amount, 1000000)
        #
        # ret_record = query(Cash).filter(Cash.type == SV.CASH_TYPE_DEPOSIT)
        # self.assertTrue(ret_record)
        # self.assertEqual(ret_record.count(), 1)
        # self.assertEqual(ret_record.one().amount, 1000000)
        #
        # add_cash_daily_data(draw_amount=10001, draw_fee=10.01, deposit_amount=1000000, ret_amount=4000)
        #
        # draw_record = query(Cash).filter(Cash.type == SV.CASH_TYPE_DRAW)
        # self.assertTrue(draw_record)
        # self.assertEqual(draw_record.count(), 2)
        # self.assertEqual(sum(list(map(lambda x: x.amount, draw_record))), 10001 * 2)
        #
        # draw_fee_record = query(Cash).filter(Cash.type == SV.CASH_TYPE_FEE)
        # self.assertTrue(draw_fee_record)
        # self.assertEqual(draw_fee_record.count(), 2)
        # self.assertEqual(sum(list(map(lambda x: x.amount, draw_fee_record))), 10.01 * 2)
        #
        # deposit_record = query(Cash).filter(Cash.type == SV.CASH_TYPE_DEPOSIT)
        # self.assertTrue(deposit_record)
        # self.assertEqual(deposit_record.count(), 2)
        # self.assertEqual(sum(list(map(lambda x: x.amount, deposit_record))), 1000000 * 2)
        #
        # ret_record = query(Cash).filter(Cash.type == SV.CASH_TYPE_DEPOSIT)
        # self.assertTrue(ret_record)
        # self.assertEqual(ret_record.count(), 2)
        # self.assertEqual(sum(list(map(lambda x: x.amount, deposit_record))), 1000000 * 2)

    def test_get_detail(self):
        pass


if __name__ == '__main__':
    unittest.main()
