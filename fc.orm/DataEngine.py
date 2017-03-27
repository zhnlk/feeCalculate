########################################################################
import shelve
from datetime import datetime

from pymongo.errors import ConnectionFailure
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker

from EventEngine import Event
from fcConstant import STATUS_ALLTRADED, LOG_DB_NAME
from fcConstant import STATUS_CANCELLED

from EventType import EVENT_CONTRACT, EVENT_LOG, EVENT_CASH
from EventType import EVENT_ORDER
from fcFunction import loadSqliteSetting
from fcGateway import FcLogData


class DataEngine(object):
    """数据引擎"""
    cashFileName = 'DataEngineFile.fc'

    # ----------------------------------------------------------------------

    def __init__(self, eventEngine):
        """Constructor"""
        self.eventEngine = eventEngine

        # 记录今日日期
        self.todayDate = datetime.now().strftime('%Y%m%d')

        # 保存合约详细信息的字典
        self.contractDict = {}

        # 保存委托数据的字典
        self.orderDict = {}

        # 保存活动委托数据的字典（即可撤销）
        self.workingOrderDict = {}

        # 读取保存在硬盘的合约数据
        # self.loadContracts()

        # 注册事件监听
        self.registerEvent()

    # ----------------------------------------------------------------------
    # def updateContract(self, event):
    #     """更新合约数据"""
    #     contract = event.dict_['data']
    #     self.contractDict[contract.vtSymbol] = contract
    #     self.contractDict[contract.symbol] = contract  # 使用常规代码（不包括交易所）可能导致重复

    # ----------------------------------------------------------------------
    # def getContract(self, vtSymbol):
    #     """查询合约对象"""
    #     try:
    #         return self.contractDict[vtSymbol]
    #     except KeyError:
    #         return None

    # ----------------------------------------------------------------------
    # def getAllContracts(self):
    #     """查询所有合约对象（返回列表）"""
    #     return self.contractDict.values()

    # ----------------------------------------------------------------------
    # def saveContracts(self):
    #     """保存所有合约对象到硬盘"""
    #     f = shelve.open(self.cashFileName)
    #     f['data'] = self.contractDict
    #     f.close()

    # ----------------------------------------------------------------------
    # def loadContracts(self):
    #     """从硬盘读取合约对象"""
    #     f = shelve.open(self.cashFileName)
    #     if 'data' in f:
    #         d = f['data']
    #         for key, value in d.items():
    #             self.contractDict[key] = value
    #     f.close()

    # ----------------------------------------------------------------------
    def updateCash(self, event):
        """更新现金明细数据"""
        print('data engine update cash')

    def updateOrder(self, event):
        """更新委托数据"""
        order = event.dict_['data']
        self.orderDict[order.vtOrderID] = order

        # 如果订单的状态是全部成交或者撤销，则需要从workingOrderDict中移除
        if order.status == STATUS_ALLTRADED or order.status == STATUS_CANCELLED:
            if order.vtOrderID in self.workingOrderDict:
                del self.workingOrderDict[order.vtOrderID]
        # 否则则更新字典中的数据
        else:
            self.workingOrderDict[order.vtOrderID] = order

    # ----------------------------------------------------------------------
    def getOrder(self, vtOrderID):
        """查询委托"""
        try:
            return self.orderDict[vtOrderID]
        except KeyError:
            return None

    # ----------------------------------------------------------------------
    def getAllWorkingOrders(self):
        """查询所有活动委托（返回列表）"""
        return self.workingOrderDict.values()

    # ----------------------------------------------------------------------
    def registerEvent(self):
        """注册事件监听"""
        self.eventEngine.register(EVENT_CASH, self.updateCash)
        # self.eventEngine.register(EVENT_CONTRACT, self.updateContract)
        self.eventEngine.register(EVENT_ORDER, self.updateOrder)

    def dbConnect(self):
        """连接MongoDB数据库"""
        # 读取sqlite3的设置
        try:
            SQLALCHEMY_DATABASE_URI, logging = loadSqliteSetting()
            engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
            DBSession = sessionmaker(bind=engine)
            self.session = DBSession()
            # 调用server_info查询服务器状态，防止服务器异常并未连接成功
            # self.dbClient.server_info()

            # self.writeLog('SqliteDB连接成功')
            print("SqliteDB连接成功")

            # 如果启动日志记录，则注册日志事件监听函数
            if logging:
                self.eventEngine.register(EVENT_LOG, self.dbLogging)

        except:
            print("SqliteDB连接失败")
            # self.writeLog('SqliteDB连接失败')

    # ----------------------------------------------------------------------
    def dbInsert(self, d):
        """向SqliteDB中插入数据，d是具体数据"""
        if self.session:
            # db = self.session[dbName]
            # collection = db[collectionName]
            # collection.insert_one(d)
            self.session.add(d)
            self.session.commit()
            self.session.close()
        else:
            self.writeLog('数据插入失败，SqliteDB没有连接')

    def getSeesion(self):
        return self.session

    def dbInsertList(self, dList):
        """向SqliteDB批量插入数据"""
        if self.session:
            self.session.add_all(dList)
            self.session.commit()
            self.session.close()
        else:
            self.writeLog('数据插入失败，SqliteDB没有连接')

    # ----------------------------------------------------------------------
    def dbQuery(self, d):
        """从SqliteDB中读取数据，d是查询要求"""
        if self.session:
            # db = self.session[dbName]
            # collection = db[collectionName]
            # cursor = collection.find(d)
            # if cursor:
            result = self.session.query(d).all()
            # for i in result:
            #     print(i)
            return result
            # else:
            #     return []
        else:
            self.writeLog('数据查询失败，SqliteDB没有连接')
            return []

    # ----------------------------------------------------------------------
    def dbUpdate(self, dbName, d, flt, upsert=False):
        """向SqliteDB中更新数据，d是具体数据，flt是过滤条件，upsert代表若无是否要插入"""
        if self.session:
            self.session.query()

        else:
            self.writeLog('数据更新失败，SqliteDB没有连接')

    # ----------------------------------------------------------------------
    def dbDelete(self, d):
        if self.session:
            self.session.delete(d)
        else:
            self.writeLog('数据删除失败，SqliteDB没有连接')

    def dbLogging(self, event):
        """向MongoDB中插入日志"""
        log = event.dict_['data']
        d = {
            'content': log.logContent,
            'time': log.logTime,
            'gateway': log.gatewayName
        }
        # self.dbInsert(LOG_DB_NAME, self.todayDate, d)

    # ----------------------------------------------------------------------
    def writeLog(self, content):
        """快速发出日志事件"""
        log = FcLogData()
        log.logContent = content
        event = Event(type_=EVENT_LOG)
        event.dict_['data'] = log
        self.eventEngine.put(event)

        # ----------------------------------------------------------------------
