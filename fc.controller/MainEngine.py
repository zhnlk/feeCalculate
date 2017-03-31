# encoding: UTF-8
import json
from collections import OrderedDict
from datetime import datetime

from Cash import Cash
from MoneyFund import MfProjectList
from ProtocolDeposit import ProtocolDeposit, PdProject, PdProjectList
from fcConstant import LOG_DB_NAME

from EventEngine import *


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
        for d in detail:
            d.total_cash = d.getTodayTotalCash()
        print('get Cash Detail')
        return detail

    def getProtocolDeposit(self):
        """查询协存汇总"""

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
            print('getProtocolListDetail' + d.uuid)
        return detail

    def getMoneyFundDetail(self):
        """查询货基列表明细"""
        detail = MfProjectList.listAll()
        for m in detail:
            print('getMoneyFundListDetail' + m.uuid)
        return detail


