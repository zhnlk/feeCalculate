# -*- coding: utf-8 -*-
import codecs
import csv
import datetime

import re
from collections import OrderedDict

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QComboBox, QFileDialog

from utils.MoneyFormat import outputmoney
from view.BasicWidget import BasicFcView, BasicCell, NumCell, BASIC_FONT
from controller.EventType import EVENT_MF
from controller.MainEngine import MainEngine
from utils import StaticValue as SV


class MoneyFundMain(BasicFcView):
    """现金详情"""

    def __init__(self, mainEngine):
        super(MoneyFundMain, self).__init__()
        self.mainEngine = mainEngine
        self.setWindowTitle('货基界面')
        self.setMinimumSize(1300, 600)
        self.initMain()

    def initMain(self):
        ##########################
        # FilterBar
        ##########################
        self.filterView = BasicFcView(self.mainEngine)

        self.filterView.moneyfundCate_list = list()
        # 下拉框，用来选择不同的协存项目
        moneyfundCate_Label = QLabel("协存项目")
        self.filterView.moneyfundCate = QComboBox()
        self.prepareMoneyfundData()

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
        filterHBox.addWidget(moneyfundCate_Label)
        filterHBox.addWidget(self.filterView.moneyfundCate)
        filterHBox.addWidget(filterStartDate_Label)
        filterHBox.addWidget(self.filterView.filterStartDate_Edit)
        filterHBox.addWidget(filterEndDate_Label)
        filterHBox.addWidget(self.filterView.filterEndDate_Edit)
        filterHBox.addWidget(filterBtn)
        # filterHBox.addWidget(outputBtn)

        self.filterView.setLayout(filterHBox)
        self.filterView.setMaximumHeight(50)
        ##########################
        # MoneyFundDetailMain
        ##########################
        self.moneyfundDetailMain = BasicFcView(self.mainEngine)
        d = OrderedDict()
        d['asset_name'] = {'chinese': '货基项目名称', 'cellType': BasicCell}
        d['cal_date'] = {'chinese': '计算日', 'cellType': BasicCell}
        d['total_amount'] = {'chinese': '金额', 'cellType': NumCell}
        d['asset_ret'] = {'chinese': '收益', 'cellType': NumCell}
        d['cash_to_fund'] = {'chinese': '申购(现金)', 'cellType': NumCell}
        d['fund_to_cash'] = {'chinese': '赎回(进现金)', 'cellType': NumCell}
        d['ret_not_carry'] = {'chinese': '未结转收益', 'cellType': NumCell}
        d['ret_carry_cash'] = {'chinese': '结转金额', 'cellType': NumCell}

        self.moneyfundDetailMain.eventType = EVENT_MF
        self.moneyfundDetailMain.setHeaderDict(d)
        self.moneyfundDetailMain.setWindowTitle('货基明细')
        self.moneyfundDetailMain.setFont(BASIC_FONT)

        self.moneyfundDetailMain.initTable()
        ##########################
        # MoneyFundSummaryView
        ##########################
        self.moneyfundSummaryView = BasicFcView(self.mainEngine)
        d = OrderedDict()
        d['asset_name'] = {'chinese': '货基项目名称', 'cellType': BasicCell}
        # 货基项目
        d['total_amount'] = {'chinese': '金额', 'cellType': NumCell}
        d['total_ret_amount'] = {'chinese': '收益', 'cellType': NumCell}
        d['total_purchase_amount'] = {'chinese': '申购总额', 'cellType': NumCell}
        d['total_redeem_amount'] = {'chinese': '赎回总额', 'cellType': NumCell}

        self.moneyfundSummaryView.setHeaderDict(d)
        self.moneyfundSummaryView.setWindowTitle('货基汇总')
        self.moneyfundSummaryView.setFont(BASIC_FONT)

        self.moneyfundSummaryView.initTable()
        #########################
        # 界面整合
        #########################
        vbox = QVBoxLayout()
        vbox.addWidget(self.filterView)
        vbox.addWidget(self.moneyfundDetailMain)
        vbox.addWidget(self.moneyfundSummaryView)
        self.setLayout(vbox)
        # 将信号接入
        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(self.moneyfundDetailMain.eventType, self.signal.emit)

    def filterAction(self):
        d = datetime.date.today()
        asset_id_index = str(self.filterView.moneyfundCate.currentIndex())
        asset_id = self.filterView.moneyfundCate_list[int(asset_id_index)]
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

        print('filter Action', asset_id, start_date, end_date)
        self.filterRefresh(asset_id, start_date, end_date)

    def outputAction(self):
        print('output Action')

    def show(self):
        """显示"""
        super(MoneyFundMain, self).show()
        self.refresh()

    def refresh(self):
        """刷新"""
        self.menu.close()  # 关闭菜单
        self.clearContents()
        self.setRowCount(0)
        self.showMoneyFundSummary()
        result = self.mainEngine.get_fund_detail_by_days(7)
        self.showMoneyFundListDetail(result)

    def filterRefresh(self, asset_id, start, end):
        """过滤刷新"""
        self.menu.close()
        self.clearContents()
        self.setRowCount(0)
        result = self.mainEngine.get_single_fund_detail_by_period(asset_id=asset_id, start=start, end=end)
        self.showMoneyFundListDetail(result)

    def showMoneyFundListDetail(self, result):
        """显示所有合约数据"""

        print('showMoneyFundListDetail', result)
        count = 0
        for d in result:
            for v in d.values():
                count = count + len(v)
        print('showMoneyFundListDetail:count:', count)
        self.moneyfundDetailMain.setRowCount(count)
        row = 0
        # 遍历资产类型
        for r in result:
            # 遍历对应资产的记录
            for col in r.values():
                for c in col:
                    # 按照定义的表头，进行数据填充
                    for n, header in enumerate(self.moneyfundDetailMain.headerList):
                        content = c[header]
                        cell = self.moneyfundDetailMain.headerDict[header]['cellType'](content)
                        self.moneyfundDetailMain.setItem(row, n, cell)
                    row = row + 1

    def showMoneyFundSummary(self):
        """显示合约汇总数据"""
        result = self.mainEngine.get_total_fund_statistic()
        self.moneyfundSummaryView.setRowCount(len(result))
        row = 0
        for r in result:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.moneyfundSummaryView.headerList):
                content = r[header]
                cellType = self.moneyfundSummaryView.headerDict[header]['cellType']
                cell = cellType(content)
                self.moneyfundSummaryView.setItem(row, n, cell)

            row = row + 1

    def prepareMoneyfundData(self):
        """准备基金类别数据"""
        result = self.mainEngine.get_all_asset_ids_by_type(SV.ASSET_CLASS_FUND)
        print('prepareMoneyfundData', result)
        for mf in result:
            if not self.filterView.moneyfundCate_list.__contains__(mf[0]):
                self.filterView.moneyfundCate_list.append(mf[0])
                self.filterView.moneyfundCate.addItem(mf[1])
    def saveToCsv(self):

        # 先隐藏右键菜单
        self.menu.close()

        csvContent = list()
        labels = [d['chinese'] for d in self.moneyfundDetailMain.headerDict.values()]
        print('labels:', labels)
        csvContent.append(labels)
        content = self.mainEngine.get_fund_detail_by_days(7)
        print('content:', content)
        for r in content:
            # 遍历对应资产的记录
            for col in r.values():
                for c in col:
                    # 按照定义的表头，进行数据填充
                    row = list()
                    for n, header in enumerate(self.moneyfundDetailMain.headerList):
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



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    mfm = MoneyFundMain(mainEngine)
    # mflv = MoneyFundDetailView(mainEngine)
    # mainfdv = MoneyFundSummaryView(mainEngine)
    # mflv.showMaximized()
    # mainfdv.showMaximized()
    mfm.show()
    sys.exit(app.exec_())
