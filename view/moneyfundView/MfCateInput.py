# -*- coding: utf-8 -*-
import datetime

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

from view.BasicWidget import BASIC_FONT, BasicFcView
from controller.MainEngine import MainEngine


class MfCateInput(BasicFcView):
    """协存输入"""

    def __init__(self, mainEngine, eventEngine=None, parent=None):
        """Constructor"""
        super(MfCateInput, self).__init__(parent=parent)

        self.mainEngine = mainEngine
        self.eventEngine = eventEngine

        self.initUi()

    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('输入货基项目')
        # self.setMinimumSize(800, 800)
        self.setFont(BASIC_FONT)
        self.initInput()

    def initInput(self):
        """设置输入框"""

        # 下拉框，用来选择不同的协存项目
        # 设置组件
        mf_project_name_Label = QLabel("协存项目名称")

        self.mf_project_name_Edit = QLineEdit('渤海基金')

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
        grid.addWidget(mf_project_name_Label, 0, 0)
        grid.addWidget(self.mf_project_name_Edit, 0, 1)
        grid.addLayout(buttonHBox, 2, 0, 1, 2)

        self.setLayout(grid)

    def addData(self):
        """增加数据"""

        mf_project_name = str(self.mf_project_name_Edit.text())
        """向数据库增加数据"""
        try:
            self.mainEngine.add_fund_class(mf_project_name)
        except ValueError:
            self.showError()
            return

        # 加入数据后，更新列表显示
        # self.mainEngine.eventEngine.put(Event(type_=EVENT_MF_INPUT))
        self.showInfo()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = MfCateInput(mainEngine, mainEngine.eventEngine)
    cashInput.show()
    sys.exit(app.exec_())
