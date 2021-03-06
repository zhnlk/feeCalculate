# -*- coding: utf-8 -*-
import codecs
import csv
import datetime
import re
from collections import OrderedDict

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog

from view.cashView.DataModifyCashView import CashDataModifyView
from controller.EventType import EVENT_CASH
from controller.MainEngine import MainEngine
from utils.MoneyFormat import outputmoney
from view.BasicWidget import BASIC_FONT, BasicFcView, BasicCell, NumCell


class CashViewMain(BasicFcView):
    def __init__(self, mainEngine, parent=None):
        super(CashViewMain, self).__init__()
        self.mainEngine = mainEngine
        self.setWindowTitle('现金界面')
        self.setMinimumSize(1300, 600)
        self.initMain()

    def initMain(self):
        ###############################
        # FilterBar
        ###############################
        self.filterView = QWidget()

        filterStartDate_Label = QLabel('开始时间')
        self.filterView.filterStartDate_Edit = QLineEdit(str(datetime.date.today()))
        filterEndDate_Label = QLabel('结束时间')
        self.filterView.filterEndDate_Edit = QLineEdit(str(datetime.date.today()))

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
        #############################
        # CashListView
        ############################
        self.cashListView = CashListViewWidget(self.mainEngine)

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

        self.cashListView.eventType = EVENT_CASH
        self.cashListView.setHeaderDict(d)
        self.cashListView.setWindowTitle('现金明细')
        self.cashListView.setFont(BASIC_FONT)
        self.cashListView.saveData = True

        self.cashListView.initTable()
        self.cashListView.connectSignal()
        #####################
        # 界面整合合
        ####################
        vbox = QVBoxLayout()
        vbox.addWidget(self.filterView)
        vbox.addWidget(self.cashListView)
        self.setLayout(vbox)
        # 将信号连接到refresh函数

        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(self.cashListView.eventType, self.signal.emit)

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

    def outputAction(self):
        print('output Action')

    def connectSignal(self):
        self.cashListView.itemDoubleClicked.connect(self.cashListView.doubleClickTrigger)

    def show(self):
        """显示"""
        super(CashViewMain, self).show()
        self.refresh()

    def showCashListDetail(self, result):
        """显示现金记录明细"""

        print('showCashListDetail:', result)
        self.cashListView.setRowCount(len(result))
        row = 0
        for r in result:
            # 按照定义的表头，进行填充数据
            for n, header in enumerate(self.cashListView.headerList):
                content = r[header]
                cellType = self.cashListView.headerDict[header]['cellType']
                cell = cellType(content)
                if self.cashListView.saveData:
                    cell.data = r['cal_date']
                self.cashListView.setItem(row, n, cell)
            row = row + 1

    def refresh(self):
        """默认刷新"""
        # self.menu.close()  # 关闭菜单
        self.clearContents()
        self.setRowCount(0)
        result = self.mainEngine.get_cash_detail_by_days(7)
        self.showCashListDetail(result)

    def filterRefresh(self, start, end):
        """过滤刷新"""
        self.clearContents()
        self.setRowCount(0)
        result = self.mainEngine.get_cash_detail_by_period(start=start, end=end)
        print('result:', result)
        self.showCashListDetail(result=result)

    def saveToCsv(self):

        # 先隐藏右键菜单
        # self.menu.close()

        csvContent = list()
        labels = [d['chinese'] for d in self.cashListView.headerDict.values()]
        csvContent.append(labels)
        content = self.mainEngine.get_cash_detail_by_days()
        for c in content:
            row = list()
            for n, header in enumerate(self.cashListView.headerDict.keys()):
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


class CashListViewWidget(BasicFcView):
    def __init__(self, mainEngine):
        super(CashListViewWidget, self).__init__()
        self.mainEngine = mainEngine
        self.widgetDict = {}

    def doubleClickTrigger(self, cell):
        """根据单元格的数据撤单"""
        try:
            self.widgetDict['showDataModifyView'].show(cell.data)
        except KeyError:
            self.widgetDict['showDataModifyView'] = CashDataModifyView(mainEngine=self.mainEngine, data=cell.data)
            self.widgetDict['showDataModifyView'].show()

    def closeEvent(self, event):
        for widget in self.widgetDict.values():
            widget.close()

        event.accept()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    clv = CashViewMain(mainEngine)
    clv.show()
    sys.exit(app.exec_())
