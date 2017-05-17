# -*- coding: utf-8 -*-
import codecs
import csv
import datetime
from collections import OrderedDict

import re
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QFileDialog, QLabel, QLineEdit, QPushButton, QHBoxLayout

from controller.EventType import EVENT_AM
from controller.MainEngine import MainEngine
from utils.MoneyFormat import outputmoney
from view.BasicWidget import BasicFcView, BasicCell, NumCell, BASIC_FONT
from view.assertmgtView.AdjustValuationView import AdjustValuationView
from view.assertmgtView.AssetMgtAdjustInput import AdjustValuationInput


class AssetMgtViewMain(BasicFcView):
    def __init__(self, mainEngine, parent=None):
        super(AssetMgtViewMain, self).__init__()
        self.mainEngine = mainEngine
        self.setWindowTitle('资管界面')
        self.widgetDict = {}  # 保存子窗口
        self.setMinimumSize(1300, 600)
        self.initMain()

    def initMain(self):
        ###############################
        # FilterBar
        ###############################
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
        ##########################
        # AssetDailyInventoryView
        #########################
        self.assetDailyInventoryView = BasicFcView(self.mainEngine)
        d = OrderedDict()
        d['cal_date'] = {'chinese': '计算日', 'cellType': BasicCell}
        d['management_amount'] = {'chinese': '存量总额', 'cellType': NumCell}
        d['management_ret'] = {'chinese': '存量日收益', 'cellType': NumCell}
        d['cash_to_management'] = {'chinese': '总净流入', 'cellType': NumCell}

        self.assetDailyInventoryView.eventType = EVENT_AM
        self.assetDailyInventoryView.setHeaderDict(d)
        self.assetDailyInventoryView.setWindowTitle('资管每日存量')
        self.assetDailyInventoryView.setFont(BASIC_FONT)

        self.assetDailyInventoryView.initTable()
        #########################
        # CommitteeDetailMain
        #########################
        self.commiteeDetailMain = BasicFcView(self.mainEngine)

        d = OrderedDict()
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

        self.commiteeDetailMain.eventType = EVENT_AM
        self.commiteeDetailMain.setHeaderDict(d)
        self.commiteeDetailMain.setWindowTitle('委贷明细')
        self.commiteeDetailMain.setFont(BASIC_FONT)
        self.commiteeDetailMain.saveData = True

        self.commiteeDetailMain.initTable()
        # 链接信号
        self.connectSignal()
        ##########################
        # 界面整合
        ##########################
        vbox = QVBoxLayout()
        vbox.addWidget(self.filterView)
        vbox.addWidget(self.assetDailyInventoryView)
        vbox.addWidget(self.commiteeDetailMain)
        self.setLayout(vbox)
        # 信号接入
        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(self.commiteeDetailMain.eventType, self.signal.emit)

    def show(self):
        """显示"""
        super(AssetMgtViewMain, self).show()
        self.refresh()

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

    def connectSignal(self):
        self.commiteeDetailMain.itemDoubleClicked.connect(self.doubleClickTrigger)

    def doubleClickTrigger(self, cell):
        try:
            op = cell.data[0]
            op_uuid = cell.data[1]
            if op is 'uuid_input':
                # print('uuid input hhhhhhhhhhhhhhhhhh')
                self.showValuationInput(uuid=op_uuid)
            elif op is 'uuid_view':
                # print('uuid view hhhhhhhhhhhhhhhhhh')
                self.showValuationView(uuid=op_uuid)
        except TypeError:
            pass


    def refresh(self):
        """刷新"""
        # self.menu.close()  # 关闭菜单
        self.clearContents()
        self.setRowCount(0)
        result = self.mainEngine.get_total_management_statistic()
        self.showAssetMgtListDetail(result)
        self.showCommiteeDetail()

    def filterRefresh(self, start_date, end_date):
        """筛选后刷新"""
        self.clearContents()
        self.setRowCount(0)
        result = self.mainEngine.get_total_management_statistic_period(start_date, end_date)
        self.showAssetMgtListDetail(result)
        self.showCommiteeDetail()

    def showAssetMgtListDetail(self, result):
        """显示所有合约数据"""

        # print(result)
        self.assetDailyInventoryView.setRowCount(len(result))
        row = 0
        for r in result:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.assetDailyInventoryView.headerList):
                content = r[header]
                cellType = self.assetDailyInventoryView.headerDict[header]['cellType']
                cell = cellType(content)
                # print(cell.text())
                self.assetDailyInventoryView.setItem(row, n, cell)

            row = row + 1

    def showCommiteeDetail(self):
        """显示所有合约数据"""
        result = self.mainEngine.get_all_management_detail()
        print(result)
        self.commiteeDetailMain.setRowCount(len(result))
        row = 0
        for r in result:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.commiteeDetailMain.headerList):
                if header is 'uuid_view':
                    content = '查看'
                elif header is 'uuid_input':
                    content = '调整'
                else:
                    content = r[header]
                cellType = self.commiteeDetailMain.headerDict[header]['cellType']
                cell = cellType(content)
                if self.commiteeDetailMain.saveData:
                    if header in ['uuid_view', 'uuid_input']:
                        cell.data = (header, r['uuid'])
                self.commiteeDetailMain.setItem(row, n, cell)
            row = row + 1

    def setDoubleClickEvent(self, n):
        for r in self.commiteeDetailMain.eventDict.keys():
            # self.commiteeDetailMain.itemDoubleClicked(self.item(r, n)).connect(self.showValuationView(self.eventDict[r])).emit()
            self.commiteeDetailMain.cellDoubleClicked(r, n).connect(self.showValuationView(self.eventDict[r]))
            print('set view item double clicked called', r, n, self.eventDict[r])
            # self.itemDoubleClicked(self.item(r, n + 1)).connect(self.showValuationInput(self.eventDict[r])).emit()
            # self.cellDoubleClicked(r, n + 1).connect(self.showValuationInput(self.eventDict[r]))
            print('set input item double clicked called', r, n + 1, self.eventDict[r])

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

    def saveUpToCsv(self):
        csvContent = list()
        labels = [d['chinese'] for d in self.assetDailyInventoryView.headerDict.values()]
        print('labels:', labels)
        csvContent.append(labels)
        content = self.mainEngine.get_total_management_statistic()
        print('content:', content)

        for c in content:
            row = list()
            for n, header in enumerate(self.assetDailyInventoryView.headerDict.keys()):
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

    def saveToCsv(self):

        csvContent = list()
        labels = [d['chinese'] for d in self.commiteeDetailMain.headerDict.values()]
        print('labels:', labels)
        csvContent.append(labels)
        content = self.mainEngine.get_all_management_detail()
        print('content:', content)

        for c in content:
            row = list()
            for n, header in enumerate(self.commiteeDetailMain.headerDict.keys()):
                if header not in ['asset_name', 'ret_rate', 'start_date', 'expiry_date', 'management_due',
                                  'uuid_view', 'uuid_input']:
                    row.append(outputmoney(c[header]))
                elif header in ['uuid_view', 'uuid_input']:
                    pass
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
    mfm = AssetMgtViewMain(mainEngine)
    # mflv = AssetDailyInventoryView(mainEngine)
    # mfm = CommitteeDetailView(mainEngine)
    # mflv.showMaximized()
    # mainfdv.showMaximized()
    mfm.show()
    sys.exit(app.exec_())
