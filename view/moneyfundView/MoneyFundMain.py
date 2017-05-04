# -*- coding: utf-8 -*-
import datetime
from PyQt5 import QtCore
from collections import OrderedDict

from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QDockWidget

from view.BasicWidget import BASIC_FONT, BasicFcView, BasicCell, NumCell
from controller.EventType import EVENT_MF
from controller.MainEngine import MainEngine


class MoneyFundMain(QMainWindow, BasicFcView):
    """现金详情"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine):
        """Constructor"""
        super(MoneyFundMain, self).__init__()

        self.mainEngine = mainEngine

        # self.setEventType(EVENT_MF)

        self.initUi()

    # ----------------------------------------------------------------------

    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('货基')
        self.setMinimumSize(1200, 600)
        # self.setFont(BASIC_FONT)
        # self.initTable()
        # self.addMenuAction()
        # self.show()
        self.initDock()

    def initDock(self):
        # 创建浮动布局
        vidgetView1, dockView1 = self.createDock(MoneyFundDetailView, '货基明细', QtCore.Qt.TopDockWidgetArea)
        vidgetView2, dockView2 = self.createDock(MoneyFundSummaryView, '今日货基总额统计', QtCore.Qt.BottomDockWidgetArea)
        # self.tabifyDockWidget(dockView1,dockView2)

    # ----------------------------------------------------------------------
    def addMenuAction(self):
        """增加右键菜单内容"""
        refreshAction = QAction('刷新', self)
        refreshAction.triggered.connect(self.refresh)

        self.menu.addAction(refreshAction)

    def createDock(self, widgetClass, widgetName, widgetArea):
        """创建停靠组件"""
        widget = widgetClass(self.mainEngine, self.eventEngine)
        dock = QDockWidget(widgetName)
        dock.setWidget(widget)
        dock.setObjectName(widgetName)
        dock.setFeatures(dock.DockWidgetFloatable | dock.DockWidgetMovable)
        self.addDockWidget(widgetArea, dock)
        return widget, dock


class MoneyFundDetailView(BasicFcView):
    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(MoneyFundDetailView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()

        d['asset_name'] = {'chinese': '货基项目名称', 'cellType': BasicCell}
        d['cal_date'] = {'chinese': '计算日', 'cellType': BasicCell}
        d['total_amount'] = {'chinese': '金额', 'cellType': NumCell}
        d['asset_ret'] = {'chinese': '收益', 'cellType': NumCell}
        d['cash_to_fund'] = {'chinese': '申购(现金)', 'cellType': NumCell}
        d['fund_to_cash'] = {'chinese': '赎回(进现金)', 'cellType': NumCell}
        d['ret_not_carry'] = {'chinese': '未结转收益', 'cellType': NumCell}
        d['ret_carry_cash'] = {'chinese': '结转金额', 'cellType': NumCell}

        self.setHeaderDict(d)

        # self.setEventType(EVENT_MF)

        self.initUi()

    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('货基明细')
        # self.setMinimumSize(1200, 600)
        # self.setFont(BASIC_FONT)
        self.initTable()
        self.show()
        # self.addMenuAction()

        # ----------------------------------------------------------------------

    def show(self):
        """显示"""
        super(MoneyFundDetailView, self).show()
        self.refresh()

    def refresh(self):
        """刷新"""
        self.menu.close()  # 关闭菜单
        self.clearContents()
        self.setRowCount(0)
        self.showMoneyFundListDetail()

        # ----------------------------------------------------------------------

    def showMoneyFundListDetail(self):
        """显示所有合约数据"""

        result = self.mainEngine.get_fund_detail_by_days(7)
        # print(result)
        self.setRowCount(len(result))
        row = 0
        for r in result:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.headerList):
                # content = r[header]
                for col in r.values():
                    content = col[0][header]
                cellType = self.headerDict[header]['cellType']
                cell = cellType(content)
                self.setItem(row, n, cell)

            row = row + 1


class MoneyFundSummaryView(BasicFcView):
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(MoneyFundSummaryView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()

        d['asset_name'] = {'chinese': '货基项目名称', 'cellType': BasicCell}
        # 货基项目
        d['total_amount'] = {'chinese': '金额', 'cellType': NumCell}
        d['total_ret_amount'] = {'chinese': '收益', 'cellType': NumCell}
        d['total_purchase_amount'] = {'chinese': '申购总额', 'cellType': NumCell}
        d['total_redeem_amount'] = {'chinese': '赎回总额', 'cellType': NumCell}

        self.setHeaderDict(d)

        # self.setEventType(EVENT_MF)

        self.initUi()

    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('今日货基总额统计')
        # self.setMinimumSize(1200, 600)
        # self.setFont(BASIC_FONT)
        self.initTable()
        self.show()
        # self.addMenuAction()

    def show(self):
        """显示"""
        super(MoneyFundSummaryView, self).show()
        self.refresh()

    def refresh(self):
        """刷新"""
        self.menu.close()  # 关闭菜单
        self.clearContents()
        self.setRowCount(0)
        self.showMoneyFundSummary()

        # ----------------------------------------------------------------------

    def showMoneyFundSummary(self):
        """显示所有合约数据"""

        result = self.mainEngine.get_total_fund_statistic()
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
    mfm = MoneyFundMain(mainEngine)
    # mflv = MoneyFundDetailView(mainEngine)
    # mainfdv = MoneyFundSummaryView(mainEngine)
    # mflv.showMaximized()
    # mainfdv.showMaximized()
    mfm.showMaximized()
    sys.exit(app.exec_())
