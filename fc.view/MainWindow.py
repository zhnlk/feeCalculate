# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from asyncio import Event

import psutil as psutil
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from BasicWidget import AddCashDetail, AboutWidget, OutCashData


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
        self.initCentral()
        self.initMenu()
        self.initStatusBar()

    # ----------------------------------------------------------------------
    def initCentral(self):
        """总估值与费用"""
        # 垂直布局
        vbox = QVBoxLayout()
        # groupBox = QGroupBox()
        # groupBox.setLayout(vbox)

        count = QWidget()
        hbox = QHBoxLayout()
        # countLabel = QLabel("细节数目:")
        # hbox.addWidget(countLabel)
        self.countSpineBox = QSpinBox()
        self.countSpineBox.setRange(0, 10)
        # self.countSpineBox.valueChanged.connect(self.countSpineValueChanged)
        hbox.addWidget(self.countSpineBox)
        hbox.addStretch()
        count.setLayout(hbox)
        # vbox.addWidget(count)  # 垂直布局，添加widget1

        self.detailTable = QTableWidget()
        colList = list()
        colList = ['计算日', '总资产净值', '现金', '协存', '货基', '资管', '流动资产比例', '当日总收益', '费用1', '费用2', '费用3', '费用4', '当日产品收益', '费用计提']
        # 设置不可编辑
        self.detailTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.detailTable.setColumnCount(len(colList))
        self.detailTable.setRowCount(20)

        # self.detailTable.setItem()
        self.detailTable.setHorizontalHeaderLabels(colList)

        for i in range(self.detailTable.rowCount()):
            for j in range(self.detailTable.columnCount()):
                cnt = '(%d,%d)' % (i, j)
                newItem = QTableWidgetItem(cnt)
                self.detailTable.setItem(i, j, newItem)
        # self.setCentralWidget(self.table)

        vbox.addWidget(self.detailTable)  # 垂直布局，添加widget2

        # 连接组件之间的信号
        # widgetPositionM.itemDoubleClicked.connect(widgetTradingW.closePosition)

        # 保存默认设置
        self.saveWindowSettings('default')
        widget = QWidget()
        widget.setLayout(vbox)

        self.setCentralWidget(widget)


    # ----------------------------------------------------------------------
    def initMenu(self):
        """初始化菜单"""
        # 创建菜单
        menubar = self.menuBar()

        # 设计为只显示存在的接口
        sysMenu = menubar.addMenu('系统')

        sysMenu.addSeparator()
        sysMenu.addAction(self.createAction('退出', self.close))

        cashDetailMenu = menubar.addMenu('现金明细')
        cashDetailMenu.addAction(self.createAction('增加记录', self.openAddCashDetail))
        cashDetailMenu.addAction(self.createAction('导出数据', self.openOutCashData))

        # 协议存款
        protocolMenu = menubar.addMenu('协议存款')
        protocolMenu.addAction(self.createAction('增加记录', self.openAbout))
        protocolMenu.addAction(self.createAction('导出记录', self.openAbout))
        # protocolMenu.addAction()

        # 货基
        moneyFundMenu = menubar.addMenu('货基明细')
        moneyFundMenu.addAction(self.createAction('增加记录', self.openAbout))
        moneyFundMenu.addAction(self.createAction('导出记录', self.openAbout))

        # 资管
        assertMgtMenu = menubar.addMenu('资管明细')
        assertMgtMenu.addAction(self.createAction('增加记录', self.openAbout))
        assertMgtMenu.addAction(self.createAction('导出记录', self.openAbout))

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
        # action.triggered.connect(function)
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

    def openAddCashDetail(self):
        """打开现金明细"""
        try:
            self.widgetDict['addCashDetail'].show()
        except KeyError:
            self.widgetDict['addCashDetail'] = AddCashDetail()
            self.widgetDict['addCashDetail'].show()

    # ----------------------------------------------------------------------
    def openOutCashData(self):
        """打开导出数据"""
        try:
            self.widgetDict['OutCashData'].show()
        except KeyError:
            self.widgetDict['OutCashData'] = OutCashData()
            self.widgetDict['OutCashData'].show()

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


