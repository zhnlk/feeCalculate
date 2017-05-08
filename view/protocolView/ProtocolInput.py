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

from controller.EventEngine import Event
from controller.EventType import EVENT_MAIN_FEE, EVENT_MAIN_VALUATION, EVENT_PD, EVENT_PD_INPUT
from view.BasicWidget import BASIC_FONT, BasicFcView
from controller.MainEngine import MainEngine
from utils import StaticValue as SV


class ProtocolInput(BasicFcView):
    """协存输入"""

    def __init__(self, mainEngine, eventEngine=None, parent=None):
        """Constructor"""
        super(ProtocolInput, self).__init__(parent=parent)

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        self.setEventType(EVENT_PD_INPUT)

        self.initUi()

    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('输入协存明细')
        # self.setMinimumSize(800, 800)
        self.setFont(BASIC_FONT)
        # self.initTable()
        self.initInput()
        self.prepareData()
        # self.addMenuAction()

        # self.signal.connect(self.prepareData)
        # self.mainEngine.eventEngine.register(self.eventType, self.signal.emit)

    def initInput(self):
        """设置输入框"""
        self.pd_ComboBox_list = list()
        # 下拉框，用来选择不同的协存项目
        pd_ComboBox_Label = QLabel("协存项目")
        self.pd_ComboBox = QComboBox()

        # 设置组件
        interest_to_principal_Label = QLabel("利息结转本金")
        # investor_to_pd_Label = QLabel("投资人资金->协存")
        cash_to_pd_Label = QLabel("现金->协存")
        # pd_to_investor_Label = QLabel("协存->兑付投资人")
        pd_to_cash_Label = QLabel("协存->现金")

        date_Label = QLabel("日期")

        self.interest_to_principal_Edit = QLineEdit("0.00")
        # self.investor_to_pd_Edit = QLineEdit("0.00")
        self.cash_to_pd_Edit = QLineEdit("0.00")
        # self.pd_to_investor_Edit = QLineEdit("0.00")
        self.pd_to_cash_Edit = QLineEdit("0.00")
        self.date_Edit = QLineEdit("2017-01-01")

        okButton = QPushButton("确定")
        cancelButton = QPushButton("取消")
        okButton.clicked.connect(self.insertDB)
        cancelButton.clicked.connect(self.close)

        # 设置布局
        buttonHBox = QHBoxLayout()
        buttonHBox.addStretch()
        buttonHBox.addWidget(okButton)
        buttonHBox.addWidget(cancelButton)

        grid = QGridLayout()
        grid.addWidget(pd_ComboBox_Label, 0, 0)
        grid.addWidget(interest_to_principal_Label, 1, 0)
        # grid.addWidget(investor_to_pd_Label, 2, 0)
        grid.addWidget(cash_to_pd_Label, 3, 0)
        # grid.addWidget(pd_to_investor_Label, 4, 0)
        grid.addWidget(pd_to_cash_Label, 5, 0)
        grid.addWidget(date_Label, 6, 0)

        grid.addWidget(self.pd_ComboBox, 0, 1)
        grid.addWidget(self.interest_to_principal_Edit, 1, 1)
        # grid.addWidget(self.investor_to_pd_Edit, 2, 1)
        grid.addWidget(self.cash_to_pd_Edit, 3, 1)
        # grid.addWidget(self.pd_to_investor_Edit, 4, 1)
        grid.addWidget(self.pd_to_cash_Edit, 5, 1)
        grid.addWidget(self.date_Edit, 6, 1)
        grid.addLayout(buttonHBox, 7, 0, 1, 2)

        self.setLayout(grid)

    def insertDB(self):
        """增加数据"""
        pd_project_name_index = str(self.pd_ComboBox.currentIndex())
        interest_to_principal = str(self.interest_to_principal_Edit.text())
        # investor_to_pd = str(self.investor_to_pd_Edit.text())
        cash_to_pd = str(self.cash_to_pd_Edit.text())
        # pd_to_investor = str(self.pd_to_investor_Edit.text())
        pd_to_cash = str(self.pd_to_cash_Edit.text())
        """向数据库增加数据"""
        print(interest_to_principal)
        print(cash_to_pd)
        print(pd_to_cash)

        pd_uuid = self.pd_ComboBox_list[int(pd_project_name_index)]
        # print(pd_uuid + '..............')

        # pdProject = PdProject.findByUUID(pd_uuid)

        date_str = str(self.date_Edit.text()).split('-')
        d = datetime.date.today()
        if date_str is None:
            date = datetime.date(d.year, d.month, d.day)
        else:
            date = datetime.date(int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[0])),
                                 int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[1])),
                                 int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", date_str[2])))
        try:
            self.mainEngine.add_agreement_daily_data(date, pd_uuid, float(interest_to_principal), float(cash_to_pd), float(pd_to_cash))

        except ValueError:
            self.showError()
            return

        # 加入数据后，更新列表显示
        self.mainEngine.eventEngine.put(Event(type_=EVENT_PD))
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_FEE))
        self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_VALUATION))
        # self.mainEngine.eventEngine.put(Event(type_=EVENT_MAIN_ASSERT_DETAIL))

        self.showInfo()


    def prepareData(self):

        result = self.mainEngine.get_all_asset_ids_by_type(SV.ASSET_CLASS_AGREEMENT)
        # print('prepareData running.....')
        for mf in result:
            # print(mf)
            self.pd_ComboBox_list.append(mf[0])
            self.pd_ComboBox.addItem(mf[1])
        print('pd prepare called ....')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = ProtocolInput(mainEngine, mainEngine.eventEngine)
    cashInput.show()
    sys.exit(app.exec_())
