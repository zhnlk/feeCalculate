# -*- coding: utf-8 -*-
import datetime
from PyQt5 import QtCore
from collections import OrderedDict

from PyQt5.QtWidgets import QAction, QMainWindow, QDockWidget, QApplication

from view.assertmgtView.AdjustValuationView import AdjustValuationView
from view.assertmgtView.AssetMgtAdjustInput import AdjustValuationInput
from view.BasicWidget import BASIC_FONT, BasicFcView, BasicCell, NumCell
from controller.EventType import EVENT_AM
from controller.MainEngine import MainEngine


class AssetMgtListView(QMainWindow, BasicFcView):
    """现金详情"""

    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(AssetMgtListView, self).__init__()

        self.mainEngine = mainEngine

        self.initUi()

    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('资管明细')

        """初始化界面"""
        self.setMinimumSize(1200, 600)
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


class AssetDailyInventoryView(BasicFcView):
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(AssetDailyInventoryView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()

        d['cal_date'] = {'chinese': '计算日', 'cellType': BasicCell}
        # d['input_date'] = {'chinese': '填表日', 'cellType': BasicCell}
        d['management_amount'] = {'chinese': '存量总额', 'cellType': NumCell}
        d['management_ret'] = {'chinese': '存量日收益', 'cellType': NumCell}
        d['cash_to_management'] = {'chinese': '总净流入', 'cellType': NumCell}

        self.setHeaderDict(d)

        self.setEventType(EVENT_AM)

        self.initUi()

    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('资管每日存量表')
        # self.setMinimumSize(1200, 600)
        # self.setFont(BASIC_FONT)
        self.initTable()
        self.show()
        # self.addMenuAction()
        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(self.eventType, self.signal.emit)

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

    def showMoneyFundListDetail(self):
        """显示所有合约数据"""
        result = self.mainEngine.get_total_management_statistic()
        # print(result)
        self.setRowCount(len(result))
        row = 0
        for r in result:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.headerList):
                content = r[header]
                cellType = self.headerDict[header]['cellType']
                cell = cellType(content)
                # print(cell.text())
                self.setItem(row, n, cell)

            row = row + 1


class CommitteeDetailView(BasicFcView):
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(CommitteeDetailView, self).__init__(parent=parent)

        self.mainEngine = mainEngine
        self.eventDict = {}  # 事件辅助字典
        self.widgetDict = {}  # 用来保存子窗口的字典

        d = OrderedDict()

        # 货基项目
        # d['no'] = {'chinese': '序号', 'cellType': BasicCell}
        d['asset_name'] = {'chinese': '借款人', 'cellType': BasicCell}
        d['management_amount'] = {'chinese': '放款金额', 'cellType': NumCell}
        d['ret_rate'] = {'chinese': '委贷利率(年化)', 'cellType': BasicCell}
        d['start_date'] = {'chinese': '起息日', 'cellType': BasicCell}
        d['expiry_date'] = {'chinese': '到期日', 'cellType': BasicCell}
        d['management_due'] = {'chinese': '期限', 'cellType': BasicCell}
        # d['committee_interest'] = {'chinese': '委贷利息', 'cellType': BasicCell}
        d['bank_fee'] = {'chinese': '委贷银行费用', 'cellType': NumCell}
        d['manage_fee'] = {'chinese': '资管计划费用', 'cellType': NumCell}
        d['asset_ret'] = {'chinese': '资管计划总收益', 'cellType': NumCell}
        d['mamangement_daily_ret'] = {'chinese': '资管计划每日收益', 'cellType': NumCell}
        # d['asset_plan_daily_valuation'] = {'chinese': '正常情况资管计划\n每日收益估值', 'cellType': BasicCell}
        d['uuid_view'] = {'chinese': '调整查看', 'cellType': BasicCell}
        d['uuid_input'] = {'chinese': '估值调整', 'cellType': BasicCell}

        self.setHeaderDict(d)

        self.setEventType(EVENT_AM)
        self.initUi()

    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('委贷明细')
        # self.setMinimumSize(1200, 600)
        # self.setFont(BASIC_FONT)
        self.initTable()
        self.show()
        # self.addMenuAction()
        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(self.eventType, self.signal.emit)

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

    def showMoneyFundSummary(self):
        """显示所有合约数据"""
        result = self.mainEngine.get_all_management_detail()
        print(result)
        self.setRowCount(len(result))
        row = 0
        for r in result:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.headerList):
                if header is 'uuid_view':
                    content = '查看'
                elif header is 'uuid_input':
                    content = '调整'
                else:
                    content = r[header]
                self.eventDict[row] = r['uuid']
                cellType = self.headerDict[header]['cellType']
                cell = cellType(content)
                self.setItem(row, n, cell)
            row = row + 1

        self.setDoubleClickEvent(9)

    def setDoubleClickEvent(self, n):
        for r in self.eventDict.keys():
            # self.itemDoubleClicked(self.item(r, n)).connect(self.showValuationView(self.eventDict[r])).emit()
            # self.cellDoubleClicked(r, n).connect(self.showValuationView(self.eventDict[r]))
            print('set view item double clicked called', r, n, self.eventDict[r])
            # self.itemDoubleClicked(self.item(r, n + 1)).connect(self.showValuationInput(self.eventDict[r])).emit()
            # self.cellDoubleClicked(r, n + 1).connect(self.showValuationInput(self.eventDict[r]))
            print('set input item double clicked called', r, n+1, self.eventDict[r])

    def showValuationInput(self, uuid):
        """打开估值调整的子窗口"""

        try:
            self.widgetDict['adjustValuationInput'].show()
        except KeyError:
            self.widgetDict['adjustValuationInput'] = AdjustValuationInput(self.mainEngine, uuid=uuid)
            self.widgetDict['adjustValuationInput'].show()

    def showValuationView(self, uuid):
        """打开估值调整的显示子窗口"""
        try:
            self.widgetDict['adjustValuationView'].show()
        except KeyError:
            self.widgetDict['adjustValuationView'] = AdjustValuationView(self.mainEngine, uuid=uuid)
            self.widgetDict['adjustValuationView'].show()

    def closeEvent(self, event):
        """资管主界面的关闭事件"""
        # reply = QMessageBox.question(self, '退出', '确认退出?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # if reply == QMessageBox.Yes:
        for widget in self.widgetDict.values():
            widget.close()

        # self.mainEngine.exit()
        event.accept()
        # else:
        #     event.ignore()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    # mfm = AssetMgtListView(mainEngine)
    # mflv = AssetDailyInventoryView(mainEngine)
    mfm = CommitteeDetailView(mainEngine)
    # mflv.showMaximized()
    # mainfdv.showMaximized()
    mfm.showMaximized()
    sys.exit(app.exec_())
