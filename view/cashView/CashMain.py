# -*- coding: utf-8 -*-
from collections import OrderedDict

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication

from view.BasicWidget import BASIC_FONT, BasicFcView, BasicCell, NumCell
from controller.EventEngine import Event
from controller.EventType import EVENT_CASH
from controller.MainEngine import MainEngine


class CashListView(BasicFcView):
    """现金详情"""

    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(CashListView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()
        d['cal_date'] = {'chinese': '计算日', 'cellType': BasicCell}
        d['total_amount'] = {'chinese': '现金总额', 'cellType': BasicCell}
        d['cash_to_management'] = {'chinese': '现金->资管', 'cellType': BasicCell}
        d['cash_to_fund'] = {'chinese': '现金->货基', 'cellType': BasicCell}
        d['cash_to_agreement'] = {'chinese': '现金->协存', 'cellType': BasicCell}
        d['cash_to_investor'] = {'chinese': '现金->兑付投资人', 'cellType': BasicCell}
        d['management_to_cash'] = {'chinese': '资管->现金', 'cellType': BasicCell}
        d['fund_to_cash'] = {'chinese': '货基->现金', 'cellType': BasicCell}
        d['agreement_to_cash'] = {'chinese': '协存->现金', 'cellType': BasicCell}
        d['investor_to_cash'] = {'chinese': '投资人->现金', 'cellType': BasicCell}
        d['cash_return'] = {'chinese': '现金收入', 'cellType': BasicCell}
        d['cash_draw_fee'] = {'chinese': '提取费用', 'cellType': BasicCell}

        self.setEventType(EVENT_CASH)

        self.setHeaderDict(d)

        self.eventType = 'eCash'

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('现金明细')
        self.setMinimumSize(1300, 600)

        # 将信号连接到refresh函数
        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(EVENT_CASH, self.signal.emit)
        # self.resizeColumnsToContents()

        self.setFont(BASIC_FONT)
        self.initTable()
        self.addMenuAction()

    # ----------------------------------------------------------------------
    def showCashListDetail(self):
        """显示现金记录明细"""

        result = self.mainEngine.get_cash_detail_by_days(7)

        print(result)
        self.setRowCount(len(result))
        row = 0
        for r in result:
            # 按照定义的表头，进行填充数据
            for n, header in enumerate(self.headerList):
                content = r[header]
                # print(content)
                cellType = self.headerDict[header]['cellType']
                cell = cellType(content)
                self.setItem(row, n, cell)

            row = row + 1

    # ----------------------------------------------------------------------
    def refresh(self):
        """刷新"""
        self.menu.close()  # 关闭菜单
        # self.clearContents()
        # self.setRowCount(0)
        self.showCashListDetail()

    # ----------------------------------------------------------------------
    def addMenuAction(self):
        """增加右键菜单内容"""
        refreshAction = QAction('刷新', self)
        refreshAction.triggered.connect(self.refresh)

        self.menu.addAction(refreshAction)

    # ----------------------------------------------------------------------
    def show(self):
        """显示"""
        super(CashListView, self).show()

        self.refresh()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    clv = CashListView(mainEngine)

    clv.show()
    sys.exit(app.exec_())
