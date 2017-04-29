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
from MainEngine import MainEngine

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
        self.am_trade_amount_Edit = QLineEdit("0.003")
        self.am_ret_rate_Edit = QLineEdit("0.00")
        self.am_rate_days_Edit = QLineEdit("0.00")

        self.am_start_date_Edit = QLineEdit("2017-02-12")
        self.am_end_date_Edit = QLineEdit("2017-05-12")

        self.am_bank_fee_rate_Edit = QLineEdit("0.003")
        self.am_bank_days_Edit = QLineEdit("0.00")
        self.am_manage_fee_rate_Edit = QLineEdit("0.005")
        self.am_manage_days_Edit = QLineEdit("0.00")

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
        am_name = str(self.am_name_Edit)
        am_trade_amount = str(self.am_trade_amount_Edit)
        am_ret_rate = str(self.am_ret_rate_Edit)
        am_rate_days = str(self.am_rate_days_Edit)
        am_start_date = str(self.am_start_date_Edit)
        am_end_date = str(self.am_end_date_Edit)
        am_bank_fee = str(self.am_bank_fee_rate_Edit)
        am_bank_days = str(self.am_bank_days_Edit)
        am_manage_fee_rate = str(self.am_manage_fee_rate_Edit)
        am_manage_days = str(self.am_manage_days_Edit)
        """向数据库增加数据"""

        start_date_str = str(self.am_start_date.text()).split('-')
        end_date_str = str(self.am_end_date.text()).split('-')

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

        self.mainEngine.add_management_class(am_name, am_trade_amount, am_ret_rate, am_rate_days, start_date, end_date,
                                             am_bank_fee, am_bank_days, am_manage_fee_rate, am_manage_days)

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
