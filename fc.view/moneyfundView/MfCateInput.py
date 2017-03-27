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
from DataEngine import DataEngine
from MainEngine import MainEngine
from MoneyFund import MfProject
from ProtocolDeposit import ProtocolDeposit, PdProject


class MfCateInput(BasicFcView):
    """协存输入"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine=None, parent=None):
        """Constructor"""
        super(MfCateInput, self).__init__(parent=parent)

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        # self.setHeaderDict(d)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('输入货基项目')
        # self.setMinimumSize(800, 800)
        self.setFont(BASIC_FONT)
        # self.initTable()
        self.initInput()
        # self.addMenuAction()

    # ----------------------------------------------------------------------
    def initInput(self):
        """设置输入框"""

        # 下拉框，用来选择不同的协存项目
        # 设置组件
        mf_project_name_Label = QLabel("协存项目名称")
        mf_project_amount_Label = QLabel("协存项目金额")
        mf_project_revenue_Label = QLabel("协存项目收益")
        mf_subscribe_amount_Label = QLabel("申购总额")
        mf_redeem_amount_Label = QLabel("赎回总额")

        self.mf_project_name_Edit = QLineEdit('广发基金')
        self.mf_project_amount_Edit = QLineEdit("0.00")
        self.mf_project_revenue_Edit = QLineEdit("0.00")
        self.mf_subscribe_amount_Edit = QLineEdit("0.00")
        self.mf_redeem_amount_Edit = QLineEdit("0.00")

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
        grid.addWidget(mf_project_name_Label, 0, 0)
        grid.addWidget(mf_project_amount_Label, 1, 0)
        grid.addWidget(mf_project_revenue_Label, 2, 0)
        grid.addWidget(mf_subscribe_amount_Label, 3, 0)
        grid.addWidget(mf_redeem_amount_Label, 4, 0)
        grid.addWidget(self.mf_project_name_Edit, 0, 1)
        grid.addWidget(self.mf_project_amount_Edit, 1, 1)
        grid.addWidget(self.mf_project_revenue_Edit, 2, 1)
        grid.addWidget(self.mf_subscribe_amount_Edit, 3, 1)
        grid.addWidget(self.mf_redeem_amount_Edit, 4, 1)
        grid.addLayout(buttonHBox, 5, 0, 1, 2)

        self.setLayout(grid)

    # ----------------------------------------------------------------------
    def addData(self):
        """增加数据"""

        mf_project_name = str(self.mf_project_name_Edit.text())
        mf_project_amount = str(self.mf_project_amount_Edit.text())
        mf_project_revenue = str(self.mf_project_revenue_Edit.text())
        mf_subscribe_amount = str(self.mf_subscribe_amount_Edit.text())
        mf_redeem_amount = str(self.mf_redeem_amount_Edit.text())
        self.insertDB(mf_project_name, mf_project_amount, mf_project_revenue, mf_subscribe_amount, mf_redeem_amount)

    # ----------------------------------------------------------------------
    def insertDB(self, mf_project_name, mf_project_amount, mf_project_revenue, mf_subscribe_amount, mf_redeem_amount):
        """向数据库增加数据"""
        print(mf_project_name)
        print(mf_project_amount)
        print(mf_project_revenue)
        print(mf_subscribe_amount)
        print(mf_redeem_amount)
        d = datetime.date.today()
        mfProject = MfProject(mf_project_name)

        dataEngine = DataEngine(self.eventEngine)
        dataEngine.dbConnect()
        # dataEngine.dbQuery()
        dataEngine.dbInsert(mfProject)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = MfCateInput(mainEngine, mainEngine.eventEngine)
    cashInput.show()
    sys.exit(app.exec_())
