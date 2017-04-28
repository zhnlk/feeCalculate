# -*- coding: utf-8 -*-
from collections import OrderedDict

import datetime
from PyQt5 import QtCore
from asyncio import Event

import psutil as psutil
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction, QApplication
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

import EventType
from BasicWidget import BasicCell, BasicFcView, BASIC_FONT
from MainEngine import MainEngine
from assertmgtView.AdjustValuationView import AdjustValuationView
from assertmgtView.AssetMgtAdjustInput import AdjustValuationInput
from assertmgtView.AssetMgtInput import AssetMgtInput
from assertmgtView.AssetMgtMain import AssetMgtListView
from cashView.CashInput import CashInput
from cashView.CashMain import CashListView
from miscView.AboutMain import AboutWidget
from miscView.ErrorMain import ErrorWidget
from moneyfundView.MfCateInput import MfCateInput
from moneyfundView.MoneyFundInput import MoneyFundInput
from moneyfundView.MoneyFundMain import MoneyFundMain
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
        widgetMainView1, dockMainView1 = self.createDock(DateMainView, '今日资金成本', QtCore.Qt.LeftDockWidgetArea)
        widgetMainView2, dockMainView2 = self.createDock(FeeTotalView, '费用详情统计', QtCore.Qt.RightDockWidgetArea)
        widgetMainView3, dockMainView3 = self.createDock(AssertTotalView, '存量资产详情', QtCore.Qt.BottomDockWidgetArea)
        widgetMainView4, dockMainView4 = self.createDock(TotalValuationView, '总估值表', QtCore.Qt.BottomDockWidgetArea)
        self.tabifyDockWidget(dockMainView3, dockMainView4)

        # dockMainView.raise_()

    # ----------------------------------------------------------------------
    def initTopMenu(self):
        """初始化菜单"""
        # 创建菜单
        menubar = self.menuBar()

        # 设计为只显示存在的接口
        sysMenu = menubar.addMenu('系统')
        sysMenu.addAction(self.createAction('退出', self.close))
        sysMenu.addSeparator()

        cashDetailMenu = menubar.addMenu('现金明细')
        cashDetailMenu.addAction(self.createAction('显示明细', self.openCashListDetail))
        cashDetailMenu.addAction(self.createAction('增加记录', self.openAddCashDetail))
        cashDetailMenu.addAction(self.createAction('导出数据', self.openOutCashData))
        sysMenu.addSeparator()
        # 协议存款
        protocolMenu = menubar.addMenu('协议存款')
        protocolMenu.addAction(self.createAction('显示明细', self.openProtocolListDetail))
        protocolMenu.addAction(self.createAction('增加记录', self.openAddProtocolDetail))
        protocolMenu.addAction(self.createAction('增加协存类别', self.openAddProtocolCate))
        protocolMenu.addAction(self.createAction('导出记录', self.openOutProtocolData))
        sysMenu.addSeparator()
        # 货基
        moneyFundMenu = menubar.addMenu('货基明细')
        moneyFundMenu.addAction(self.createAction('显示明细', self.openMoneyFundListDetail))
        moneyFundMenu.addAction(self.createAction('增加记录', self.openAddMoneyFundDetail))
        moneyFundMenu.addAction(self.createAction('增加货基类别', self.openAddMoneyFundCate))
        moneyFundMenu.addAction(self.createAction('导出记录', self.openOutMoneFundData))
        sysMenu.addSeparator()
        # 资管
        assertMgtMenu = menubar.addMenu('资管明细')
        assertMgtMenu.addAction(self.createAction('显示明细', self.openAssetMgtListDetail))
        assertMgtMenu.addAction(self.createAction('资管估值调整', self.oepnAdjustValuation))
        assertMgtMenu.addAction(self.createAction('增加资管类别', self.openAddAssetMgtCate))
        assertMgtMenu.addAction(self.createAction('导出记录', self.openOutAssetMgtData))
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
            self.widgetDict['openMoneyFundListDetail'] = MoneyFundMain(self.mainEngine)
            self.widgetDict['openMoneyFundListDetail'].show()

    def openAssetMgtListDetail(self):
        """打开资管明细"""
        try:
            self.widgetDict['openAssetMgtListDetail'].show()
        except KeyError:
            self.widgetDict['openAssetMgtListDetail'] = AssetMgtListView(self.mainEngine)
            self.widgetDict['openAssetMgtListDetail'].show()

    def oepnAdjustValuation(self):
        """资管估值调整"""
        try:
            self.widgetDict['oepnAdjustValuationInput'].show()
        except KeyError:
            self.widgetDict['oepnAdjustValuationInput'] = AdjustValuationInput(self.mainEngine)
            self.widgetDict['oepnAdjustValuationInput'].show()

    def openAddAssetMgtCate(self):
        """增加资管类别"""
        try:
            self.widgetDict['openAddAssetMgtCate'].show()
        except KeyError:
            self.widgetDict['openAddAssetMgtCate'] = AssetMgtInput(self.mainEngine)
            self.widgetDict['openAddAssetMgtCate'].show()

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

    def openOutProtocolData(self):
        try:
            self.widgetDict['openOutProtocolData'].show()
        except KeyError:
            self.widgetDict['openOutProtocolData'] = ErrorWidget(self)
            self.widgetDict['openOutProtocolData'].show()

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

    def openOutMoneFundData(self):
        try:
            self.widgetDict['openOutMoneFundData'].show()
        except KeyError:
            self.widgetDict['openOutMoneFundData'] = ErrorWidget(self)
            self.widgetDict['openOutMoneFundData'].show()

    def openOutAssetMgtData(self):
        try:
            self.widgetDict['openOutAssetMgtData'].show()
        except KeyError:
            self.widgetDict['openOutAssetMgtData'] = ErrorWidget(self)
            self.widgetDict['openOutAssetMgtData'].show()

    # ----------------------------------------------------------------------
    def openOutCashData(self):
        """打开现金导出"""
        try:
            self.widgetDict['OutCashData'].show()
        except KeyError:
            self.widgetDict['OutCashData'] = ErrorWidget(self)
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

            self.mainEngine.exit()
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
    def loadWindowSettings(self, settingName):
        """载入窗口设置"""
        settings = QSettings('vn.trader', settingName)
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

        self.setEventType(EventType.EVENT_MAIN_COST)

        # 设置字体
        # self.setFont(BASIC_FONT)

        # 设置允许排序
        self.setSorting(True)

        # 界面初始化
        self.initUI()

        # 注册事件监听
        self.registerEvent()

    def initUI(self):
        # 初始化表格
        self.initTable()
        self.refresh()

    def refresh(self):
        self.initData()

    def initData(self):
        """初始化数据"""
        result = self.mainEngine.getMainCostData()
        self.setRowCount(1)
        row = 0
        self.setItem(0, 0, BasicCell(result[0]))
        self.setItem(0, 1, BasicCell(result[1]))
        self.setItem(0, 2, BasicCell(result[2]))
        # for r in result:
        #     # 按照定义的表头，进行数据填充
        #     for n, header in enumerate(self.headerList):
        #         content = r[n]
        #         cellType = self.headerDict[header]['cellType']
        #         cell = cellType(content)
        #         print(cell.text())
        #         self.setItem(row, n, cell)
        #     row = row + 1


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

        self.setEventType(EventType.EVENT_MAIN_FEE)

        # 设置字体
        # self.setFont(BASIC_FONT)

        # 设置允许排序
        self.setSorting(True)

        # 初始化表格
        self.initUI()

        # 注册事件监听
        self.registerEvent()

    def initUI(self):
        # 初始化表格
        self.initTable()
        self.refresh()

    def refresh(self):
        self.initData()
        # pass

    def initData(self):
        """初始化数据"""
        rate, duration = self.mainEngine.getFeeConstrant()
        self.setRowCount(3)

        self.setItem(0, 0, BasicCell('费率'))
        self.setItem(1, 0, BasicCell('计算天数'))
        self.setItem(2, 0, BasicCell('今日费用'))
        c = 1
        for r in rate:
            self.setItem(0, c, BasicCell(r))
            c += 1
        c = 1
        for d in duration:
            self.setItem(1, c, BasicCell(d))
            c += 1
        date = datetime.date(2017, 3, 10)
        todayFee = self.mainEngine.getTodayFee(date)
        c = 1
        for tf in todayFee:
            self.setItem(2, c, BasicCell(tf))
            c += 1


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
        self.setEventType(EventType.EVENT_MAIN_ASSERT_DETAIL)

        # 设置字体
        # self.setFont(BASIC_FONT)

        # 设置允许排序
        self.setSorting(True)

        # 初始化表格
        self.initTable()

        # 注册事件监听
        self.registerEvent()


class TotalValuationView(BasicFcView):
    """总估值表"""

    def __init__(self, mainEngine, eventEngine, parent=None):
        super(TotalValuationView, self).__init__(mainEngine, eventEngine, parent)

        # 设置表头有序字典
        d = OrderedDict()
        d['cal_date'] = {'chinese': '计算日', 'cellType': BasicCell}
        d['all_value'] = {'chinese': '总资产净值', 'cellType': BasicCell}
        d['cash'] = {'chinese': '现金', 'cellType': BasicCell}
        d['agreement'] = {'chinese': '协存', 'cellType': BasicCell}
        d['fund'] = {'chinese': '货币基金', 'cellType': BasicCell}
        d['management'] = {'chinese': '资管', 'cellType': BasicCell}
        # d['liquid_assert_ratio'] = {'chinese': '流动资产比例', 'cellType': BasicCell}
        d['all_ret'] = {'chinese': '当日总收益', 'cellType': BasicCell}
        d['fee1'] = {'chinese': '费用1', 'cellType': BasicCell}
        d['fee2'] = {'chinese': '费用2', 'cellType': BasicCell}
        d['fee3'] = {'chinese': '费用3', 'cellType': BasicCell}
        # d['fee_4'] = {'chinese': '费用4', 'cellType': BasicCell}
        # d['today_product_revenue'] = {'chinese': '当日产品收益', 'cellType': BasicCell}
        # d['fee_accual'] = {'chinese': '费用计提', 'cellType': BasicCell}

        self.setHeaderDict(d)
        self.setDataKey('fcSymbol')

        self.setEventType(EventType.EVENT_MAIN_VALUATION)

        # self.setFont(BASIC_FONT)

        self.setSorting(True)

        self.initUI()

        self.registerEvent()

    def initUI(self):
        # 初始化表格
        self.initTable()
        self.refresh()
        self.addPopAction()

    def refresh(self):
        self.initData()
        # pass

    def addPopAction(self):
        """增加右键菜单内容"""
        refreshAction = QAction('刷新', self)
        refreshAction.triggered.connect(self.refresh)

        self.menu.addAction(refreshAction)

    def initData(self):
        """初始化数据"""
        result = self.mainEngine.get_total_evaluate_detail(7)

        self.setRowCount(len(result))
        row = 0
        for r in result:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.headerList):
                content = r[header]
                cellType = self.headerDict[header]['cellType']
                cell = cellType(content)
                self.setItem(row, n, cell)
            row = row + 1


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    mflv = TotalValuationView(mainEngine, mainEngine.eventEngine)
    # mainfdv = MoneyFundSummaryView(mainEngine)
    mflv.showMaximized()
    # mainfdv.showMaximized()
    sys.exit(app.exec_())
