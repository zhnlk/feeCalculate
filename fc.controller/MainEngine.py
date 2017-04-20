# encoding: UTF-8
from datetime import datetime

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
        self.todayDate = datetime.now().strftime('%Y%m%d')

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
        return v.fee_1, v.fee_2, v.fee_3,v.fee_4

    # ----------------------------------------------------------------------
    def getCashDetail(self):
        """查询现金明细"""
        detail = Cash.listAll()
        # 计算每日的现金明细
        for d in detail:
            d.total_cash = d.getTodayTotalCash(d.date)
            # 计算协存与货基的相关数据
            d.getRelatedData()

            print(d.__dict__)
            d.save()
        print('get Cash Detail')
        return detail

    def getProtocolDeposit(self, date):
        """查询协存汇总"""
        pd = ProtocolDeposit(date)

        # protocolDepositList = PdProjectList.listByDate(date)
        # for p in protocolDepositList:
        #     pd.protocol_deposit_amount += p.pd_amount
        #     pd.protocol_deposit_revenue += p.pd_interest
        #     pd.cash_to_protocol_deposit += p.pd_cash_to_pd
        #     pd.protocol_deposit_to_cash += p.pd_pd_to_cash
        pd.save()

        return pd

    def getProtocolDetail(self):
        """查询协存"""
        detail = PdProject.listAll()
        for d in detail:
            print('getProtocolDetail' + d.uuid)
        return detail

    def getProtocolListDetail(self):
        """查询协存列表明细"""
        detail = PdProjectList.listAll()
        for d in detail:
            self.getProtocolDeposit(d.date)
            print('getProtocolListDetail.........' + d.uuid)
        return detail

    def getMoneyFundDetail(self):
        """查询货基列表明细"""
        detail = MfProjectList.listAll()
        for m in detail:
            print('getMoneyFundListDetail' + m.uuid)
        return detail

    def getMoneyFundSummary(self, date):
        res = MfProjectList.listAllForSummary(date)
        for r in res:
            print(r[0], r[1], r[2], r[3])
        return res
