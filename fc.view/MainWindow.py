# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from asyncio import Event

import psutil as psutil
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QVBoxLayout

from BasicWidget import AddCashDetail, OutPutData


class MainWindow(QMainWindow):
    """主窗口"""
    signalStatusBar = pyqtSignal(type(Event()))

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(MainWindow, self).__init__()

        self.widgetDict = {}  # 用来保存子窗口的字典

        self.initUi()
        self.loadWindowSettings('custom')

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('feeCalc')
        # self.initCentral()
        self.initMenu()
        self.initStatusBar()

    # ----------------------------------------------------------------------
    def initCentral(self):
        """初始化中心区域"""
        # widgetMarketM, dockMarketM = self.createDock(MarketMonitor, u'行情', QtCore.Qt.RightDockWidgetArea)
        # widgetLogM, dockLogM = self.createDock(LogMonitor, u'日志', QtCore.Qt.BottomDockWidgetArea)
        # widgetErrorM, dockErrorM = self.createDock(ErrorMonitor, u'错误', QtCore.Qt.BottomDockWidgetArea)
        # widgetTradeM, dockTradeM = self.createDock(TradeMonitor, u'成交', QtCore.Qt.BottomDockWidgetArea)
        # widgetOrderM, dockOrderM = self.createDock(OrderMonitor, u'委托', QtCore.Qt.RightDockWidgetArea)
        # widgetPositionM, dockPositionM = self.createDock(PositionMonitor, u'持仓', QtCore.Qt.BottomDockWidgetArea)
        # widgetAccountM, dockAccountM = self.createDock(AccountMonitor, u'资金', QtCore.Qt.BottomDockWidgetArea)
        # widgetTradingW, dockTradingW = self.createDock(TradingWidget, u'交易', QtCore.Qt.LeftDockWidgetArea)

        # self.tabifyDockWidget(dockTradeM, dockErrorM)
        # self.tabifyDockWidget(dockTradeM, dockLogM)
        # self.tabifyDockWidget(dockPositionM, dockAccountM)

        # dockTradeM.raise_()
        # dockPositionM.raise_()

        # 连接组件之间的信号
        # widgetPositionM.itemDoubleClicked.connect(widgetTradingW.closePosition)

        # 保存默认设置
        self.saveWindowSettings('default')

    # ----------------------------------------------------------------------
    def initMenu(self):
        """初始化菜单"""
        # 创建菜单
        menubar = self.menuBar()

        # 设计为只显示存在的接口
        sysMenu = menubar.addMenu(u'系统')

        sysMenu.addSeparator()
        sysMenu.addAction(self.createAction(u'退出', self.close))

        cashDetailMenu = menubar.addMenu('现金明细')
        cashDetailMenu.addAction(self.createAction('增加记录', self.openAddCashDetail))
        cashDetailMenu.addAction(self.createAction('导出数据', self.openOutPutData))

        # 协议存款
        protocolMenu = menubar.addMenu('协议存款')
        protocolMenu.addAction(self.createAction('CTA策略', self.openCta))
        # protocolMenu.addAction()

        # 货基
        moneyFundMenu = menubar.addMenu('货基明细')
        moneyFundMenu.addAction(self.createAction('关于', self.openAbout))

        # 资管
        assertMgtMenu = menubar.addMenu('资管明细')
        assertMgtMenu.addAction(self.createAction('关于', self.openAbout))

        # 帮助
        helpMenu = menubar.addMenu(u'帮助')
        helpMenu.addAction(self.createAction('关于', self.openAbout))

    # ----------------------------------------------------------------------
    def initStatusBar(self):
        """初始化状态栏"""
        self.statusLabel = QLabel()
        self.statusLabel.setAlignment(QtCore.Qt.AlignLeft)

        self.statusBar().addPermanentWidget(self.statusLabel)
        self.statusLabel.setText(self.getCpuMemory())

        self.sbCount = 0
        self.sbTrigger = 10  # 10秒刷新一次
        self.signalStatusBar.connect(self.updateStatusBar)
        # self.eventEngine.register(EVENT_TIMER, self.signalStatusBar.emit)

    # ----------------------------------------------------------------------
    def updateStatusBar(self, event):
        """在状态栏更新CPU和内存信息"""
        self.sbCount += 1

        if self.sbCount == self.sbTrigger:
            self.sbCount = 0
            self.statusLabel.setText(self.getCpuMemory())

    # ----------------------------------------------------------------------
    def getCpuMemory(self):
        """获取CPU和内存状态信息"""
        cpuPercent = psutil.cpu_percent()
        memoryPercent = psutil.virtual_memory().percent
        return u'CPU使用率：%d%%   内存使用率：%d%%' % (cpuPercent, memoryPercent)

        # ----------------------------------------------------------------------

    def addConnectAction(self, menu, gatewayName, displayName=''):
        """增加连接功能"""

        # if gatewayName not in self.mainEngine.getAllGatewayNames():
        #     return

        def connect():
            pass
            # self.mainEngine.connect(gatewayName)

        if not displayName:
            displayName = gatewayName
        actionName = u'连接' + displayName

        menu.addAction(self.createAction(actionName, connect))

    # ----------------------------------------------------------------------
    def createAction(self, actionName, function):
        """创建操作功能"""
        action = QAction(actionName, self)
        action.triggered.connect(function)
        return action

    # ----------------------------------------------------------------------
    def openAbout(self):
        """打开关于"""
        try:
            self.widgetDict['aboutW'].show()
        except KeyError:
            self.widgetDict['aboutW'] = AboutWidget(self)
            self.widgetDict['aboutW'].show()

    # ----------------------------------------------------------------------
    def openContract(self):
        """打开合约查询"""
        try:
            self.widgetDict['contractM'].show()
        except KeyError:
            # self.widgetDict['contractM'] = ContractMonitor(self.mainEngine)
            self.widgetDict['contractM'].show()


    def openAddCashDetail(self):
        """打开现金明细"""
        try:
            self.widgetDict['addCashDetail'].show()
        except KeyError:
            self.widgetDict['addCashDetail'] = AddCashDetail()
            self.widgetDict['addCashDetail'].show()

    # ----------------------------------------------------------------------
    def openOutPutData(self):
        """打开导出数据"""
        try:
            self.widgetDict['outPutData'].show()
        except KeyError:
            self.widgetDict['outPutData'] = OutPutData()
            self.widgetDict['outPutData'].show()

    def openCta(self):
        """打开CTA组件"""
        try:
            self.widgetDict['ctaM'].showMaximized()
        except KeyError:
            # self.widgetDict['ctaM'] = CtaEngineManager(self.mainEngine.ctaEngine, self.eventEngine)
            self.widgetDict['ctaM'].showMaximized()

    # ----------------------------------------------------------------------
    def openDr(self):
        """打开行情数据记录组件"""
        try:
            self.widgetDict['drM'].showMaximized()
        except KeyError:
            # self.widgetDict['drM'] = DrEngineManager(self.mainEngine.drEngine, self.eventEngine)
            self.widgetDict['drM'].showMaximized()

    # ----------------------------------------------------------------------
    def openRm(self):
        """打开组件"""
        try:
            self.widgetDict['rmM'].show()
        except KeyError:
            # self.widgetDict['rmM'] = RmEngineManager(self.mainEngine.rmEngine, self.eventEngine)
            self.widgetDict['rmM'].show()

            # ----------------------------------------------------------------------

    def closeEvent(self, event):
        """关闭事件"""
        reply = QMessageBox.question(self, '退出', '确认退出?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            for widget in self.widgetDict.values():
                widget.close()
            self.saveWindowSettings('custom')

            # self.mainEngine.exit()
            event.accept()
        else:
            event.ignore()

    # ----------------------------------------------------------------------
    def createDock(self, widgetClass, widgetName, widgetArea):
        """创建停靠组件"""
        # widget = widgetClass(self.mainEngine, self.eventEngine)
        widget = widgetClass()
        dock = QDockWidget(widgetName)
        dock.setWidget(widget)
        dock.setObjectName(widgetName)
        dock.setFeatures(dock.DockWidgetFloatable | dock.DockWidgetMovable)
        self.addDockWidget(widgetArea, dock)
        return widget, dock

    # ----------------------------------------------------------------------
    def saveWindowSettings(self, settingName):
        """保存窗口设置"""
        settings = QSettings('vn.trader', settingName)
        settings.setValue('state', self.saveState())
        settings.setValue('geometry', self.saveGeometry())

    # ----------------------------------------------------------------------
    def loadWindowSettings(self, settingName):
        """载入窗口设置"""
        settings = QSettings('vn.trader', settingName)
        # 这里由于PyQt4的版本不同，settings.value('state')调用返回的结果可能是：
        # 1. None（初次调用，注册表里无相应记录，因此为空）
        # 2. QByteArray（比较新的PyQt4）
        # 3. QVariant（以下代码正确执行所需的返回结果）
        # 所以为了兼容考虑，这里加了一个try...except，如果是1、2的情况就pass
        # 可能导致主界面的设置无法载入（每次退出时的保存其实是成功了）
        try:
            self.restoreState(settings.value('state').toByteArray())
            self.restoreGeometry(settings.value('geometry').toByteArray())
        except AttributeError:
            pass

    # ----------------------------------------------------------------------
    def restoreWindow(self):
        """还原默认窗口设置（还原停靠组件位置）"""
        self.loadWindowSettings('default')
        self.showMaximized()
        ########################################################################


class AboutWidget(QDialog):
    """显示关于信息"""

    # ----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(AboutWidget, self).__init__(parent)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """"""
        self.setWindowTitle('About Fee Calculate')

        text = """
                Developed by zhnlk.

                License：MIT

                Mail：yanan.zhang@creditcloud.com

                Github：www.github.com/zhnlk

                """

        label = QLabel()
        label.setText(text)
        label.setMinimumWidth(500)

        vbox = QVBoxLayout()
        vbox.addWidget(label)

        self.setLayout(vbox)


