# -*- coding: utf-8 -*-
import codecs
import csv
from collections import OrderedDict

import datetime

import re
from PyQt5 import QtCore

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QAction, QApplication, QFileDialog, QHBoxLayout, QPushButton, QLineEdit, QLabel, QVBoxLayout
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

from miscView.TodayCostInput import TodayCostInput
from utils.MoneyFormat import outputmoney
from controller.EventType import EVENT_MAIN_VALUATION, EVENT_MAIN_ASSERT_DETAIL, EVENT_MAIN_FEE, EVENT_MAIN_COST
from controller.MainEngine import MainEngine
from view.BasicWidget import BasicCell, BasicFcView, NumCell, BASIC_FONT
from view.assertmgtView.AssetMgtInput import AssetMgtInput
from view.assertmgtView.AssetMgtMain import AssetMgtViewMain
from view.cashView.CashInput import CashInput
from view.cashView.CashMain import CashViewMain
from view.miscView.AboutMain import AboutWidget
from view.moneyfundView.MfCateInput import MfCateInput
from view.moneyfundView.MoneyFundInput import MoneyFundInput
from view.moneyfundView.MoneyFundMain import MoneyFundMain
from view.protocolView.PdCateInput import PdCateInput
from view.protocolView.ProtocolInput import ProtocolInput
from view.protocolView.ProtocolMain import ProtocolViewMain


class MainWindow(QMainWindow, BasicFcView):
    """主窗口"""

    def __init__(self, mainEngine, eventEngine):
        """Constructor"""
        super(MainWindow, self).__init__()

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        self.widgetDict = {}  # 用来保存子窗口的字典

        self.initUi()
        self.loadWindowSettings('custom')

    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('feeCalc')
        self.initCentral()
        self.initTopMenu()

    def initCentral(self):
        """总估值与费用"""

        # 增加主界面显示
        widgetMainView1, dockMainView1 = self.createDock(DateMainView, '今日资金成本', QtCore.Qt.LeftDockWidgetArea)
        widgetMainView2, dockMainView2 = self.createDock(FeeTotalView, '费用详情统计', QtCore.Qt.RightDockWidgetArea)
        widgetMainView3, dockMainView3 = self.createDock(AssertTotalView, '存量资产详情', QtCore.Qt.BottomDockWidgetArea)
        widgetMainView4, dockMainView4 = self.createDock(TotalValuationMain, '总估值表', QtCore.Qt.BottomDockWidgetArea)
        self.tabifyDockWidget(dockMainView3, dockMainView4)

        # dockMainView.raise_()

    def initTopMenu(self):
        """初始化菜单"""
        menubar = self.menuBar()

        # 设计为只显示存在的接口
        sysMenu = menubar.addMenu('系统')
        sysMenu.addAction(self.createAction('导出估值数据', self.openValuationDetail))
        sysMenu.addAction(self.createAction('输入今日资金成本', self.openAddTodayCost))
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
        # assertMgtMenu.addAction(self.createAction('资管估值调整', self.oepnAdjustValuation))
        assertMgtMenu.addAction(self.createAction('增加资管类别', self.openAddAssetMgtCate))
        assertMgtMenu.addAction(self.createAction('导出存量记录', self.openOutAssetMgtUpData))
        assertMgtMenu.addAction(self.createAction('导出委贷记录', self.openOutAssetMgtData))
        sysMenu.addSeparator()
        # 帮助
        helpMenu = menubar.addMenu('帮助')
        helpMenu.addAction(self.createAction('关于', self.openAbout))

    def openAbout(self):
        """打开关于"""
        try:
            self.widgetDict['aboutW'].show()
        except KeyError:
            self.widgetDict['aboutW'] = AboutWidget(self)
            self.widgetDict['aboutW'].show()

    def openValuationDetail(self):
        try:
            self.widgetDict['openValuationDetail'].saveToCsv()
        except KeyError:
            self.widgetDict['openValuationDetail'] = TotalValuationMain(self.mainEngine)
            self.widgetDict['openValuationDetail'].saveToCsv()

    def openCashListDetail(self):
        """打开现金明细"""
        try:
            self.widgetDict['showCashListDetail'].show()
        except KeyError:
            self.widgetDict['showCashListDetail'] = CashViewMain(self.mainEngine)
            self.widgetDict['showCashListDetail'].show()

    def openProtocolListDetail(self):
        """打开协存明细"""
        try:
            self.widgetDict['openProtocolListDetail'].show()
        except KeyError:
            self.widgetDict['openProtocolListDetail'] = ProtocolViewMain(self.mainEngine)
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
            self.widgetDict['openAssetMgtListDetail'] = AssetMgtViewMain(self.mainEngine)
            self.widgetDict['openAssetMgtListDetail'].show()

    # def oepnAdjustValuation(self):
    #     """资管估值调整"""
    #     try:
    #         self.widgetDict['oepnAdjustValuationInput'].show()
    #     except KeyError:
    #         self.widgetDict['oepnAdjustValuationInput'] = AdjustValuationInput(self.mainEngine)
    #         self.widgetDict['oepnAdjustValuationInput'].show()

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

    def openAddTodayCost(self):
        """打开今日资金成本输入框"""
        try:
            self.widgetDict['openAddTodayCost'].show()
        except KeyError:
            self.widgetDict['openAddTodayCost'] = TodayCostInput(self.mainEngine)
            self.widgetDict['openAddTodayCost'].show()

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

    def openOutCashData(self):
        """打开现金导出"""
        try:
            self.widgetDict['openOutCashData'].saveToCsv()
        except KeyError:
            self.widgetDict['openOutCashData'] = CashViewMain(self.mainEngine)
            self.widgetDict['openOutCashData'].saveToCsv()

    def openOutProtocolData(self):
        """导出协存"""
        try:
            self.widgetDict['openOutProtocolData'].saveToCsv()
        except KeyError:
            self.widgetDict['openOutProtocolData'] = ProtocolViewMain(self.mainEngine)
            self.widgetDict['openOutProtocolData'].saveToCsv()

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
            self.widgetDict['openOutMoneFundData'].saveToCsv()
        except KeyError:
            self.widgetDict['openOutMoneFundData'] = MoneyFundMain(self.mainEngine)
            self.widgetDict['openOutMoneFundData'].saveToCsv()

    def openOutAssetMgtData(self):
        try:
            self.widgetDict['openOutAssetMgtData'].saveToCsv()
        except KeyError:
            self.widgetDict['openOutAssetMgtData'] = AssetMgtViewMain(self.mainEngine)
            self.widgetDict['openOutAssetMgtData'].saveToCsv()

    def openOutAssetMgtUpData(self):
        try:
            self.widgetDict['openOutAssetMgtData'].saveUpToCsv()
        except KeyError:
            self.widgetDict['openOutAssetMgtData'] = AssetMgtViewMain(self.mainEngine)
            self.widgetDict['openOutAssetMgtData'].saveUpToCsv()

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

    def loadWindowSettings(self, settingName):
        """载入窗口设置"""
        settings = QSettings('vn.trader', settingName)
        try:
            self.restoreState(settings.value('state').toByteArray())
            self.restoreGeometry(settings.value('geometry').toByteArray())
        except AttributeError:
            pass

    def restoreWindow(self):
        """还原默认窗口设置（还原停靠组件位置）"""
        self.loadWindowSettings('default')
        self.showMaximized()


class DateMainView(BasicFcView):
    """"""

    def __init__(self, mainEngine, eventEngine, parant=None):
        """Constructor"""
        super(DateMainView, self).__init__(mainEngine, eventEngine, parant)
        # 设置表头有序字典
        d = OrderedDict()
        d['total_assert'] = {'chinese': '计算日', 'cellType': BasicCell}
        d['cash'] = {'chinese': '今日资金成本', 'cellType': BasicCell}

        self.setHeaderDict(d)
        # 设置数据键
        self.setDataKey('fcSymbol')

        self.eventType = EVENT_MAIN_COST

        # 设置字体
        # self.setFont(BASIC_FONT)

        # 设置允许排序
        self.setSorting(True)

        # 界面初始化
        self.initUI()

        # 注册事件监听
        # self.registerEvent()

    def initUI(self):
        # 初始化表格
        self.initTable()
        self.refresh()

        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(self.eventType, self.signal.emit)

    def refresh(self):
        self.initData()

    def initData(self):
        """初始化数据"""
        result = self.mainEngine.getMainCostData()
        self.setRowCount(1)
        row = 0
        self.setItem(0, 0, BasicCell(result[0]))
        self.setItem(0, 1, NumCell(result[1]))


class FeeTotalView(BasicFcView):
    """"""

    def __init__(self, mainEngine, eventEngine, parant=None):
        """Constructor"""
        super(FeeTotalView, self).__init__(mainEngine, eventEngine, parant)
        # 设置表头有序字典
        d = OrderedDict()
        d['date'] = {'chinese': '--', 'cellType': BasicCell}
        d['fee1'] = {'chinese': '费用1', 'cellType': BasicCell}
        d['fee2'] = {'chinese': '费用2', 'cellType': BasicCell}
        d['fee3'] = {'chinese': '费用3', 'cellType': BasicCell}
        d['fee4'] = {'chinese': '超额费用', 'cellType': BasicCell}

        self.setHeaderDict(d)
        # 设置数据键
        self.setDataKey('fcSymbol')

        self.eventType = EVENT_MAIN_FEE

        # 设置字体
        # self.setFont(BASIC_FONT)

        # 设置允许排序
        self.setSorting(True)
        self.initUI()

    def initUI(self):
        # 初始化表格
        self.initTable()
        self.refresh()

        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(self.eventType, self.signal.emit)

    def refresh(self):
        self.initData()

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
        # todayFee = self.mainEngine.getTodayFee(date)

        todayFee = self.mainEngine.get_today_fees()
        today_fee_list = list()
        today_fee_list.append(todayFee['fee1'])
        today_fee_list.append(todayFee['fee2'])
        today_fee_list.append(todayFee['fee3'])
        today_fee_list.append(todayFee['fee4'])
        c = 1
        for tf in today_fee_list:
            self.setItem(2, c, NumCell(tf))
            c += 1


class AssertTotalView(BasicFcView):
    """主界面"""

    def __init__(self, mainEngine, eventEngine, parent=None):
        """Constructor"""
        super(AssertTotalView, self).__init__(mainEngine, eventEngine, parent)

        # 设置表头有序字典
        d = OrderedDict()
        d['date'] = {'chinese': '存量资产详情', 'cellType': BasicCell}
        d['total_assert'] = {'chinese': '--', 'cellType': BasicCell}
        d['cash'] = {'chinese': '--', 'cellType': BasicCell}
        d['money_fund'] = {'chinese': '比例', 'cellType': BasicCell}
        d['assert_mgt'] = {'chinese': '净值/价格', 'cellType': NumCell}
        d['liquid_assert_ratio'] = {'chinese': '份额', 'cellType': BasicCell}
        d['today_total_revenue'] = {'chinese': '金额', 'cellType': NumCell}
        d['fee_1'] = {'chinese': '本金', 'cellType': NumCell}
        d['fee_2'] = {'chinese': '累计收益', 'cellType': NumCell}
        d['fee_3'] = {'chinese': '今日收益', 'cellType': NumCell}

        self.setHeaderDict(d)
        # 设置数据键
        self.setDataKey('fcSymbol')

        # 设置监控事件类型
        self.eventType = EVENT_MAIN_ASSERT_DETAIL
        # 设置字体
        # self.setFont(BASIC_FONT)

        # 设置允许排序
        self.setSorting(True)

        # 初始化表格
        self.initTable()


class TotalValuationMain(BasicFcView):
    """总估值表"""

    def __init__(self, mainEngine, parent=None):
        super(TotalValuationMain, self).__init__(mainEngine=mainEngine)
        self.mainEngine = mainEngine
        self.eventEngine = mainEngine.eventEngine

        self.initUI()
        self.refresh()

    def initUI(self):
        ############################
        # FilterBar
        ############################
        self.filterView = BasicFcView(self.mainEngine)

        filterStartDate_Label = QLabel('开始时间')
        self.filterView.filterStartDate_Edit = QLineEdit(str(datetime.date.today()))
        self.filterView.filterStartDate_Edit.setMaximumWidth(80)
        filterEndDate_Label = QLabel('结束时间')
        self.filterView.filterEndDate_Edit = QLineEdit(str(datetime.date.today()))
        self.filterView.filterEndDate_Edit.setMaximumWidth(80)

        filterBtn = QPushButton('筛选')
        # outputBtn = QPushButton('导出')

        filterBtn.clicked.connect(self.filterAction)
        # outputBtn.clicked.connect(self.outputAction)

        filterHBox = QHBoxLayout()
        filterHBox.addStretch()
        filterHBox.addWidget(filterStartDate_Label)
        filterHBox.addWidget(self.filterView.filterStartDate_Edit)
        filterHBox.addWidget(filterEndDate_Label)
        filterHBox.addWidget(self.filterView.filterEndDate_Edit)
        filterHBox.addWidget(filterBtn)
        # filterHBox.addWidget(outputBtn)

        self.filterView.setLayout(filterHBox)
        self.filterView.setMaximumHeight(50)
        #############################
        # TotalValuationView
        #############################
        self.totalValuationView = BasicFcView(self.mainEngine)
        # 设置表头有序字典
        d = OrderedDict()
        d['cal_date'] = {'chinese': '计算日', 'cellType': BasicCell}
        d['all_value'] = {'chinese': '总资产净值', 'cellType': NumCell}
        d['cash'] = {'chinese': '现金', 'cellType': NumCell}
        d['agreement'] = {'chinese': '协存', 'cellType': NumCell}
        d['fund'] = {'chinese': '货币基金', 'cellType': NumCell}
        d['management'] = {'chinese': '资管', 'cellType': NumCell}
        # d['liquid_assert_ratio'] = {'chinese': '流动资产比例', 'cellType': BasicCell}
        d['all_ret'] = {'chinese': '当日总收益', 'cellType': NumCell}
        d['fee1'] = {'chinese': '费用1', 'cellType': NumCell}
        d['fee2'] = {'chinese': '费用2', 'cellType': NumCell}
        d['fee3'] = {'chinese': '费用3', 'cellType': NumCell}
        d['fee4'] = {'chinese': '费用4', 'cellType': NumCell}
        d['cost'] = {'chinese': '当日资金成本', 'cellType': NumCell}
        # d['today_product_revenue'] = {'chinese': '当日产品收益', 'cellType': BasicCell}
        # d['fee_accual'] = {'chinese': '费用计提', 'cellType': BasicCell}

        self.eventType = EVENT_MAIN_VALUATION
        self.totalValuationView.setHeaderDict(d)
        self.totalValuationView.setFont(BASIC_FONT)
        self.totalValuationView.setSorting(True)
        self.totalValuationView.initTable()

        #########################
        # 界面整合
        #########################
        vbox = QVBoxLayout()
        vbox.addWidget(self.filterView)
        vbox.addWidget(self.totalValuationView)
        self.setLayout(vbox)

        # 链接信号
        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(self.eventType, self.signal.emit)

    def filterAction(self):
        d = datetime.date.today()
        filter_start_date = str(self.filterView.filterStartDate_Edit.text()).split('-')
        filter_end_date = str(self.filterView.filterEndDate_Edit.text()).split('-')
        if filter_start_date is None or filter_end_date is None:
            start_date = datetime.date(d.year, d.month, d.day)
            end_date = datetime.date(d.year, d.month, d.day)
        else:
            start_date = datetime.date(int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", filter_start_date[0])),
                                       int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", filter_start_date[1])),
                                       int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", filter_start_date[2])))
            end_date = datetime.date(int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", filter_end_date[0])),
                                     int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", filter_end_date[1])),
                                     int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", filter_end_date[2])))

        print('filter Action', start_date, end_date)
        self.filterRefresh(start_date, end_date)

    def refresh(self):
        """默认刷新"""
        self.clearContents()
        self.setRowCount(0)
        result = self.mainEngine.get_total_evaluate_detail(7)
        self.showTotalEvaluateDetail(result)

    def filterRefresh(self, start, end):
        """过滤刷新"""
        self.clearContents()
        self.setRowCount(0)
        result = self.mainEngine.get_total_evaluate_detail_by_period(start=start, end=end)
        self.showTotalEvaluateDetail(result)

    def addPopAction(self, start, end):
        """增加右键菜单内容"""
        refreshAction = QAction('刷新', self)
        refreshAction.triggered.connect(self.refresh)
        self.menu.addAction(refreshAction)

    def showTotalEvaluateDetail(self, result):
        """初始化数据"""
        self.totalValuationView.setRowCount(len(result))
        row = 0
        for r in result:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.totalValuationView.headerList):
                content = r[header]
                cellType = self.totalValuationView.headerDict[header]['cellType']
                cell = cellType(content)
                self.totalValuationView.setItem(row, n, cell)
            row = row + 1

    def saveToCsv(self):
        # 先隐藏右键菜单
        # self.menu.close()

        csvContent = list()
        labels = [d['chinese'] for d in self.totalValuationView.headerDict.values()]
        csvContent.append(labels)
        content = self.mainEngine.get_total_evaluate_detail()
        for c in content:
            row = list()
            for n, header in enumerate(self.totalValuationView.headerDict.keys()):
                if header is not 'cal_date':
                    row.append(outputmoney(c[header]))
                else:
                    row.append(c[header])
            csvContent.append(row)

        # 获取想要保存的文件名
        path = QFileDialog.getSaveFileName(self, '保存数据', '', 'CSV(*.csv)')

        try:
            if path[0]:
                print(path[0])
                with codecs.open(path[0], 'w', 'utf_8_sig') as f:
                    writer = csv.writer(f)
                    writer.writerows(csvContent)
                f.close()

        except IOError as e:
            pass


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    mw = MainWindow(mainEngine, mainEngine.eventEngine)
    # mflv = TotalValuationView(mainEngine, mainEngine.eventEngine)
    # mainfdv = MoneyFundSummaryView(mainEngine)
    mw.showMaximized()
    # mainfdv.showMaximized()
    sys.exit(app.exec_())
