# -*- coding: utf-8 -*-
import datetime
from collections import OrderedDict

from PyQt5.QtWidgets import QAction, QMainWindow, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QApplication

from view.BasicWidget import BASIC_FONT, BasicFcView, BasicCell, NumCell
from controller.EventType import EVENT_CASH
from controller.MainEngine import MainEngine


class CashViewMain(BasicFcView):
    def __init__(self, mainEngine, parent=None):
        super(CashViewMain, self).__init__()
        self.mainEngine = mainEngine
        self.setMinimumSize(1300, 600)
        self.initMain()

    def initMain(self):
        """初始化界面"""
        self.setWindowTitle('现金主界面')
        filterBar = FilterBar(self.mainEngine)
        cashListView = CashListView(self.mainEngine)

        vbox = QVBoxLayout()
        vbox.addWidget(filterBar)
        vbox.addWidget(cashListView)
        self.setLayout(vbox)

    def show(self):
        """显示"""
        super(CashViewMain, self).show()


class FilterBar(QWidget):
    def __init__(self, mainEngine, parent=None):
        super(FilterBar, self).__init__()
        self.initUI()

    def initUI(self):
        # 过滤的开始时间
        filterStartDate_Label = QLabel('开始时间')
        # 开始时间输入框
        self.filterStartDate_Edit = QLineEdit(str(datetime.date.today()))
        self.filterStartDate_Edit.setMaximumWidth(80)
        # 过滤的结束时间
        filterEndDate_Label = QLabel('结束时间')
        # 结束时间输入框
        self.filterEndDate_Edit = QLineEdit(str(datetime.date.today()))
        self.filterEndDate_Edit.setMaximumWidth(80)

        # 筛选按钮
        filterBtn = QPushButton('筛选')
        # 导出按钮
        outputBtn = QPushButton('导出')

        filterHBox = QHBoxLayout()
        filterHBox.addStretch()
        filterHBox.addWidget(filterStartDate_Label)
        filterHBox.addWidget(self.filterStartDate_Edit)
        filterHBox.addWidget(filterEndDate_Label)
        filterHBox.addWidget(self.filterEndDate_Edit)

        filterHBox.addWidget(filterBtn)
        filterHBox.addWidget(outputBtn)

        self.setLayout(filterHBox)


class CashListView(BasicFcView):
    """现金详情"""

    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(CashListView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()
        d['cal_date'] = {'chinese': '计算日', 'cellType': BasicCell}
        d['total_amount'] = {'chinese': '现金总额', 'cellType': NumCell}
        d['cash_to_management'] = {'chinese': '现金->资管', 'cellType': NumCell}
        d['cash_to_fund'] = {'chinese': '现金->货基', 'cellType': NumCell}
        d['cash_to_agreement'] = {'chinese': '现金->协存', 'cellType': NumCell}
        d['cash_to_investor'] = {'chinese': '现金->兑付投资人', 'cellType': NumCell}
        d['management_to_cash'] = {'chinese': '资管->现金', 'cellType': NumCell}
        d['fund_to_cash'] = {'chinese': '货基->现金', 'cellType': NumCell}
        d['agreement_to_cash'] = {'chinese': '协存->现金', 'cellType': NumCell}
        d['investor_to_cash'] = {'chinese': '投资人->现金', 'cellType': NumCell}
        d['cash_return'] = {'chinese': '现金收入', 'cellType': NumCell}
        d['cash_draw_fee'] = {'chinese': '提取费用', 'cellType': NumCell}

        self.setEventType(EVENT_CASH)

        self.setHeaderDict(d)

        self.eventType = 'eCash'

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('现金明细')
        # self.setMinimumSize(1300, 600)

        self.setFont(BASIC_FONT)

        # self.initFilterBar()
        self.initTable()
        self.addMenuAction()
        self.refresh()

        # 将信号连接到refresh函数
        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(self.eventType, self.signal.emit)

    def showCashListDetail(self):
        """显示现金记录明细"""

        result = self.mainEngine.get_cash_detail_by_days(7)

        # print(result)
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

    def refresh(self):
        """刷新"""
        self.menu.close()  # 关闭菜单
        self.clearContents()
        self.setRowCount(0)
        self.showCashListDetail()

    def addMenuAction(self):
        """增加右键菜单内容"""
        refreshAction = QAction('刷新', self)
        refreshAction.triggered.connect(self.refresh)

        self.menu.addAction(refreshAction)

    def show(self):
        """显示"""
        super(CashListView, self).show()
        self.refresh()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    # clv = CashListView(mainEngine)
    clv = CashViewMain(mainEngine)
    clv.show()
    sys.exit(app.exec_())
