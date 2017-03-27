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
from ProtocolDeposit import ProtocolDeposit, PdProject


class ProtocolInput(BasicFcView):
    """协存输入"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine=None, parent=None):
        """Constructor"""
        super(ProtocolInput, self).__init__(parent=parent)

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        # self.setHeaderDict(d)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('输入协存明细')
        # self.setMinimumSize(800, 800)
        self.setFont(BASIC_FONT)
        # self.initTable()
        self.initInput()
        self.prepareData()
        # self.addMenuAction()

    # ----------------------------------------------------------------------
    def initInput(self):
        """设置输入框"""

        # 下拉框，用来选择不同的协存项目
        pd_ComboBox_Label = QLabel("协存项目")
        self.pd_ComboBox = QComboBox()


        # 设置组件
        interest_to_principal_Label = QLabel("利息结转本金")
        investor_to_pd_Label = QLabel("投资人资金->协存")
        cash_to_pd_Label = QLabel("现金->协存")
        pd_to_investor_Label = QLabel("协存->兑付投资人")
        pd_to_cash_Label = QLabel("协存->现金")

        self.interest_to_principal_Edit = QLineEdit("0.00")
        self.investor_to_pd_Edit = QLineEdit("0.00")
        self.cash_to_pd_Edit = QLineEdit("0.00")
        self.pd_to_investor_Edit = QLineEdit("0.00")
        self.pd_to_cash_Edit = QLineEdit("0.00")
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
        grid.addWidget(pd_ComboBox_Label,0,0)
        grid.addWidget(interest_to_principal_Label, 1, 0)
        grid.addWidget(investor_to_pd_Label, 2, 0)
        grid.addWidget(cash_to_pd_Label, 3, 0)
        grid.addWidget(pd_to_investor_Label, 4, 0)
        grid.addWidget(pd_to_cash_Label, 5, 0)
        grid.addWidget(self.pd_ComboBox,0,1)
        grid.addWidget(self.interest_to_principal_Edit, 1, 1)
        grid.addWidget(self.investor_to_pd_Edit, 2, 1)
        grid.addWidget(self.cash_to_pd_Edit, 3, 1)
        grid.addWidget(self.pd_to_investor_Edit, 4, 1)
        grid.addWidget(self.pd_to_cash_Edit, 5, 1)
        grid.addLayout(buttonHBox, 6, 0, 1, 2)

        self.setLayout(grid)

    # ----------------------------------------------------------------------
    def addData(self):
        """增加数据"""
        interest_to_principal = str(self.interest_to_principal_Edit.text())
        investor_to_pd = str(self.investor_to_pd_Edit.text())
        cash_to_pd = str(self.cash_to_pd_Edit.text())
        pd_to_investor = str(self.pd_to_investor_Edit.text())
        pd_to_cash = str(self.pd_to_cash_Edit.text())
        self.insertDB(interest_to_principal, investor_to_pd, cash_to_pd, pd_to_investor, pd_to_cash)

    # ----------------------------------------------------------------------
    def prepareData(self):

        # self.pd_ComboBox.addItem('测试1')
        # self.pd_ComboBox.addItem('测试2')
        dataEngine = DataEngine(self.eventEngine)
        dataEngine.dbConnect()
        for pd in dataEngine.dbQuery(PdProject):

            self.pd_ComboBox.addItem(pd.pd_project_name)
            print(pd.pd_project_name)


    def insertDB(self, interest_to_principal, investor_to_pd, cash_to_pd, pd_to_investor, pd_to_cash):
        """向数据库增加数据"""
        print(interest_to_principal)
        print(investor_to_pd)
        print(cash_to_pd)
        print(pd_to_investor)
        print(pd_to_cash)
        d = datetime.date.today()
        pdProject = PdProject.set_params(datetime.date(d.year, d.month, d.day),interest_to_principal, investor_to_pd, cash_to_pd, pd_to_investor, pd_to_cash)

        dataEngine = DataEngine(self.eventEngine)
        dataEngine.dbConnect()
        dataEngine.dbInsert(pdProject)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = ProtocolInput(mainEngine, mainEngine.eventEngine)
    cashInput.show()
    sys.exit(app.exec_())
