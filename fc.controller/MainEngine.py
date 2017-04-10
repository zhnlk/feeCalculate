# encoding: UTF-8
from datetime import datetime

from Cash import Cash
from EventEngine import *
from MoneyFund import MfProjectList
from ProtocolDeposit import PdProject, PdProjectList, ProtocolDeposit


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

    # ----------------------------------------------------------------------
    def getCashDetail(self):
        """查询现金明细"""
        detail = Cash.listAll()
        # 计算每日的现金明细
        for d in detail:
            d.total_cash = d.getTodayTotalCash(d.date)
            # 计算协存与货基的相关数据
            d.getRelatedData()
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


