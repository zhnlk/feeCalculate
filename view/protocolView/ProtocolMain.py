# -*- coding: utf-8 -*-
import codecs
import csv
import datetime
from collections import OrderedDict

import re
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QComboBox, QFileDialog, QWidget
from PyQt5.QtWidgets import QApplication

from view.protocolView.DataModifyAgreementView import AgreementDataModifyView
from view.BasicWidget import BASIC_FONT, BasicFcView, BasicCell, NumCell
from controller.EventType import EVENT_PD, EVENT_PD_INV
from controller.MainEngine import MainEngine
from utils.MoneyFormat import outputmoney
from utils import StaticValue as SV


class ProtocolViewMain(BasicFcView):
    def __init__(self, mainEngine, parent=None):
        super(ProtocolViewMain, self).__init__()
        self.mainEngine = mainEngine
        self.setWindowTitle('协存界面')
        self.setMinimumSize(1300, 600)
        self.initMain()

    def initMain(self):
        ############################
        # FilterBar
        ############################
        self.filterView = QWidget()

        self.filterView.protocolCate_list = list()
        # 下拉框，用来选择不同的协存项目
        protocolCate_Label = QLabel("协存项目")
        self.filterView.protocolCate = QComboBox()
        self.prepareCateData()

        filterStartDate_Label = QLabel('开始时间')
        self.filterView.filterStartDate_Edit = QLineEdit(str(datetime.date.today()))
        self.filterView.filterStartDate_Edit.resize()
        filterEndDate_Label = QLabel('结束时间')
        self.filterView.filterEndDate_Edit = QLineEdit(str(datetime.date.today()))
        self.filterView.filterEndDate_Edit.resize()

        filterBtn = QPushButton('筛选')
        # outputBtn = QPushButton('导出')

        filterBtn.clicked.connect(self.filterAction)
        # outputBtn.clicked.connect(self.outputAction)

        filterHBox = QHBoxLayout()
        filterHBox.addStretch()
        filterHBox.addWidget(protocolCate_Label)
        filterHBox.addWidget(self.filterView.protocolCate)
        filterHBox.addWidget(filterStartDate_Label)
        filterHBox.addWidget(self.filterView.filterStartDate_Edit)
        filterHBox.addWidget(filterEndDate_Label)
        filterHBox.addWidget(self.filterView.filterEndDate_Edit)
        filterHBox.addWidget(filterBtn)
        # filterHBox.addWidget(outputBtn)

        self.filterView.setLayout(filterHBox)
        ################################
        # ProtocolListView
        ###############################
        self.protocolListView = AgreementListViewWidget(self.mainEngine)
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

        self.protocolListView.eventType = EVENT_PD
        self.protocolListView.setHeaderDict(d)
        self.protocolListView.setWindowTitle('协存明细')
        self.protocolListView.saveData = True

        self.protocolListView.setFont(BASIC_FONT)

        self.protocolListView.initTable()
        ##########################
        # FilterBar2
        ##########################
        self.filterView2 = QWidget()

        filterStartDate_Label = QLabel('开始时间')
        self.filterView2.filterStartDate_Edit = QLineEdit(str(datetime.date.today()))
        self.filterView2.filterStartDate_Edit.resize()
        filterEndDate_Label = QLabel('结束时间')
        self.filterView2.filterEndDate_Edit = QLineEdit(str(datetime.date.today()))
        self.filterView2.filterEndDate_Edit.resize()

        filterBtn = QPushButton('筛选')
        # outputBtn = QPushButton('导出')

        filterBtn.clicked.connect(self.filterAction2)
        # outputBtn.clicked.connect(self.outputAction)

        filterHBox = QHBoxLayout()
        filterHBox.addStretch()
        filterHBox.addWidget(filterStartDate_Label)
        filterHBox.addWidget(self.filterView2.filterStartDate_Edit)
        filterHBox.addWidget(filterEndDate_Label)
        filterHBox.addWidget(self.filterView2.filterEndDate_Edit)
        filterHBox.addWidget(filterBtn)
        # filterHBox.addWidget(outputBtn)

        self.filterView2.setLayout(filterHBox)
        ##########################
        # protocolInventory
        ##########################
        self.protocolInventory = BasicFcView(self.mainEngine)
        d = OrderedDict()
        d['cal_date'] = {'chinese': '计算日', 'cellType': BasicCell}
        d['total_amount'] = {'chinese': '协存总额', 'cellType': NumCell}
        d['total_ret_amount'] = {'chinese': '协存总收益', 'cellType': NumCell}
        self.protocolInventory.eventType = EVENT_PD_INV
        self.protocolInventory.setHeaderDict(d)
        self.protocolInventory.setWindowTitle('协存存量')
        self.protocolInventory.setFont(BASIC_FONT)

        self.protocolInventory.initTable()

        ##########################
        # 界面整合
        ##########################
        vbox = QVBoxLayout()
        vbox.addWidget(self.filterView2)
        vbox.addWidget(self.protocolInventory)#存量
        vbox.addWidget(self.filterView)
        vbox.addWidget(self.protocolListView)#明细
        self.setLayout(vbox)
        # 将信号连接到refresh函数

        self.connectSignal()
        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(self.protocolListView.eventType, self.signal.emit)

    def connectSignal(self):
        self.protocolListView.itemDoubleClicked.connect(self.protocolListView.doubleClickTrigger)

    def filterAction(self):
        d = datetime.date.today()
        asset_id_index = str(self.filterView.protocolCate.currentIndex())
        asset_id = self.filterView.protocolCate_list[int(asset_id_index)]
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
        self.filterRefresh(asset_id, start_date, end_date)

    def filterAction2(self):
        d = datetime.date.today()
        filter_start_date = str(self.filterView2.filterStartDate_Edit.text()).split('-')
        filter_end_date = str(self.filterView2.filterEndDate_Edit.text()).split('-')
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
        self.filterRefresh2(start_date, end_date)

    def outputAction(self):
        print('output Action')

    def show(self):
        """显示"""
        super(ProtocolViewMain, self).show()
        self.refresh()

    def showProtocolListDetail(self, result):
        """显示所有合约数据"""
        print('showProtocolListDetail:', result)
        count = 0
        for d in result:
            for v in d.values():
                count = count + len(v)
        self.protocolListView.setRowCount(count)
        row = 0
        # 遍历资产类型
        for r in result:
            # 遍历对应资产的记录
            for col in r.values():
                asset_id = list(r.keys())[0]
                for c in col:
                    # 按照定义的表头，进行数据填充
                    for n, header in enumerate(self.protocolListView.headerList):
                        content = c[header]
                        cell = self.protocolListView.headerDict[header]['cellType'](content)
                        if self.protocolListView.saveData:
                            cell.data = (asset_id, c['cal_date'])
                        self.protocolListView.setItem(row, n, cell)
                    row = row + 1

    def showProtocolInventory(self, result):
        """显示货基的存量"""
        print('show moneyfund inventory', result)
        self.protocolInventory.setRowCount(len(result))
        row = 0
        for r in result:
            for n, header in enumerate(self.protocolInventory.headerList):
                content = r[header]
                cellType = self.protocolInventory.headerDict[header]['cellType']
                cell = cellType(content)
                self.protocolInventory.setItem(row, n, cell)
            row = row + 1

    def refresh(self):
        """默认刷新"""
        # self.menu.close()  # 关闭菜单
        self.clearContents()
        self.setRowCount(0)
        result1 = self.mainEngine.get_agreement_detail_by_days(7)
        self.showProtocolListDetail(result1)
        result2 = self.mainEngine.get_total_agreement_statistic_by_days(7)
        self.showProtocolInventory(result2)

    def filterRefresh(self, asset_id, start, end):
        """过滤刷新"""
        self.clearContents()
        self.setRowCount(0)
        result = self.mainEngine.get_single_agreement_detail_by_period(asset_id, start=start, end=end)
        self.showProtocolListDetail(result)

    def filterRefresh2(self, start, end):
        """过滤刷新"""
        self.clearContents()
        self.setRowCount(0)
        result = self.mainEngine.get_total_agreement_statistic_by_period(start=start, end=end)
        self.showProtocolInventory(result)

    def prepareCateData(self):
        result = self.mainEngine.get_all_asset_ids_by_type(SV.ASSET_CLASS_AGREEMENT)
        for mf in result:
            if not self.filterView.protocolCate_list.__contains__(mf[0]):
                self.filterView.protocolCate_list.append(mf[0])
                self.filterView.protocolCate.addItem(mf[1])

    def saveToCsv(self):

        # 先隐藏右键菜单
        # self.menu.close()

        csvContent = list()
        labels = [d['chinese'] for d in self.protocolListView.headerDict.values()]
        print('labels:', labels)
        csvContent.append(labels)
        content = self.mainEngine.get_agreement_detail_by_days()
        print('content:', content)
        for r in content:
            # 遍历对应资产的记录
            for col in r.values():
                for c in col:
                    # 按照定义的表头，进行数据填充
                    row = list()
                    for n, header in enumerate(self.protocolListView.headerList):
                        if header not in ['cal_date', 'asset_name', 'rate']:
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

    def saveToCsv2(self):

        # 先隐藏右键菜单
        # self.menu.close()

        csvContent = list()
        labels = [d['chinese'] for d in self.protocolInventory.headerDict.values()]
        print('labels:', labels)
        csvContent.append(labels)
        content = self.mainEngine.get_total_agreement_statistic_by_days()
        print('content:', content)

        for r in content:
            row = list()
            for n, header in enumerate(self.protocolInventory.headerList):
                if header is not 'cal_date':
                    row.append(outputmoney(r[header]))
                else:
                    row.append(r[header])
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


class AgreementListViewWidget(BasicFcView):
    def __init__(self, mainEngine):
        super(AgreementListViewWidget, self).__init__()
        self.mainEngine = mainEngine
        self.widgetDict = {}

    def doubleClickTrigger(self, cell):
        """根据单元格的数据撤单"""
        try:
            self.widgetDict['showDataModifyView'].show(cell.data)
        except KeyError:
            self.widgetDict['showDataModifyView'] = AgreementDataModifyView(mainEngine=self.mainEngine,
                                                                            data=cell.data)
            self.widgetDict['showDataModifyView'].show()

    def closeEvent(self, event):
        for widget in self.widgetDict.values():
            widget.close()

        event.accept()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    plv = ProtocolViewMain(mainEngine)
    plv.show()
    sys.exit(app.exec_())
