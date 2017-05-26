# -*- coding: utf-8 -*-
# @Author:zhnlk
# @Date:  2017/5/25
# @Email: dG9tbGVhZGVyMDgyOEBnbWFpbC5jb20=  
# @Github:github/zhnlk

# -*- coding: utf-8 -*-
# @Author:zhnlk
# @Date:  2017/4/25
# @Email: dG9tbGVhZGVyMDgyOEBnbWFpbC5jb20=
# @Github:github/zhnlk
import datetime
from collections import OrderedDict

import re
from PyQt5.QtWidgets import QAction, QLabel, QLineEdit, QPushButton, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QApplication

from utils.Utils import strToDate
from controller.EventEngine import Event
from view.BasicWidget import BASIC_FONT, BasicFcView, BasicCell, NumCell
from controller.EventType import EVENT_PD, EVENT_ADJUST_VIEW, EVENT_MODIFY_CASH_VIEW
from controller.MainEngine import MainEngine


class CashDataModifyView(BasicFcView):
    """协存详情"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, dateToModified,parent=None):
        """Constructor"""
        super(CashDataModifyView, self).__init__(parent=parent)

        self.mainEngine = mainEngine
        # self.dateToModified = strToDate(dateToModified)
        self.dateToModified = dateToModified
        self.widgetDict = {}  # 保存子窗口
        d = OrderedDict()
        d['date'] = {'chinese': '日期', 'cellType': BasicCell}
        d['type'] = {'chinese': '类型', 'cellType': BasicCell}
        d['amount'] = {'chinese': '金额', 'cellType': NumCell}
        # d['pd_pd_to_cash'] = {'chinese': '调整结果', 'cellType': NumCell}

        self.setHeaderDict(d)

        self.eventType = EVENT_MODIFY_CASH_VIEW
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

    def showModifyListDetail(self,dateToModified):
        """显示所有合约数据"""
        result = self.mainEngine.get_cash_input_detail_by_date_dic(dateToModified)
        self.setRowCount(len(result))
        row = 0

        for r in result:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.headerList):
                content = r[header]

                cellType = self.headerDict[header]['cellType']
                cell = cellType(content)
                if self.saveData and header is 'amount':
                    cell.data = (r['id'], r['date'], r['type'], r['amount'])
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

    def refresh(self):
        """刷新"""
        # self.menu.close()  # 关闭菜单
        self.clearContents()
        self.setRowCount(0)
        self.showModifyListDetail(self.dateToModified)

    def addMenuAction(self):
        """增加右键菜单内容"""
        refreshAction = QAction('刷新', self)
        refreshAction.triggered.connect(self.refresh)

        # self.menu.addAction(refreshAction)

    def closeEvent(self, event):
        for widget in self.widgetDict.values():
            widget.close()

        event.accept()

    def show(self):
        """显示"""
        super(CashDataModifyView, self).show()
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
        print('init Input ',self.data)
        # cash_id, date,type,amount = self.data

        self.modify_date_Edit = QLineEdit(str(self.data[1]))
        self.modify_date_Edit.setReadOnly(True)
        self.modify_type_Edit = QLineEdit(str(self.data[2]))
        self.modify_type_Edit.setReadOnly(True)
        self.modify_amount_Edit = QLineEdit(str(self.data[3]))

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

            self.mainEngine.update_cash_input_by_id_type(cash_id=self.data[0],
                                                         amount=float(modify_amount),
                                                         cash_type=modify_type,
                                                         cal_date=strToDate(modify_date))
        except ValueError:
            self.showError()

        ### 发送修改后的触发信号
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MODIFY_CASH_VIEW))

        self.showInfo()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    plv = CashDataModifyView(mainEngine,datetime.date(2017, 5, 25))
    plv.show()
    sys.exit(app.exec_())
