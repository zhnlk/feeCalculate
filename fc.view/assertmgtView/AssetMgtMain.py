# -*- coding: utf-8 -*-
import datetime
from PyQt5 import QtCore
from collections import OrderedDict

from PyQt5.QtWidgets import QAction, QMainWindow, QDockWidget, QApplication

from BasicWidget import BASIC_FONT, BasicFcView, BasicCell
from EventType import EVENT_AM
from MainEngine import MainEngine


class AssetMgtListView(QMainWindow, BasicFcView):
    """现金详情"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(AssetMgtListView, self).__init__()

        self.mainEngine = mainEngine

        # self.setEventType(EVENT_MF)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('资管明细')
        # self.setFont(BASIC_FONT)
        # self.initTable()
        # self.addMenuAction()

        """初始化界面"""
        self.setMinimumSize(1200, 600)
        # self.setFont(BASIC_FONT)
        # self.initTable()
        # self.addMenuAction()
        # self.show()
        self.initDock()

    def initDock(self):
        # 创建浮动布局
        vidgetView1, dockView1 = self.createDock(AssetDailyInventoryView, '资管每日存量表', QtCore.Qt.TopDockWidgetArea)
        vidgetView2, dockView2 = self.createDock(CommitteeDetailView, '委贷明细', QtCore.Qt.BottomDockWidgetArea)


        # self.tabifyDockWidget(dockView1,dockView2)

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
        # ----------------------------------------------------------------------


class AssetDailyInventoryView(BasicFcView):
    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(AssetDailyInventoryView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()

        d['cal_date'] = {'chinese': '计算日', 'cellType': BasicCell}
        d['input_date'] = {'chinese': '填表日', 'cellType': BasicCell}
        d['inventory_amount'] = {'chinese': '存量总额', 'cellType': BasicCell}
        d['inventory_daily_revenue'] = {'chinese': '存量日收益', 'cellType': BasicCell}
        d['total_liquid_amount'] = {'chinese': '总净流动', 'cellType': BasicCell}

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
        super(AssetDailyInventoryView, self).show()
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
        # result0 = self.mainEngine.getProtocol()
        result1 = self.mainEngine.getProtocolDetail()
        result2 = self.mainEngine.getMoneyFundDetail()
        print(len(result1) + len(result2))
        # self.setRowCount(len(result1)+len(result2))
        self.setRowCount(len(result2))
        row = 0
        for r in result2:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.headerList):
                # if header is 'mf_project_name':
                #     content = r.getMfProjectName(r.mf_obj_uuid)
                    # else:
                content = ''
                    # content = r.__getattribute__(header)
                cellType = self.headerDict[header]['cellType']
                cell = cellType(content)
                print(cell.text())
                if self.font:
                    cell.setFont(self.font)  # 如果设置了特殊字体，则进行单元格设置

                self.setItem(row, n, cell)

            row = row + 1


class CommitteeDetailView(BasicFcView):
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(CommitteeDetailView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()

        # 货基项目
        d['no'] = {'chinese': '序号', 'cellType': BasicCell}
        d['loan'] = {'chinese': '借款人', 'cellType': BasicCell}
        d['loan_amount'] = {'chinese': '放款金额', 'cellType': BasicCell}
        d['committee_rate'] = {'chinese': '委贷利率(年化)', 'cellType': BasicCell}
        d['value_date'] = {'chinese': '起息日', 'cellType': BasicCell}
        d['due_date'] = {'chinese': '到期日', 'cellType': BasicCell}
        d['duration'] = {'chinese': '期限', 'cellType': BasicCell}
        d['committee_interest'] = {'chinese': '委贷利息', 'cellType': BasicCell}
        d['committee_bank_fee'] = {'chinese': '委贷银行费用', 'cellType': BasicCell}
        d['asset_plan_fee'] = {'chinese': '资管计划费用', 'cellType': BasicCell}
        d['asset_plan_revenue'] = {'chinese': '资管计划总收益', 'cellType': BasicCell}
        d['asset_plan_daily_revenue'] = {'chinese': '资管计划每日收益', 'cellType': BasicCell}
        d['asset_plan_daily_valuation'] = {'chinese': '正常情况资管计划\n每日收益估值', 'cellType': BasicCell}
        d['valuation_adjust'] = {'chinese': '估值调整', 'cellType': BasicCell}

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
        super(CommitteeDetailView, self).show()
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

        date = datetime.date(2017, 3, 10)

        result = self.mainEngine.getMoneyFundSummary(date)
        self.setRowCount(len(result))
        row = 0
        for r in result:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.headerList):
                if header is 'mf_project_name':
                    # content = MfProjectList.getMfProjectName(r[0])
                    # else:
                    content = r[n]
                cellType = self.headerDict[header]['cellType']
                cell = cellType(content)
                print(row, n, cell.text())
                self.setItem(row, n, cell)

            row = row + 1


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    mfm = AssetMgtListView(mainEngine)
    # mflv = MoneyFundDetailView(mainEngine)
    # mainfdv = MoneyFundSummaryView(mainEngine)
    # mflv.showMaximized()
    # mainfdv.showMaximized()
    mfm.showMaximized()
    sys.exit(app.exec_())


    # def showAssertMgtListDetail(self):
    #
    #     """显示所有合约数据"""
    #     l = self.mainEngine.getAllContracts()
    #     d = {'.'.join([contract.exchange, contract.symbol]): contract for contract in l}
    #     l2 = d.keys()
    #     l2.sort(reverse=True)
    #
    #     self.setRowCount(len(l2))
    #     row = 0
    #
    #     for key in l2:
    #         contract = d[key]
    #
    #         for n, header in enumerate(self.headerList):
    #             content = contract.__getattribute__(header)
    #             cellType = self.headerDict[header]['cellType']
    #             cell = cellType(content)
    #
    #             if self.font:
    #                 cell.setFont(self.font)  # 如果设置了特殊字体，则进行单元格设置
    #
    #             self.setItem(row, n, cell)
    #
    #         row = row + 1
    #
    # # ----------------------------------------------------------------------
    #
    # def refresh(self):
    #     """刷新"""
    #     self.menu.close()  # 关闭菜单
    #     self.clearContents()
    #     self.setRowCount(0)
    #     # self.showAssertMgtListDetail()
    #
    # # ----------------------------------------------------------------------
    # def addMenuAction(self):
    #     """增加右键菜单内容"""
    #     refreshAction = QAction('刷新', self)
    #     refreshAction.triggered.connect(self.refresh)
    #
    #     self.menu.addAction(refreshAction)
    #
    # # ----------------------------------------------------------------------
    # def show(self):
    #     """显示"""
    #     super(AssertMgtListView, self).show()
    #     self.refresh()
