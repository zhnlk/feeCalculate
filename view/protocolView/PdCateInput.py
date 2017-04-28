# -*- coding: utf-8 -*-
import datetime

from PyQt5.QtWidgets import QApplication, QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

from BasicWidget import BASIC_FONT, BasicFcView
from MainEngine import MainEngine


class PdCateInput(BasicFcView):
    """协存输入"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, eventEngine=None, parent=None):
        """Constructor"""
        super(PdCateInput, self).__init__(parent=parent)

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        # self.setHeaderDict(d)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('输入协存项目')
        self.setMinimumSize(500, 200)
        self.setFont(BASIC_FONT)
        # self.initTable()
        self.initInput()
        # self.addMenuAction()

    # ----------------------------------------------------------------------
    def initInput(self):
        """设置输入框"""

        # 下拉框，用来选择不同的协存项目
        # 设置组件
        pd_project_name_Label = QLabel("协存项目名称")
        pd_project_rate_Label = QLabel("协存项目利率(0.03)")
        pd_stage_amount_Label = QLabel("若总额大于：")
        pd_stage_rate_Label = QLabel("利率为：")

        self.pd_project_name_Edit = QLineEdit('盛京银行协存')
        self.pd_project_rate_Edit = QLineEdit("0.03")
        self.pd_stage_amount_Edit = QLineEdit("0")
        self.pd_stage_rate_Edit = QLineEdit("0")

        self.pd_stage_Edit = QCheckBox("")

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

        grid.addWidget(self.pd_stage_Edit, 2, 0)
        grid.addWidget(pd_project_name_Label, 0, 1)
        grid.addWidget(pd_project_rate_Label, 1, 1)
        grid.addWidget(pd_stage_amount_Label, 2, 1)
        grid.addWidget(pd_stage_rate_Label, 2, 3)
        grid.addWidget(self.pd_project_name_Edit, 0, 2)
        grid.addWidget(self.pd_project_rate_Edit, 1, 2)
        grid.addWidget(self.pd_stage_amount_Edit, 2, 2)
        grid.addWidget(self.pd_stage_rate_Edit, 2, 4)
        grid.addLayout(buttonHBox, 4, 1, 1, 2)

        self.setLayout(grid)

    # ----------------------------------------------------------------------
    def insertDB(self):
        """增加数据"""
        pd_project_name = str(self.pd_project_name_Edit.text())
        pd_project_rate = str(self.pd_project_rate_Edit.text())
        stage_rate = self.pd_stage_Edit.isChecked()
        pd_stage_amount = str(self.pd_stage_amount_Edit.text())
        pd_stage_rate = str(self.pd_stage_rate_Edit.text())

        """向数据库增加数据"""
        if stage_rate:
            self.mainEngine.add_agreement_class(pd_project_name, pd_project_rate, pd_stage_amount, pd_stage_rate)
        else:
            self.mainEngine.add_agreement_class(name=pd_project_name, rate=pd_project_rate)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = PdCateInput(mainEngine, mainEngine.eventEngine)
    cashInput.show()
    sys.exit(app.exec_())
