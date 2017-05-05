# -*- coding: utf-8 -*-
import datetime
import re

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

from EventEngine import Event
from EventType import EVENT_AM, EVENT_MAIN_FEE, EVENT_MAIN_VALUATION, EVENT_AM_INPUT
from view.BasicWidget import BASIC_FONT, BasicFcView
from controller.MainEngine import MainEngine


class AssetMgtInput(BasicFcView):
    """资管项目输入"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine=None, parent=None):
        """Constructor"""
        super(AssetMgtInput, self).__init__(parent=parent)

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        self.setEventType(EVENT_AM_INPUT)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('输入资管项目字段')
        self.setMinimumSize(400, 350)
        self.setFont(BASIC_FONT)
        # self.initTable()
        self.initInput()

    # ----------------------------------------------------------------------
    def initInput(self):
        """设置输入框"""

        # 设置组件
        am_name_Label = QLabel("借款方")
        am_trade_amount_Label = QLabel("放款金额")
        am_ret_rate_Label = QLabel("委贷利率")
        am_rate_days_Label = QLabel("全年计息天数")

        am_start_date_Label = QLabel("起息日")
        am_end_date_Label = QLabel("到期日")

        am_bank_fee_rate_Label = QLabel("委贷银行费率")
        am_bank_days_Label = QLabel("全年计息天数")
        am_manage_fee_rate = QLabel("资管通道费率")
        am_manage_days_Label = QLabel("全年计息天数")

        self.am_name_Edit = QLineEdit("借款方")
        self.am_trade_amount_Edit = QLineEdit("300000")
        self.am_ret_rate_Edit = QLineEdit("0.009")
        self.am_rate_days_Edit = QLineEdit("360")

        self.am_start_date_Edit = QLineEdit("2017-02-12")
        self.am_end_date_Edit = QLineEdit("2017-05-12")

        self.am_bank_fee_rate_Edit = QLineEdit("0.003")
        self.am_bank_days_Edit = QLineEdit("360")
        self.am_manage_fee_rate_Edit = QLineEdit("0.005")
        self.am_manage_days_Edit = QLineEdit("360")

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
        grid.addWidget(am_name_Label, 0, 0)
        grid.addWidget(am_trade_amount_Label, 1, 0)
        grid.addWidget(am_ret_rate_Label, 2, 0)
        grid.addWidget(am_rate_days_Label, 3, 0)
        grid.addWidget(am_start_date_Label, 4, 0)
        grid.addWidget(am_end_date_Label, 5, 0)
        grid.addWidget(am_bank_fee_rate_Label, 6, 0)
        grid.addWidget(am_bank_days_Label, 7, 0)
        grid.addWidget(am_manage_fee_rate, 6, 2)
        grid.addWidget(am_manage_days_Label, 7, 2)

        grid.addWidget(self.am_name_Edit, 0, 1)
        grid.addWidget(self.am_trade_amount_Edit, 1, 1)
        grid.addWidget(self.am_ret_rate_Edit, 2, 1)
        grid.addWidget(self.am_rate_days_Edit, 3, 1)

        grid.addWidget(self.am_start_date_Edit, 4, 1)
        grid.addWidget(self.am_end_date_Edit, 5, 1)

        grid.addWidget(self.am_bank_fee_rate_Edit, 6, 1)
        grid.addWidget(self.am_bank_days_Edit, 7, 1)
        grid.addWidget(self.am_manage_fee_rate_Edit, 6, 3)
        grid.addWidget(self.am_manage_days_Edit, 7, 3)

        grid.addLayout(buttonHBox, 8, 1, 1, 2)

        self.setLayout(grid)

    # ----------------------------------------------------------------------
    def addData(self):
        """增加数据"""
        am_name = str(self.am_name_Edit.text())
        am_trade_amount = str(self.am_trade_amount_Edit.text())
        am_ret_rate = str(self.am_ret_rate_Edit.text())
        am_rate_days = str(self.am_rate_days_Edit.text())
        am_start_date = str(self.am_start_date_Edit.text())
        am_end_date = str(self.am_end_date_Edit.text())
        am_bank_fee = str(self.am_bank_fee_rate_Edit.text())
        am_bank_days = str(self.am_bank_days_Edit.text())
        am_manage_fee_rate = str(self.am_manage_fee_rate_Edit.text())
        am_manage_days = str(self.am_manage_days_Edit.text())
        """向数据库增加数据"""

        start_date_str = am_start_date.split('-')
        end_date_str = am_end_date.split('-')

        # print(start_date_str[0], end_date_str[0])

        d = datetime.date.today()
        if start_date_str is None or end_date_str is None:
            start_date = datetime.date(d.year, d.month, d.day)
            end_date = datetime.date(d.year, d.month, d.day)
        else:
            start_date = datetime.date(int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", start_date_str[0])),
                                       int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", start_date_str[1])),
                                       int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", start_date_str[2])))
            end_date = datetime.date(int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", end_date_str[0])),
                                     int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", end_date_str[1])),
                                     int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", end_date_str[2])))
        try:
            self.mainEngine.add_management_class(am_name, float(am_trade_amount), float(am_ret_rate), float(am_rate_days), start_date, end_date,
                                             float(am_bank_fee), float(am_bank_days), float(am_manage_fee_rate), float(am_manage_days))
        except ValueError:
            self.showError()
            return

        # 加入数据后，更新列表显示
        self.mainEngine.eventEngine.put(Event(type_=EVENT_AM))
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_FEE))
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_VALUATION))
        # self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_ASSERT_DETAIL))

        self.showInfo()

    # 输入成功提示框
    def showInfo(self):
        print('slotInformation called...')
        QMessageBox.information(self, "Information",
                                self.tr("输入成功!"))
        self.close()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = AssetMgtInput(mainEngine, mainEngine.eventEngine)
    cashInput.show()
    sys.exit(app.exec_())
