# -*- coding: utf-8 -*-
# @Author:zhnlk
# @Date:  2017/5/26
# @Email: dG9tbGVhZGVyMDgyOEBnbWFpbC5jb20=  
# @Github:github/zhnlk

import datetime
from collections import OrderedDict

from PyQt5.QtWidgets import QLabel, QAction, QLineEdit, QPushButton, QHBoxLayout, QGridLayout, QApplication

from view.BasicWidget import BasicFcView, BasicCell, NumCell, BASIC_FONT
from controller.EventEngine import Event
from controller.EventType import EVENT_MAIN_VALUATION, EVENT_MF, EVENT_MODIFY_MF_VIEW
from controller.MainEngine import MainEngine
from utils.Utils import strToDate, fund_type_to_key, fund_key_to_type


class FundDataModifyView(BasicFcView):
    """协存详情"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, data, parent=None):
        """Constructor"""
        super(FundDataModifyView, self).__init__(parent=parent)

        self.mainEngine = mainEngine
        self.asset_id = data[0]
        self.dateToModified = data[1]

        self.widgetDict = {}  # 保存子窗口
        d = OrderedDict()
        d['date'] = {'chinese': '日期', 'cellType': BasicCell}
        d['type'] = {'chinese': '类型', 'cellType': BasicCell}
        d['amount'] = {'chinese': '金额', 'cellType': NumCell}
        # d['pd_pd_to_cash'] = {'chinese': '调整结果', 'cellType': NumCell}

        self.setHeaderDict(d)

        self.eventType = EVENT_MODIFY_MF_VIEW
        self.initUi()

    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('估值调整明细')
        self.setMinimumSize(600, 200)
        self.setFont(BASIC_FONT)
        self.initTable()
        self.verticalHeader().setVisible(True)
        # self.addMenuAction()
        self.saveData = True
        self.connectSignal()
        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(self.eventType, self.signal.emit)

    def showModifyListDetail(self, asset_id, dateToModified):
        """显示所有合约数据"""
        result = self.mainEngine.get_fund_input_by_id_date_dic(fund_id=asset_id,
                                                               cal_date=dateToModified)
        self.setRowCount(len(result))
        row = 0

        for r in result:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.headerList):
                content = r[header]
                if header is 'type':
                    content = fund_type_to_key(r['is_asset'],content)
                if header is 'amount':
                    if r['type'] is 1 and r['is_asset'] is False:
                        content = r['not_carry_amount']
                    else:
                        content = r['amount']
                cellType = self.headerDict[header]['cellType']
                cell = cellType(content)
                if self.saveData:
                    cell.data = (r['id'], r['date'], content, r['type'], r['is_asset'])
                self.setItem(row, n, cell)

            row = row + 1

    def connectSignal(self):
        self.itemDoubleClicked.connect(self.doubleClickTrigger)

    def doubleClickTrigger(self, cell):
        try:
            # 仅支持对金额进行修改
            self.showModifyInput(data=cell.data)
        except TypeError:
            pass

    def showModifyInput(self, data):
        self.widgetDict['showModifyInput'] = ModifyInput(self.mainEngine, data=data)
        self.widgetDict['showModifyInput'].show()

    def refresh(self, data=None):
        """带参数刷新"""
        self.clearContents()
        self.setRowCount(0)
        self.showModifyListDetail(self.asset_id, self.dateToModified)

    def closeEvent(self, event):
        for widget in self.widgetDict.values():
            widget.close()

        event.accept()
        self.close()

    def show(self, data=None):
        """显示"""
        super(FundDataModifyView, self).show()
        if data is not None:
            self.asset_id = data[0]
            self.dateToModified = data[1]
        self.refresh()


class ModifyInput(BasicFcView):
    def __init__(self, mainEngine, data, parent=None):
        super(ModifyInput, self).__init__(parent=parent)
        self.mainEngine = mainEngine
        self.eventEngine = mainEngine.eventEngine
        self.setWindowTitle("修改数据明细")
        self.data = data
        self.initInput()

    def initInput(self):
        """修改的界面初始化"""
        modify_date_Label = QLabel("日期")
        modify_type_Label = QLabel("类型")
        modify_amount_Label = QLabel("金额")
        print('init Input ', self.data)

        self.modify_date_Edit = QLineEdit(str(self.data[1]))
        self.modify_date_Edit.setReadOnly(True)
        self.modify_type_Edit = QLineEdit(str(fund_type_to_key(self.data[4],self.data[3])))
        self.modify_type_Edit.setReadOnly(True)
        self.modify_amount_Edit = QLineEdit(str(self.data[2]))

        okButton = QPushButton("确认修改")
        cancelButton = QPushButton("取消")
        okButton.clicked.connect(self.updateData)
        cancelButton.clicked.connect(self.close)

        # 设置布局
        buttonHBox = QHBoxLayout()
        buttonHBox.addStretch()
        buttonHBox.addWidget(okButton)
        buttonHBox.addWidget(cancelButton)

        grid = QGridLayout()
        grid.addWidget(modify_date_Label, 0, 0)
        grid.addWidget(modify_type_Label, 1, 0)
        grid.addWidget(modify_amount_Label, 2, 0)

        grid.addWidget(self.modify_date_Edit, 0, 1)
        grid.addWidget(self.modify_type_Edit, 1, 1)
        grid.addWidget(self.modify_amount_Edit, 2, 1)

        grid.addLayout(buttonHBox, 3, 0, 1, 2)
        self.setLayout(grid)

    def updateData(self):
        """更新数据"""
        modify_date = self.modify_date_Edit.text()
        modify_type = self.modify_type_Edit.text()
        modify_amount = self.modify_amount_Edit.text()

        try:

            self.mainEngine.update_fund_input_by_id_date(fund_trade_id=self.data[0],
                                                         cal_date=strToDate(modify_date),
                                                         amount=float(modify_amount),
                                                         is_asset=self.data[4])
        except ValueError:
            self.showError()

        ### 发送修改后的触发信号
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MODIFY_MF_VIEW))
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MF))
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_VALUATION))

        self.showInfo()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    plv = FundDataModifyView(mainEngine=mainEngine, dateToModified=datetime.date(2017, 5, 25))
    plv.show()
    sys.exit(app.exec_())
