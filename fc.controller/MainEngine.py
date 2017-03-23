# encoding: UTF-8

from collections import OrderedDict
from datetime import datetime

from fcConstant import LOG_DB_NAME
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

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

        # MongoDB数据库相关
        self.dbClient = None  # MongoDB客户端对象

        # 调用一个个初始化函数
        self.initGateway()

        # 扩展模块
        # self.ctaEngine = CtaEngine(self, self.eventEngine)
        # self.drEngine = DrEngine(self, self.eventEngine)
        # self.rmEngine = RmEngine(self, self.eventEngine)

    # ----------------------------------------------------------------------
    def initGateway(self):
        """初始化接口对象"""
        # 用来保存接口对象的字典
        self.gatewayDict = OrderedDict()

        # 创建我们想要接入的接口对象
        # try:
        #     from okcoinGateway.okcoinGateway import OkcoinGateway
        #     self.addGateway(OkcoinGateway, 'OKCOIN')
        #     self.gatewayDict['OKCOIN'].setQryEnabled(True)
        # except Exception as e:
        #     print(e)

    # ----------------------------------------------------------------------
    def addGateway(self, gateway, gatewayName=None):
        """创建接口"""
        self.gatewayDict[gatewayName] = gateway(self.eventEngine, gatewayName)

    # ----------------------------------------------------------------------
    def connect(self, gatewayName):
        """连接特定名称的接口"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            gateway.connect()
        else:
            self.writeLog('接口不存在：%s' % gatewayName)

    # ----------------------------------------------------------------------
    def subscribe(self, subscribeReq, gatewayName):
        """订阅特定接口的行情"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            gateway.subscribe(subscribeReq)
        else:
            self.writeLog('接口不存在：%s' % gatewayName)

            # ----------------------------------------------------------------------

    def sendOrder(self, orderReq, gatewayName):
        """对特定接口发单"""
        # 如果风控检查失败则不发单
        if not self.rmEngine.checkRisk(orderReq):
            return ''

        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            return gateway.sendOrder(orderReq)
        else:
            self.writeLog('接口不存在：%s' % gatewayName)

            # ----------------------------------------------------------------------

    def cancelOrder(self, cancelOrderReq, gatewayName):
        """对特定接口撤单"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            gateway.cancelOrder(cancelOrderReq)
        else:
            self.writeLog('接口不存在：%s' % gatewayName)

            # ----------------------------------------------------------------------

    def qryAccont(self, gatewayName):
        """查询特定接口的账户"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            gateway.qryAccount()
        else:
            self.writeLog('接口不存在：%s' % gatewayName)

            # ----------------------------------------------------------------------

    def qryPosition(self, gatewayName):
        """查询特定接口的持仓"""
        if gatewayName in self.gatewayDict:
            gateway = self.gatewayDict[gatewayName]
            gateway.qryPosition()
        else:
            self.writeLog('接口不存在：%s' % gatewayName)

            # ----------------------------------------------------------------------

    def exit(self):
        """退出程序前调用，保证正常退出"""
        # 安全关闭所有接口
        for gateway in self.gatewayDict.values():
            gateway.close()

        # 停止事件引擎
        self.eventEngine.stop()

        # 停止数据记录引擎
        self.drEngine.stop()

        # 保存数据引擎里的合约数据到硬盘
        self.dataEngine.saveContracts()

    # ----------------------------------------------------------------------



    def getContract(self, vtSymbol):
        """查询合约"""
        return self.dataEngine.getContract(vtSymbol)

    # ----------------------------------------------------------------------
    def getAllContracts(self):
        """查询所有合约（返回列表）"""
        return self.dataEngine.getAllContracts()

    # ----------------------------------------------------------------------
    def getOrder(self, vtOrderID):
        """查询委托"""
        return self.dataEngine.getOrder(vtOrderID)

    # ----------------------------------------------------------------------
    def getAllWorkingOrders(self):
        """查询所有的活跃的委托（返回列表）"""
        return self.dataEngine.getAllWorkingOrders()

    # ----------------------------------------------------------------------
    def getAllGatewayNames(self):
        """查询引擎中所有可用接口的名称"""
        return self.gatewayDict.keys()




