# -*- coding: utf-8 -*-
import datetime

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


class MoneyFundInput(BasicFcView):
    """货基输入"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine=None, parent=None):
        """Constructor"""
        super(MoneyFundInput, self).__init__(parent=parent)

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        # self.setHeaderDict(d)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('输入货基明细')
        # self.setMinimumSize(800, 800)
        self.setFont(BASIC_FONT)
        # self.initTable()
        self.initInput()
        self.prepareData()
        # self.addMenuAction()

    # ----------------------------------------------------------------------
    def initInput(self):
        """设置输入框"""
        self.mf_ComboBox_list = list()
        # 下拉框，用来选择不同的协存项目
        mf_ComboBox_Label = QLabel("基金项目")
        self.mf_ComboBox = QComboBox()

        # 设置组件
        mf_subscribe_normal_Label = QLabel("正常申购")
        mf_subscribe_from_assert_mgt_Label = QLabel("申购(现金)")
        mf_subscribe_from_cash_Label = QLabel("申购(现金)")
        mf_redeem_normal_Label = QLabel("正常赎回")
        mf_redeem_to_assert_mgt_Label = QLabel("赎回(资管)")
        mf_redeem_to_cash_Label = QLabel("赎回(现金)")
        mf_redeem_fee_Label = QLabel("赎回(费用)")
        mf_not_carry_forward_revenue_Label = QLabel("未结转收益")
        mf_carry_forward_revenue_Label = QLabel("结转金额")

        self.mf_subscribe_normal_Edit = QLineEdit("0.00")
        self.mf_subscribe_from_assert_mgt_Edit = QLineEdit("0.00")
        self.mf_subscribe_from_cash_Edit = QLineEdit("0.00")
        self.mf_redeem_normal_Edit = QLineEdit("0.00")
        self.mf_redeem_to_assert_mgt_Edit = QLineEdit("0.00")
        self.mf_redeem_to_cash_Edit = QLineEdit("0.00")
        self.mf_redeem_fee_Edit = QLineEdit("0.00")
        self.mf_not_carry_forward_revenue_Edit = QLineEdit("0.00")
        self.mf_carry_forward_revenue_Edit = QLineEdit("0.00")

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
        grid.addWidget(mf_ComboBox_Label,0,0)
        grid.addWidget(mf_subscribe_normal_Label, 1, 0)
        grid.addWidget(mf_subscribe_from_assert_mgt_Label, 2, 0)
        grid.addWidget(mf_subscribe_from_cash_Label, 3, 0)
        grid.addWidget(mf_redeem_normal_Label, 4, 0)
        grid.addWidget(mf_redeem_to_assert_mgt_Label, 5, 0)
        grid.addWidget(mf_redeem_to_cash_Label, 6, 0)
        grid.addWidget(mf_redeem_fee_Label, 7, 0)
        grid.addWidget(mf_not_carry_forward_revenue_Label, 8, 0)
        grid.addWidget(mf_carry_forward_revenue_Label, 9, 0)

        grid.addWidget(self.mf_ComboBox,0,1)
        grid.addWidget(self.mf_subscribe_normal_Edit, 1, 1)
        grid.addWidget(self.mf_subscribe_from_assert_mgt_Edit, 2, 1)
        grid.addWidget(self.mf_subscribe_from_cash_Edit, 3, 1)
        grid.addWidget(self.mf_redeem_normal_Edit, 4, 1)
        grid.addWidget(self.mf_redeem_to_assert_mgt_Edit, 5, 1)
        grid.addWidget(self.mf_redeem_to_cash_Edit, 6, 1)
        grid.addWidget(self.mf_redeem_fee_Edit, 7, 1)
        grid.addWidget(self.mf_not_carry_forward_revenue_Edit, 8, 1)
        grid.addWidget(self.mf_carry_forward_revenue_Edit, 9, 1)
        grid.addLayout(buttonHBox, 10, 0, 1, 2)

        self.setLayout(grid)

    # ----------------------------------------------------------------------
    def addData(self):
        """增加数据"""
        mf_project_name_index = str(self.mf_ComboBox.currentIndex())

        mf_subscribe_normal = str(self.mf_subscribe_normal_Edit.text())
        mf_subscribe_from_assert_mgt = str(self.mf_subscribe_from_assert_mgt_Edit.text())
        mf_subscribe_from_cash = str(self.mf_subscribe_from_cash_Edit.text())
        mf_redeem_normal = str(self.mf_redeem_normal_Edit.text())
        mf_redeem_to_assert_mgt = str(self.mf_redeem_to_assert_mgt_Edit.text())
        mf_redeem_to_cash = str(self.mf_redeem_to_cash_Edit.text())
        mf_redeem_fee = str(self.mf_redeem_fee_Edit.text())
        mf_not_carry_forward_revenue = str(self.mf_not_carry_forward_revenue_Edit.text())
        mf_carry_forward_revenue = str(self.mf_carry_forward_revenue_Edit.text())

        mf_uuid = self.mf_ComboBox_list[int(mf_project_name_index)]
        """向数据库增加数据"""
        print(mf_subscribe_normal)
        print(mf_subscribe_from_assert_mgt)
        print(mf_subscribe_from_cash)
        print(mf_redeem_normal)
        print(mf_redeem_to_assert_mgt)
        print(mf_redeem_to_cash)
        print(mf_redeem_fee)
        print(mf_not_carry_forward_revenue)
        print(mf_carry_forward_revenue)
        d = datetime.date.today()
        mfProjectList = MfProjectList(d, mf_subscribe_normal, mf_subscribe_from_assert_mgt,mf_subscribe_from_cash,
                      mf_redeem_normal,mf_redeem_to_assert_mgt,mf_redeem_to_cash,
                      mf_redeem_fee,mf_not_carry_forward_revenue,mf_carry_forward_revenue)

        mfProjectList.save(mf_uuid)

        moneyFund = MoneyFund(datetime.date(d.year, d.month, d.day))
        moneyFund.update()

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
    cashInput = MoneyFundInput(mainEngine, mainEngine.eventEngine)
    cashInput.show()
    sys.exit(app.exec_())
