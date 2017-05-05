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
from EventType import EVENT_MF, EVENT_MAIN_FEE, EVENT_MAIN_VALUATION, EVENT_MF_INPUT
from view.BasicWidget import BASIC_FONT, BasicFcView
from controller.MainEngine import MainEngine
from utils import StaticValue as SV


class MoneyFundInput(BasicFcView):
    """货基输入"""

    def __init__(self, mainEngine, eventEngine=None, parent=None):
        """Constructor"""
        super(MoneyFundInput, self).__init__(parent=parent)

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        self.setEventType(EVENT_MF_INPUT)

        self.initUi()

    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('输入货基明细')
        # self.setMinimumSize(800, 800)
        self.setFont(BASIC_FONT)
        self.initInput()
        self.prepareData()

        # self.signal.connect(self.prepareData)
        # self.mainEngine.eventEngine.register(self.eventType,self.signal.emit)

    def initInput(self):
        """设置输入框"""
        self.mf_ComboBox_list = list()
        # 下拉框，用来选择不同的协存项目
        mf_ComboBox_Label = QLabel("基金项目")
        self.mf_ComboBox = QComboBox()

        # 设置组件
        mf_subscribe_from_cash_Label = QLabel("申购(现金)")
        mf_redeem_to_cash_Label = QLabel("赎回(现金)")
        mf_not_carry_forward_revenue_Label = QLabel("未结转收益")
        mf_carry_forward_revenue_Label = QLabel("结转金额")

        date_Label = QLabel("时间")

        self.mf_subscribe_from_cash_Edit = QLineEdit("0.00")
        self.mf_redeem_to_cash_Edit = QLineEdit("0.00")
        self.mf_not_carry_forward_revenue_Edit = QLineEdit("0.00")
        self.mf_carry_forward_revenue_Edit = QLineEdit("0.00")

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
        grid.addWidget(mf_ComboBox_Label, 0, 0)
        grid.addWidget(mf_subscribe_from_cash_Label, 1, 0)
        grid.addWidget(mf_redeem_to_cash_Label, 2, 0)
        grid.addWidget(mf_not_carry_forward_revenue_Label, 3, 0)
        grid.addWidget(mf_carry_forward_revenue_Label, 4, 0)
        grid.addWidget(date_Label, 5, 0)

        grid.addWidget(self.mf_ComboBox, 0, 1)
        grid.addWidget(self.mf_subscribe_from_cash_Edit, 1, 1)
        grid.addWidget(self.mf_redeem_to_cash_Edit, 2, 1)
        grid.addWidget(self.mf_not_carry_forward_revenue_Edit, 3, 1)
        grid.addWidget(self.mf_carry_forward_revenue_Edit, 4, 1)
        grid.addWidget(self.date_Edit, 5, 1)

        grid.addLayout(buttonHBox, 6, 0, 1, 2)

        self.setLayout(grid)

    def addData(self):
        """增加数据"""
        mf_project_name_index = str(self.mf_ComboBox.currentIndex())

        mf_subscribe_from_cash = str(self.mf_subscribe_from_cash_Edit.text())
        mf_redeem_to_cash = str(self.mf_redeem_to_cash_Edit.text())
        mf_not_carry_forward_revenue = str(self.mf_not_carry_forward_revenue_Edit.text())
        mf_carry_forward_revenue = str(self.mf_carry_forward_revenue_Edit.text())

        mf_uuid = self.mf_ComboBox_list[int(mf_project_name_index)]
        """向数据库增加数据"""

        date_str = str(self.date_Edit.text()).split('-')
        d = datetime.date.today()
        if date_str is None:
            date = datetime.date(d.year, d.month, d.day)
        else:
            date = datetime.date(int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[0])),
                                 int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[1])),
                                 int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[2])))
        try:
            self.mainEngine.add_fund_daily_data(date, mf_uuid, float(mf_carry_forward_revenue), float(mf_subscribe_from_cash),
                                                float(mf_redeem_to_cash),
                                                float(mf_not_carry_forward_revenue))
        except ValueError:
            self.showError()
            return

        # 加入数据后，更新列表显示
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MF))
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_FEE))
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_VALUATION))
        # self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_ASSERT_DETAIL))

        self.showInfo()


    def prepareData(self):

        result = self.mainEngine.get_all_asset_ids_by_type(SV.ASSET_CLASS_FUND)
        for mf in result:
            # print(mf)
            self.mf_ComboBox_list.append(mf[0])
            self.mf_ComboBox.addItem(mf[1])
        print('prepare data called ....')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = MoneyFundInput(mainEngine, mainEngine.eventEngine)
    cashInput.show()
    sys.exit(app.exec_())
