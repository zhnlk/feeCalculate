# -*- coding: utf-8 -*-
from collections import OrderedDict

from PyQt5 import QtCore
from asyncio import Event

import psutil as psutil
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

from BasicWidget import BasicCell, BasicFcView, BASIC_FONT
from EventType import EVENT_TICK
from assertmgtView.AssertMgtMain import AssertMgtListView
from cashView.CashInput import CashInput
from cashView.CashMain import CashListView
from miscView.AboutMain import AboutWidget
from moneyfundView.MfCateInput import MfCateInput
from moneyfundView.MoneyFundInput import MoneyFundInput
from moneyfundView.MoneyFundMain import MoneyFundListView
from protocolView.PdCateInput import PdCateInput
from protocolView.ProtocolInput import ProtocolInput
from protocolView.ProtocolMain import ProtocolListView


class MainWindow(QMainWindow, BasicFcView):
    """主窗口"""
    signalStatusBar = pyqtSignal(type(Event()))

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine):
        """Constructor"""
        super(MainWindow, self).__init__()

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        self.widgetDict = {}  # 用来保存子窗口的字典

        self.initUi()
        self.loadWindowSettings('custom')

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('feeCalc')
        self.initCentral()
        self.initTopMenu()
        self.initStatusBar()

    # ----------------------------------------------------------------------
    def initCentral(self):
        """总估值与费用"""

        # 增加主界面显示
        widgetMainView, dockMainView = self.createDock(DateMainView, '今日资金成本', QtCore.Qt.LeftDockWidgetArea)
        widgetMainView, dockMainView = self.createDock(FeeTotalView, '费用详情统计', QtCore.Qt.RightDockWidgetArea)
        widgetMainView, dockMainView = self.createDock(AssertTotalView, '存量资产详情', QtCore.Qt.BottomDockWidgetArea)
        # self.tabifyDockWidget(widgetMainView,dockMainView)

        dockMainView.raise_()

        # 保存默认设置
        self.saveWindowSettings('default')

    # ----------------------------------------------------------------------
    def initTopMenu(self):
        """初始化菜单"""
        # 创建菜单
        menubar = self.menuBar()

        # 设计为只显示存在的接口
        sysMenu = menubar.addMenu('系统')
        # sysMenu.addAction(self.createAction('增加大类产品(暂未支持)',self.openAddCate))
        sysMenu.addAction(self.createAction('退出', self.close))
        sysMenu.addSeparator()

        cashDetailMenu = menubar.addMenu('现金明细')
        cashDetailMenu.addAction(self.createAction('显示明细', self.openCashListDetail))
        cashDetailMenu.addAction(self.createAction('增加记录', self.openAddCashDetail))
        # cashDetailMenu.addAction(self.createAction('导出数据', self.openOutCashData))
        sysMenu.addSeparator()
        # 协议存款
        protocolMenu = menubar.addMenu('协议存款')
        protocolMenu.addAction(self.createAction('显示明细', self.openProtocolListDetail))
        protocolMenu.addAction(self.createAction('增加记录', self.openAddProtocolDetail))
        protocolMenu.addAction(self.createAction('增加协存类别', self.openAddProtocolCate))
        # protocolMenu.addAction(self.createAction('导出记录', self.openOutProtocolData))
        sysMenu.addSeparator()
        # 货基
        moneyFundMenu = menubar.addMenu('货基明细')
        moneyFundMenu.addAction(self.createAction('显示明细', self.openMoneyFundListDetail))
        moneyFundMenu.addAction(self.createAction('增加记录', self.openAddMoneyFundDetail))
        moneyFundMenu.addAction(self.createAction('增加货基类别', self.openAddMoneyFundCate))
        # moneyFundMenu.addAction(self.createAction('导出记录', self.openOutMoneFundData))
        sysMenu.addSeparator()
        # 资管
        assertMgtMenu = menubar.addMenu('资管明细')
        assertMgtMenu.addAction(self.createAction('显示明细', self.openAssertMgtListDetail))
        assertMgtMenu.addAction(self.createAction('增加记录', self.oepnAddAssertMgtDetail))
        # assertMgtMenu.addAction(self.createAction('导出记录', self.openOutAssertMgtData))
        sysMenu.addSeparator()
        # 帮助
        helpMenu = menubar.addMenu('帮助')
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
    def openAbout(self):
        """打开关于"""
        try:
            self.widgetDict['aboutW'].show()
        except KeyError:
            self.widgetDict['aboutW'] = AboutWidget(self)
            self.widgetDict['aboutW'].show()

    # ----------------------------------------------------------------------

    def openCashListDetail(self):
        """打开现金明细"""
        try:
            self.widgetDict['showCashListDetail'].show()
        except KeyError:
            self.widgetDict['showCashListDetail'] = CashListView(self.mainEngine)
            self.widgetDict['showCashListDetail'].show()

    def openProtocolListDetail(self):
        """打开协存明细"""
        try:
            self.widgetDict['openProtocolListDetail'].show()
        except KeyError:
            self.widgetDict['openProtocolListDetail'] = ProtocolListView(self.mainEngine)
            self.widgetDict['openProtocolListDetail'].show()

    def openMoneyFundListDetail(self):
        """打开货基明细"""
        try:
            self.widgetDict['openMoneyFundListDetail'].show()
        except KeyError:
            self.widgetDict['openMoneyFundListDetail'] = MoneyFundListView(self.mainEngine)
            self.widgetDict['openMoneyFundListDetail'].show()

    def openAssertMgtListDetail(self):
        """打开资管明细"""
        try:
            self.widgetDict['openAssertMgtListDetail'].show()
        except KeyError:
            self.widgetDict['openAssertMgtListDetail'] = AssertMgtListView(self.mainEngine)
            self.widgetDict['openAssertMgtListDetail'].show()

    def openAddCashDetail(self):
        """打开现金输入界面"""
        try:
            self.widgetDict['addCashDetail'].show()
        except KeyError:
            self.widgetDict['addCashDetail'] = CashInput(self.mainEngine)
            self.widgetDict['addCashDetail'].show()
    def openAddProtocolDetail(self):
        """打开协存输入界面"""
        try:
            self.widgetDict['openAddProtocolDetail'].show()
        except KeyError:
            self.widgetDict['openAddProtocolDetail'] = ProtocolInput(self.mainEngine)
            self.widgetDict['openAddProtocolDetail'].show()

    def openAddProtocolCate(self):
        """增加协存类别增加界面"""
        try:
            self.widgetDict['openAddProtocolCate'].show()
        except KeyError:
            self.widgetDict['openAddProtocolCate'] = PdCateInput(self.mainEngine)
            self.widgetDict['openAddProtocolCate'].show()

    def openAddMoneyFundDetail(self):
        """打开货基输入界面"""
        try:
            self.widgetDict['openAddMoneyFundDetail'].show()
        except KeyError:
            self.widgetDict['openAddMoneyFundDetail'] = MoneyFundInput(self.mainEngine)
            self.widgetDict['openAddMoneyFundDetail'].show()
    def openAddMoneyFundCate(self):
        """打开货基类别增加界面"""
        try:
            self.widgetDict['openAddMoneyFundCate'].show()
        except KeyError:
            self.widgetDict['openAddMoneyFundCate'] = MfCateInput(self.mainEngine)
            self.widgetDict['openAddMoneyFundCate'].show()

    def oepnAddAssertMgtDetail(self):
        """打开资管输入界面"""
        try:
            self.widgetDict['oepnAddAssertMgtDetail'].show()
        except KeyError:
            self.widgetDict['oepnAddAssertMgtDetail'] = CashListView(self.mainEngine)
            self.widgetDict['oepnAddAssertMgtDetail'].show()

    # ----------------------------------------------------------------------
    def openOutCashData(self):
        """打开现金导出"""
        try:
            self.widgetDict['OutCashData'].show()
        except KeyError:
            self.widgetDict['OutCashData'] = CashListView(self.mainEngine)
            self.widgetDict['OutCashData'].show()

    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    def createAction(self, actionName, function):
        """创建操作功能"""
        action = QAction(actionName, self)
        # action.triggered.connect(self.close)
        action.triggered.connect(function)
        return action

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

    def createDock(self, widgetClass, widgetName, widgetArea):
        """创建停靠组件"""
        widget = widgetClass(self.mainEngine, self.eventEngine)
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


class DateMainView(BasicFcView):
    """"""

    def __init__(self, mainEngine, eventEngine, parant=None):
        """Constructor"""
        super(DateMainView, self).__init__(mainEngine, eventEngine, parant)
        # 设置表头有序字典
        d = OrderedDict()
        d['date'] = {'chinese': '填表日', 'cellType': BasicCell}
        d['total_assert'] = {'chinese': '计算日', 'cellType': BasicCell}
        d['cash'] = {'chinese': '今日资金成本', 'cellType': BasicCell}

        self.setHeaderDict(d)
        # 设置数据键
        self.setDataKey('fcSymbol')

        # 设置监控事件类型
        self.setEventType(EVENT_TICK)

        # 设置字体
        self.setFont(BASIC_FONT)

        # 设置允许排序
        self.setSorting(True)

        # 初始化表格
        self.initTable()

        # 注册事件监听
        self.registerEvent()


class FeeTotalView(BasicFcView):
    """"""

    def __init__(self, mainEngine, eventEngine, parant=None):
        """Constructor"""
        super(FeeTotalView, self).__init__(mainEngine, eventEngine, parant)
        # 设置表头有序字典
        d = OrderedDict()
        d['date'] = {'chinese': '--', 'cellType': BasicCell}
        d['fee_1'] = {'chinese': '费用1', 'cellType': BasicCell}
        d['fee_2'] = {'chinese': '费用2', 'cellType': BasicCell}
        d['fee_3'] = {'chinese': '费用3', 'cellType': BasicCell}
        d['fee_4'] = {'chinese': '超额费用', 'cellType': BasicCell}

        self.setHeaderDict(d)
        # 设置数据键
        self.setDataKey('fcSymbol')

        # 设置监控事件类型
        self.setEventType(EVENT_TICK)

        # 设置字体
        self.setFont(BASIC_FONT)

        # 设置允许排序
        self.setSorting(True)

        # 初始化表格
        self.initTable()

        # 注册事件监听
        self.registerEvent()


class AssertTotalView(BasicFcView):
    """主界面"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine, parent=None):
        """Constructor"""
        super(AssertTotalView, self).__init__(mainEngine, eventEngine, parent)

        # 设置表头有序字典
        d = OrderedDict()
        d['date'] = {'chinese': '存量资产详情', 'cellType': BasicCell}
        d['total_assert'] = {'chinese': '--', 'cellType': BasicCell}
        d['cash'] = {'chinese': '--', 'cellType': BasicCell}
        d['money_fund'] = {'chinese': '比例', 'cellType': BasicCell}
        d['assert_mgt'] = {'chinese': '净值/价格', 'cellType': BasicCell}
        d['liquid_assert_ratio'] = {'chinese': '份额', 'cellType': BasicCell}
        d['today_total_revenue'] = {'chinese': '金额', 'cellType': BasicCell}
        d['fee_1'] = {'chinese': '本金', 'cellType': BasicCell}
        d['fee_2'] = {'chinese': '累计收益', 'cellType': BasicCell}
        d['fee_3'] = {'chinese': '今日收益', 'cellType': BasicCell}

        self.setHeaderDict(d)
        # 设置数据键
        self.setDataKey('fcSymbol')

        # 设置监控事件类型
        self.setEventType(EVENT_TICK)

        # 设置字体
        self.setFont(BASIC_FONT)

        # 设置允许排序
        self.setSorting(True)

        # 初始化表格
        self.initTable()

        # 注册事件监听
        self.registerEvent()
