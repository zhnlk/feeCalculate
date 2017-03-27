# -*- coding: utf-8 -*-
import datetime

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

from BasicWidget import BASIC_FONT, BasicFcView
from Cash import Cash
from DataEngine import DataEngine
from MainEngine import MainEngine
from MoneyFund import MoneyFund
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
        # self.addMenuAction()

    # ----------------------------------------------------------------------
    def initInput(self):
        """设置输入框"""

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
        grid.addWidget(mf_subscribe_normal_Label, 0, 0)
        grid.addWidget(mf_subscribe_from_assert_mgt_Label, 1, 0)
        grid.addWidget(mf_subscribe_from_cash_Label, 2, 0)
        grid.addWidget(mf_redeem_normal_Label, 3, 0)
        grid.addWidget(mf_redeem_to_assert_mgt_Label, 4, 0)
        grid.addWidget(mf_redeem_to_cash_Label, 5, 0)
        grid.addWidget(mf_redeem_fee_Label, 6, 0)
        grid.addWidget(mf_not_carry_forward_revenue_Label, 7, 0)
        grid.addWidget(mf_carry_forward_revenue_Label, 8, 0)

        grid.addWidget(self.mf_subscribe_normal_Edit, 0, 1)
        grid.addWidget(self.mf_subscribe_from_assert_mgt_Edit, 1, 1)
        grid.addWidget(self.mf_subscribe_from_cash_Edit, 2, 1)
        grid.addWidget(self.mf_redeem_normal_Edit, 3, 1)
        grid.addWidget(self.mf_redeem_to_assert_mgt_Edit, 4, 1)
        grid.addWidget(self.mf_redeem_to_cash_Edit, 5, 1)
        grid.addWidget(self.mf_redeem_fee_Edit, 6, 1)
        grid.addWidget(self.mf_not_carry_forward_revenue_Edit, 7, 1)
        grid.addWidget(self.mf_carry_forward_revenue_Edit, 8, 1)
        grid.addLayout(buttonHBox, 9, 0, 1, 2)

        self.setLayout(grid)

    # ----------------------------------------------------------------------
    def addData(self):
        """增加数据"""

        mf_subscribe_normal = str(self.mf_subscribe_normal_Edit.text())
        mf_subscribe_from_assert_mgt = str(self.mf_subscribe_from_assert_mgt_Edit.text())
        mf_subscribe_from_cash = str(self.mf_subscribe_from_cash_Edit.text())
        mf_redeem_normal = str(self.mf_redeem_normal_Edit.text())
        mf_redeem_to_assert_mgt = str(self.mf_redeem_to_assert_mgt_Edit.text())
        mf_redeem_to_cash = str(self.mf_redeem_to_cash_Edit.text())
        mf_redeem_fee = str(self.mf_redeem_fee_Edit.text())
        mf_not_carry_forward_revenue = str(self.mf_not_carry_forward_revenue_Edit.text())
        mf_carry_forward_revenue = str(self.mf_carry_forward_revenue_Edit.text())

        self.insertDB(mf_subscribe_normal, mf_subscribe_from_assert_mgt,mf_subscribe_from_cash,
                      mf_redeem_normal,mf_redeem_to_assert_mgt,mf_redeem_to_cash,
                      mf_redeem_fee,mf_not_carry_forward_revenue,mf_carry_forward_revenue)

    # ----------------------------------------------------------------------
    def insertDB(self, mf_subscribe_normal, mf_subscribe_from_assert_mgt,mf_subscribe_from_cash,
                      mf_redeem_normal,mf_redeem_to_assert_mgt,mf_redeem_to_cash,
                      mf_redeem_fee,mf_not_carry_forward_revenue,mf_carry_forward_revenue):
        """向数据库增加数据"""
        # print(cash_to_investor)
        # print(invest_to_cash)
        d = datetime.date.today()
        pd = ProtocolDeposit()
        cash = Cash(datetime.date(d.year, d.month, d.day), cash_to_investor, invest_to_cash)

        MoneyFund()

        dataEngine = DataEngine(self.eventEngine)
        dataEngine.dbConnect()
        dataEngine.dbInsert(cash)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = MoneyFundInput(mainEngine, mainEngine.eventEngine)
    cashInput.show()
    sys.exit(app.exec_())
