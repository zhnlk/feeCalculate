# -*- coding: utf-8 -*-
# @Author:zhnlk
# @Date:  2017/4/25
# @Email: dG9tbGVhZGVyMDgyOEBnbWFpbC5jb20=  
# @Github:github/zhnlk

import datetime
import re

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

import AssetService
from controller.EventEngine import Event
from controller.EventType import EVENT_AM_ADJUST, EVENT_AM, EVENT_MAIN_FEE, EVENT_MAIN_VALUATION
from view.BasicWidget import BASIC_FONT, BasicFcView
from controller.MainEngine import MainEngine


class AdjustValuationInput(BasicFcView):
    """资管项目输入"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine=None, parent=None):
        """Constructor"""
        super(AdjustValuationInput, self).__init__(parent=parent)

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        # self.setHeaderDict(d)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('输入资管项目字段')
        # self.setMinimumSize(400, 350)
        self.setFont(BASIC_FONT)
        # self.initTable()
        self.initInput()
        # self.prepareData()
        # self.addMenuAction()

    # ----------------------------------------------------------------------
    def initInput(self):
        """设置输入框"""

        # 设置组件
        adjust_date_Label = QLabel("调整日")
        adjust_transfer_fee_Label = QLabel("转账费用")
        adjust_check_fee_Label = QLabel("支票费用")

        self.adjust_date_Edit = QLineEdit("2017-04-20")
        self.adjust_transfer_fee_Edit = QLineEdit("0.00")
        self.adjust_check_Edit = QLineEdit("0.00")

        okButton = QPushButton("确认调整")
        cancelButton = QPushButton("取消")
        okButton.clicked.connect(self.addData)
        cancelButton.clicked.connect(self.close)

        # 设置布局
        buttonHBox = QHBoxLayout()
        buttonHBox.addStretch()
        buttonHBox.addWidget(okButton)
        buttonHBox.addWidget(cancelButton)

        grid = QGridLayout()
        grid.addWidget(adjust_date_Label, 0, 0)
        grid.addWidget(adjust_transfer_fee_Label, 1, 0)
        grid.addWidget(adjust_check_fee_Label, 2, 0)

        grid.addWidget(self.adjust_date_Edit, 0, 1)
        grid.addWidget(self.adjust_transfer_fee_Edit, 1, 1)
        grid.addWidget(self.adjust_check_Edit, 2, 1)

        grid.addLayout(buttonHBox, 3, 0, 1, 2)

        self.setLayout(grid)

    # ----------------------------------------------------------------------
    def addData(self):
        """增加数据"""
        adjust_date = str(self.adjust_date_Edit.text())
        adjust_transfer_fee = str(self.adjust_transfer_fee_Edit.text())
        adjust_check = str(self.adjust_check_Edit.text())

        # """向数据库增加数据"""

        date_str = adjust_date.split('-')
        d = datetime.date.today()
        if date_str is None:
            date = datetime.date(d.year, d.month, d.day)
        else:
            date = datetime.date(int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[0])),
                                 int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[1])),
                                 int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[2])))

        try:
            if float(adjust_check) is not 0.0:
                AssetService.add_asset_fee_with_asset_and_type(float(adjust_check), asset_id='', cal_date=date)
            if float(adjust_transfer_fee) is not 0.0:
                AssetService.add_asset_fee_with_asset_and_type(float(adjust_transfer_fee), asset_id='', cal_date=date)
        except ValueError:
            self.showError()

        # 加入数据后，更新列表显示
        self.mainEngine.eventEngine.put(Event(type_=EVENT_AM))
        self.mainEngine.eventEngine.put(Event(type_=EVENT_AM_ADJUST))
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_FEE))
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_VALUATION))
        # self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_ASSERT_DETAIL))

        self.showInfo()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = AdjustValuationInput(mainEngine, mainEngine.eventEngine)
    cashInput.show()
    sys.exit(app.exec_())
