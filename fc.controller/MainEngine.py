# encoding: UTF-8

from collections import OrderedDict
from datetime import datetime

from Cash import Cash
from ProtocolDeposit import ProtocolDeposit, PdProject, PdProjectList
from fcConstant import LOG_DB_NAME

from DataEngine import DataEngine
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

        # 创建数据引擎
        self.dataEngine = DataEngine(self.eventEngine)


        # 调用一个个初始化函数
        # self.initGateway()

        # 扩展模块
        # self.ctaEngine = CtaEngine(self, self.eventEngine)
        # self.drEngine = DrEngine(self, self.eventEngine)
        # self.rmEngine = RmEngine(self, self.eventEngine)

    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------

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

