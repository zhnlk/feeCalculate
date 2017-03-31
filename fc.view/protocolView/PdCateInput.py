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
from MainEngine import MainEngine
from ProtocolDeposit import ProtocolDeposit, PdProject


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
        pd_project_name_Label = QLabel("协存项目名称")
        pd_project_rate_Label = QLabel("协存项目利率(0.03)")

        self.pd_project_name_Edit = QLineEdit('盛京银行协存')
        self.pd_project_rate_Edit = QLineEdit("0.03")
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
        grid.addWidget(pd_project_name_Label, 0, 0)
        grid.addWidget(pd_project_rate_Label, 1, 0)
        grid.addWidget(self.pd_project_name_Edit, 0, 1)
        grid.addWidget(self.pd_project_rate_Edit, 1, 1)
        grid.addLayout(buttonHBox, 2, 0, 1, 2)

        self.setLayout(grid)

    # ----------------------------------------------------------------------
    def insertDB(self):
        """增加数据"""
        pd_project_name = str(self.pd_project_name_Edit.text())
        pd_project_rate = str(self.pd_project_rate_Edit.text())
        """向数据库增加数据"""
        pdProject = PdProject(pd_project_name, pd_project_rate)
        pdProject.save()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = PdCateInput(mainEngine, mainEngine.eventEngine)
    cashInput.show()
    sys.exit(app.exec_())
