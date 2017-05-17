# -*- coding: utf-8 -*-
# @Author:zhnlk
# @Date:  2017/5/17
# @Email: dG9tbGVhZGVyMDgyOEBnbWFpbC5jb20=  
# @Github:github/zhnlk
import datetime

import re
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox, QApplication, QHBoxLayout, QGridLayout

from view.BasicWidget import BasicFcView, BASIC_FONT
from controller.EventEngine import Event
from controller.EventType import EVENT_MAIN_VALUATION, EVENT_MAIN_FEE, EVENT_MAIN_COST
from controller.MainEngine import MainEngine


class TodayCostInput(BasicFcView):
    """现金详情"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(TodayCostInput, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('输入今日资金成本')
        # self.setMinimumSize(800, 800)
        self.setFont(BASIC_FONT)
        # self.initTable()
        self.initInput()
        # self.addMenuAction()

    # ----------------------------------------------------------------------
    def initInput(self):
        """设置输入框"""

        # 设置组件
        today_cost_Label = QLabel("今日资金成本")

        date_Label = QLabel("日期")

        self.today_cost_Edit = QLineEdit("0.00")
        self.date_Edit = QLineEdit(str(datetime.date.today()))

        okButton = QPushButton("确定")
        cancelButton = QPushButton("取消")
        okButton.clicked.connect(self.addData)
        cancelButton.clicked.connect(self.close)

        # 设置布局
        buttonHBox = QHBoxLayout()
        buttonHBox.addStretch()
        buttonHBox.addWidget(okButton)
        buttonHBox.addWidget(cancelButton)

        grid = QGridLayout()
        grid.addWidget(today_cost_Label, 0, 0)
        grid.addWidget(date_Label, 1, 0)

        grid.addWidget(self.today_cost_Edit, 0, 1)
        grid.addWidget(self.date_Edit, 1, 1)
        grid.addLayout(buttonHBox, 2, 0, 1, 2)

        self.setLayout(grid)

    # ----------------------------------------------------------------------
    def addData(self):
        """增加数据"""
        today_cost = str(self.today_cost_Edit.text())
        if today_cost == '':
            today_cost = '0.00'

        date_str = str(self.date_Edit.text()).split('-')
        d = datetime.date.today()
        if date_str is None:
            date = datetime.date(d.year, d.month, d.day)
        else:
            date = datetime.date(int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[0])),
                                 int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[1])),
                                 int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[2])))
        if date > d:
            self.showError()
            return
        # print(cash_to_investor, extract_fee, invest_to_cash, cash_revenue)
        try:
            self.mainEngine.add_asset_fee_with_asset_and_type(amount=float(today_cost),cal_date=date)
        except ValueError:
            self.showError()
            return

        # 加入数据后，更新列表显示
        # self.mainEngine.eventEngine.put(Event(type_=EVENT_CASH))
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_COST))
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_FEE))
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_VALUATION))
        # self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_ASSERT_DETAIL))

        self.showInfo()

    # 输入成功提示框
    def showInfo(self):
        print('slotInformation called...')
        QMessageBox.information(self, "Information",
                                self.tr("输入成功!"))
        self.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = TodayCostInput(mainEngine)
    cashInput.show()
    sys.exit(app.exec_())
