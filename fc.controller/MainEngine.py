# encoding: UTF-8
import datetime

import AssetService
import CashService
from Cash import Cash
from EventEngine import *
from MoneyFund import MfProjectList, MoneyFund
from ProtocolDeposit import PdProject, PdProjectList, ProtocolDeposit
from Valuation import Valuation


class MainEngine(object):
    """主引擎"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        # 记录今日日期
        self.todayDate = datetime.datetime.today()

        # 创建事件引擎
        self.eventEngine = EventEngine()
        self.eventEngine.start()

    # ----------------------------------------------------------------------

    def exit(self):
        """退出程序前调用，保证正常退出"""

        # 停止事件引擎
        self.eventEngine.stop()

    def getMainCostData(self):

        return self.todayDate, self.todayDate, '今日资金成本'

    def getMainFeeData(self):
        rate, duration = self.getFeeConstrant()
        return rate, duration

    def getMainTotalValuationData(self):
        return Valuation.listAll()

    def saveTotalValuationData(self, date):
        v = Valuation.findByDate(date)
        if v:
            return v

        valuation = Valuation(date)
        # 现金的总额
        cash = Cash.findByDate(date)
        valuation.cash = cash.getTodayTotalCash()

        # 协存
        pd = ProtocolDeposit.findByDate(date)
        valuation.protocol_deposit = pd.protocol_deposit_amount

        pd_revenue = pd.protocol_deposit_revenue

        # 货基
        mf = MoneyFund.findByDate(date)
        valuation.money_fund = mf.money_fund_amount
        mf_revenue = mf.money_fund_revenue

        # 资管
        valuation.assert_mgt = 0.00
        am_revenue = 0.00

        # 总资产净值 = 现金 + 协存 + 货基 + 资管
        valuation.total_assert_net_value = valuation.cash \
                                           + valuation.protocol_deposit \
                                           + valuation.money_fund \
                                           + valuation.assert_mgt

        # 流动资产比例 = (现金 + 协存 + 货基)/总资产净值
        valuation.liquid_assert_ratio = (valuation.cash
                                         + valuation.protocol_deposit
                                         + valuation.money_fund) \
                                        / valuation.total_assert_net_value
        # 当日总收益 = 协存当日总收益 + 货基当日总收益 + 资管当日总收益
        valuation.today_total_revenue = pd_revenue \
                                        + mf_revenue \
                                        + am_revenue

        rate, duration = self.getFeeConstrant()

        valuation.fee_1 = valuation.total_assert_net_value * eval(rate[0].replace('%', '/100')) / duration[0]
        valuation.fee_2 = valuation.total_assert_net_value * eval(rate[1].replace('%', '/100')) / duration[1]
        valuation.fee_3 = valuation.total_assert_net_value * eval(rate[2].replace('%', '/100')) / duration[2]
        valuation.fee_4 = valuation.today_total_revenue \
                          - valuation.today_product_revenue \
                          - valuation.fee_1 \
                          - valuation.fee_2 \
                          - valuation.fee_3

        valuation.save()

        return valuation

    def getFeeConstrant(self):
        rate = ['0.02%', '0.30%', '0.04%']
        duration = ['360', '360', '365']
        return rate, duration

    def getTodayFee(self, date):
        v = Valuation.findByDate(date)
        if v is None:
            return '0', '0', '0', '0'
        else:
            return v.fee_1, v.fee_2, v.fee_3, v.fee_4

    # ----------------------------------------------------------------------

    def get_cash_detail_by_days(self, days):
        """
        获取现金明细
        :param days:获取days内的现金明细
        :return 现金明细的dict
        """
        return CashService.get_cash_detail_by_days(days)

    def add_cash_daily_data(self,draw_amount,draw_fee,deposit_amount,ret_amount):
        """
        增加现金明细记录
        :param draw_amount: 兑付
        :param draw_fee: 提取费用
        :param deposit_amount: 流入
        :param ret_amount:现金收入
        :return None 
        """
        CashService.add_cash_daily_data(draw_amount,draw_fee,deposit_amount,ret_amount)

    def get_agreement_detail_by_days(self,days=0):
        """
        获取协存明细记录
        :param days: 
        :return: 
        """
        return [{'rate': 0.035, 'asset_name': '浦发理财一号', 'cal_date': datetime.date(2017, 4, 20), 'cash_to_agreement': 20001.0, 'agreement_to_cash': 10001.0, 'ret_carry_principal': 1001.0, 'asset_ret': -1001.0, 'total_amount': 10000.0}]
        # return AssetService.get_agreement_detail_by_days(days)

    def get_fund_detail_by_days(self,days=0):
        """
        获取货基明细记录
        :param days: 
        :return: 
        """
        return [{'asset_name': '余额宝', 'cal_date': datetime.date(2017, 4, 20), 'cash_to_fund': 13009.0, 'fund_to_cash': 8011.0, 'asset_ret': 3005.0, 'ret_carry_cash': 1005.0, 'ret_not_carry': 2000.0, 'total_amount': 8003.0}]
        # return AssetService.get_fund_detail_by_days(days)

    def get_all_management_detail(self):
        """
        资管相关明细
        :return: 
        """
        return AssetService.get_all_management_detail()

