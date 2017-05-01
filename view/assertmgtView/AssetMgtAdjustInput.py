# -*- coding: utf-8 -*-
# @Author:zhnlk
# @Date:  2017/4/25
# @Email: dG9tbGVhZGVyMDgyOEBnbWFpbC5jb20=  
# @Github:github/zhnlk

import datetime
import re

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

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
        # mf_project_name_index = str(self.mf_ComboBox.currentIndex())
        #
        # mf_subscribe_from_cash = str(self.mf_subscribe_from_cash_Edit.text())
        # mf_redeem_to_cash = str(self.mf_redeem_to_cash_Edit.text())
        # mf_not_carry_forward_revenue = str(self.mf_not_carry_forward_revenue_Edit.text())
        # mf_carry_forward_revenue = str(self.mf_carry_forward_revenue_Edit.text())
        #
        # mf_uuid = self.mf_ComboBox_list[int(mf_project_name_index)]
        # """向数据库增加数据"""
        #
        # date_str = str(self.date_Edit.text()).split('-')
        # d = datetime.date.today()
        # if date_str is None:
        #     date = datetime.date(d.year, d.month, d.day)
        # else:
        #     date = datetime.date(int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[0])),
        #                          int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[1])),
        #                          int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[2])))
        #
        # mfProjectList = MfProjectList(date,mf_subscribe_from_cash,mf_redeem_to_cash,mf_not_carry_forward_revenue,mf_carry_forward_revenue)
        #
        # mfProjectList.save(mf_uuid)
        #
        # moneyFund = MoneyFund(date)
        # moneyFund.update()
        #
        # v = Valuation(date)
        # v.save()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = AdjustValuationInput(mainEngine, mainEngine.eventEngine)
    cashInput.show()
    sys.exit(app.exec_())
