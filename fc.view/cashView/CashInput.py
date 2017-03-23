# -*- coding: utf-8 -*-
from collections import OrderedDict
import datetime

from PyQt5.QtCore import QMetaObject
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QWidget
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import fcFunction
from BasicWidget import BASIC_FONT, BasicFcView, BasicCell
from Cash import Cash
from DataEngine import DataEngine
from MainEngine import MainEngine
from MainWindow import MainWindow


class CashInput(BasicFcView):
    """现金详情"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine=None, parent=None):
        """Constructor"""
        super(CashInput, self).__init__(parent=parent)

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        # self.setHeaderDict(d)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('输入现金明细')
        # self.setMinimumSize(800, 800)
        self.setFont(BASIC_FONT)
        # self.initTable()
        self.initInput()
        # self.addMenuAction()

    # ----------------------------------------------------------------------
    def initInput(self):
        """设置输入框"""

        # 设置组件
        cash_to_investor_Label = QLabel("现金->兑付投资人")
        investor_to_cash_Label = QLabel("投资人->现金")
        self.cash_to_investor_Edit = QLineEdit("0.00")
        self.invest_to_cash_Edit = QLineEdit("0.00")
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
        grid.addWidget(cash_to_investor_Label, 0, 0)
        grid.addWidget(investor_to_cash_Label, 1, 0)
        grid.addWidget(self.cash_to_investor_Edit, 0, 1)
        grid.addWidget(self.invest_to_cash_Edit, 1, 1)
        grid.addLayout(buttonHBox, 3, 0, 1, 2)

        self.setLayout(grid)

    # ----------------------------------------------------------------------
    def addData(self):
        """登录"""
        cash_to_investor = str(self.cash_to_investor_Edit.text())
        invest_to_cash = str(self.invest_to_cash_Edit.text())
        # self.dbConnectt()
        self.insertDB(cash_to_investor, invest_to_cash)
        # self.close()

    # ----------------------------------------------------------------------
    # def insertDB(self, editArea1, editArea2, editArea3, editArea4, editArea5):
    def insertDB(self, cash_to_investor, invest_to_cash):
        """向数据库增加数据"""
        print(cash_to_investor)
        print(invest_to_cash)
        d = datetime.date.today()
        cash = Cash(datetime.date(d.year, d.month, d.day), cash_to_investor, invest_to_cash)
        # eventEngine = EventEngine()
        dataEngine = DataEngine(self.eventEngine)
        # init_db(dataEngine.)
        dataEngine.dbConnect()
        dataEngine.dbInsert(cash)
        # result = dataEngine.dbQuery(Cash)
        # for r in result:
        #     print(r.uuid)

        # self.session.add(cash)
        #
        # # 提交即保存到数据库:
        # self.session.commit()
        # # 关闭session:
        # self.session.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = CashInput(mainEngine, mainEngine.eventEngine)
    cashInput.show()
    sys.exit(app.exec_())
