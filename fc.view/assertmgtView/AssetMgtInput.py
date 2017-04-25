# -*- coding: utf-8 -*-
import datetime
import re

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

from BasicWidget import BASIC_FONT, BasicFcView
from Cash import Cash
from MainEngine import MainEngine
from MoneyFund import MoneyFund, MfProjectList, MfProject
from ProtocolDeposit import ProtocolDeposit
from Valuation import Valuation


class AssetMgtInput(BasicFcView):
    """资管项目输入"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine=None, parent=None):
        """Constructor"""
        super(AssetMgtInput, self).__init__(parent=parent)

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        # self.setHeaderDict(d)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('输入资管项目字段')
        self.setMinimumSize(400, 350)
        self.setFont(BASIC_FONT)
        # self.initTable()
        self.initInput()
        # self.prepareData()
        # self.addMenuAction()

    # ----------------------------------------------------------------------
    def initInput(self):
        """设置输入框"""

        # 设置组件
        am_loan_person_Label = QLabel("借款人")
        am_loan_amount_Label = QLabel("放款金额")
        am_committee_rate_Label = QLabel("委贷利率")
        am_interested_days_Label = QLabel("全年计息天数")

        am_value_date_Label = QLabel("起息日")
        am_due_date_Label = QLabel("到期日")

        am_committee_bank_rate_Label = QLabel("委贷银行费率")
        am_c_count_interest_days_Label = QLabel("全年计息天数")
        am_channel_fee_Label = QLabel("资管通道费率")
        am_a_count_interest_days_Label = QLabel("全年计息天数")

        self.am_loan_person_Edit = QLineEdit("0.00")
        self.am_loan_amount_Edit = QLineEdit("0.00")
        self.am_committee_rate_Edit = QLineEdit("0.00")
        self.am_interested_days_Edit = QLineEdit("0.00")

        self.am_value_date_Edit = QLineEdit("2017-02-12")
        self.am_due_date_Edit = QLineEdit("2017-05-12")

        self.am_committee_bank_rate_Edit = QLineEdit("0.00")
        self.am_c_count_interest_days_Edit = QLineEdit("0.00")
        self.am_channel_fee_Edit = QLineEdit("0.00")
        self.am_a_count_interest_days_Edit = QLineEdit("0.00")

        okButton = QPushButton("新增借款")
        cancelButton = QPushButton("取消")
        okButton.clicked.connect(self.addData)
        cancelButton.clicked.connect(self.close)

        # 设置布局
        buttonHBox = QHBoxLayout()
        buttonHBox.addStretch()
        buttonHBox.addWidget(okButton)
        buttonHBox.addWidget(cancelButton)

        grid = QGridLayout()
        grid.addWidget(am_loan_person_Label, 0, 0)
        grid.addWidget(am_loan_amount_Label, 1, 0)
        grid.addWidget(am_committee_rate_Label, 2, 0)
        grid.addWidget(am_interested_days_Label, 3, 0)
        grid.addWidget(am_value_date_Label, 4, 0)
        grid.addWidget(am_due_date_Label, 5, 0)
        grid.addWidget(am_committee_bank_rate_Label, 6, 0)
        grid.addWidget(am_c_count_interest_days_Label, 7, 0)
        grid.addWidget(am_channel_fee_Label, 6, 2)
        grid.addWidget(am_a_count_interest_days_Label, 7, 2)

        grid.addWidget(self.am_loan_person_Edit, 0, 1)
        grid.addWidget(self.am_loan_amount_Edit, 1, 1)
        grid.addWidget(self.am_committee_rate_Edit, 2, 1)
        grid.addWidget(self.am_interested_days_Edit, 3, 1)

        grid.addWidget(self.am_value_date_Edit, 4, 1)
        grid.addWidget(self.am_due_date_Edit, 5, 1)

        grid.addWidget(self.am_committee_bank_rate_Edit, 6, 1)
        grid.addWidget(self.am_c_count_interest_days_Edit, 7, 1)
        grid.addWidget(self.am_channel_fee_Edit, 6, 3)
        grid.addWidget(self.am_a_count_interest_days_Edit, 7, 3)

        grid.addLayout(buttonHBox, 8, 1, 1, 2)

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

    def prepareData(self):
        result = MfProject.listAll()
        print('prepareData running.....')
        for mf in result:
            print(mf.mf_project_name)
            self.mf_ComboBox.addItem(mf.mf_project_name)

            self.mf_ComboBox_list.append(mf.uuid)
            print(str(mf.uuid) + ',' + str(mf.mf_project_name))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = AssetMgtInput(mainEngine, mainEngine.eventEngine)
    cashInput.show()
    sys.exit(app.exec_())
