# -*- coding: utf-8 -*-
import datetime

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

from BasicWidget import BASIC_FONT, BasicFcView
from Cash import Cash
from EventEngine import Event
from EventType import EVENT_CASH
from MainEngine import MainEngine


class CashInput(BasicFcView):
    """现金详情"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(CashInput, self).__init__(parent=parent)

        self.mainEngine = mainEngine

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
        """增加数据"""
        cash_to_investor = str(self.cash_to_investor_Edit.text())
        if cash_to_investor == '':
            cash_to_investor = '0.00'
        invest_to_cash = str(self.invest_to_cash_Edit.text())
        if invest_to_cash == '':
            invest_to_cash = '0.00'

        """向数据库增加数据"""
        print(cash_to_investor)
        print(invest_to_cash)
        d = datetime.date.today()
        cash = Cash(datetime.date(d.year, d.month, d.day), cash_to_investor, invest_to_cash)
        cash.total_cash = Cash.getTodayTotalCash(datetime.date(d.year, d.month, d.day))
        cash.save()

        # self.mainEngine.eventEngine.put(EVENT_CASH)
        # self.connect(okButton, SIGNAL("clicked()"), self.slotInformation)
        self.signal.emit(Event(EVENT_CASH))

    # 输入成功提示框
    def slotInformation(self):
        QMessageBox.information(self, "Information",
                                self.tr("输入成功!"))
        self.label.setText("Information MessageBox")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = CashInput(mainEngine)
    cashInput.show()
    sys.exit(app.exec_())
