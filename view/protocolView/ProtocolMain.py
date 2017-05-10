# -*- coding: utf-8 -*-
import datetime
from collections import OrderedDict

from PyQt5.QtWidgets import QAction, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QApplication

from view.BasicWidget import BASIC_FONT, BasicFcView, BasicCell, NumCell
from controller.EventType import EVENT_PD
from controller.MainEngine import MainEngine


class ProtocolViewMain(BasicFcView):
    def __init__(self, mainEngine, parent=None):
        super(ProtocolViewMain, self).__init__()
        self.mainEngine = mainEngine
        self.setMinimumSize(1300, 600)
        self.initMain()

    def initMain(self):
        """初始化界面"""
        self.setWindowTitle('现金主界面')
        filterBar = FilterBar(self.mainEngine)
        cashListView = ProtocolListView(self.mainEngine)

        vbox = QVBoxLayout()
        vbox.addWidget(filterBar)
        vbox.addWidget(cashListView)
        self.setLayout(vbox)

    def show(self):
        """显示"""
        super(ProtocolViewMain, self).show()


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


class ProtocolListView(BasicFcView):
    """协存详情"""

    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(ProtocolListView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()
        d['asset_name'] = {'chinese': '协存项目名称', 'cellType': BasicCell}
        d['rate'] = {'chinese': '协存项目利率', 'cellType': BasicCell}

        d['cal_date'] = {'chinese': '计算日', 'cellType': BasicCell}

        # 协存项目
        d['total_amount'] = {'chinese': '总额', 'cellType': NumCell}
        d['total_principal'] = {'chinese': '协存本金', 'cellType': NumCell}
        d['asset_ret'] = {'chinese': '当日协存利息和', 'cellType': NumCell}
        # 协存项目 输入项
        d['ret_carry_principal'] = {'chinese': '利息转结本金', 'cellType': NumCell}
        d['cash_to_agreement'] = {'chinese': '现金->协存', 'cellType': NumCell}
        d['agreement_to_cash'] = {'chinese': '协存->现金', 'cellType': NumCell}

        self.setHeaderDict(d)

        self.setEventType(EVENT_PD)

        self.initUi()

    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('协存明细')
        self.setMinimumSize(1200, 600)
        self.setFont(BASIC_FONT)
        self.initTable()
        self.refresh()
        self.addMenuAction()

        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(self.eventType, self.signal.emit)

    def showProtocolListDetail(self):
        """显示所有合约数据"""
        result = self.mainEngine.get_agreement_detail_by_days()
        print(result)
        count = 0
        for d in result:
            for v in d.values():
                count = count + len(v)
        self.setRowCount(count)
        row = 0
        # 遍历资产类型
        for r in result:
            # 遍历对应资产的记录
            for col in r.values():
                for c in col:
                    # print(c)
                    # 按照定义的表头，进行数据填充
                    for n, header in enumerate(self.headerList):
                        content = c[header]
                        cell = self.headerDict[header]['cellType'](content)
                        # print(row,n,content)
                        self.setItem(row, n, cell)

                    row = row + 1

    def refresh(self):
        """刷新"""
        self.menu.close()  # 关闭菜单
        self.clearContents()
        self.setRowCount(0)
        self.showProtocolListDetail()
        print('pd refresh called ....')

    def addMenuAction(self):
        """增加右键菜单内容"""
        refreshAction = QAction('刷新', self)
        refreshAction.triggered.connect(self.refresh)

        self.menu.addAction(refreshAction)

    def show(self):
        """显示"""
        super(ProtocolListView, self).show()
        self.refresh()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    plv = ProtocolViewMain(mainEngine)

    plv.show()
    sys.exit(app.exec_())
