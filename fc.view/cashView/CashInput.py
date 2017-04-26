# -*- coding: utf-8 -*-
import datetime
import re

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
from Valuation import Valuation


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
        extract_fee_Label = QLabel("提取费用")
        investor_to_cash_Label = QLabel("投资人->现金")
        cash_revenue_Label = QLabel("现金收入")

        date_Label = QLabel("日期")

        self.cash_to_investor_Edit = QLineEdit("0.00")
        self.extract_fee_Edit = QLineEdit("0.00")
        self.invest_to_cash_Edit = QLineEdit("0.00")
        self.cash_revenue_Edit = QLineEdit("0.00")
        self.date_Edit = QLineEdit("2017-01-01")

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
        grid.addWidget(extract_fee_Label, 1, 0)
        grid.addWidget(investor_to_cash_Label, 2, 0)
        grid.addWidget(cash_revenue_Label, 3, 0)
        grid.addWidget(date_Label, 4, 0)

        grid.addWidget(self.cash_to_investor_Edit, 0, 1)
        grid.addWidget(self.extract_fee_Edit, 1, 1)
        grid.addWidget(self.invest_to_cash_Edit, 2, 1)
        grid.addWidget(self.cash_revenue_Edit, 3, 1)
        grid.addWidget(self.date_Edit, 4, 1)
        grid.addLayout(buttonHBox, 6, 0, 1, 2)

        self.setLayout(grid)

    # ----------------------------------------------------------------------
    def addData(self):
        """增加数据"""
        cash_to_investor = str(self.cash_to_investor_Edit.text())
        if cash_to_investor == '':
            cash_to_investor = '0.00'

        extract_fee = str(self.extract_fee_Edit.text())
        if extract_fee == '':
            extract_fee = '0.00'

        invest_to_cash = str(self.invest_to_cash_Edit.text())
        if invest_to_cash == '':
            invest_to_cash = '0.00'

        cash_revenue = str(self.cash_revenue_Edit.text())
        if cash_revenue == '':
            cash_revenue = '0.00'

        date_str = str(self.date_Edit.text()).split('-')
        d = datetime.date.today()
        if date_str is None:
            date = datetime.date(d.year, d.month, d.day)
        else:
            date = datetime.date(int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[0])),
                                 int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[1])),
                                 int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[2])))

        """向数据库增加数据"""
        print(cash_to_investor, extract_fee, invest_to_cash, cash_revenue)
        mainEngine.add_cash_daily_data(cash_to_investor, extract_fee, invest_to_cash, cash_revenue)

        v = Valuation(date)
        v.save()

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
