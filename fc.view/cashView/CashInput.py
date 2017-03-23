# -*- coding: utf-8 -*-
from collections import OrderedDict

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

from BasicWidget import BASIC_FONT, BasicFcView, BasicCell
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
        label1 = QLabel("标签1")
        label2 = QLabel("标签2")
        label3 = QLabel("标签3")
        label4 = QLabel("标签4")
        label5 = QLabel("标签5")
        self.editArea1 = QLineEdit()
        self.editArea2 = QLineEdit()
        self.editArea3 = QLineEdit()
        self.editArea4 = QLineEdit()
        self.editArea5 = QLineEdit()
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
        grid.addWidget(label1, 0, 0)
        grid.addWidget(label2, 1, 0)
        grid.addWidget(label3, 2, 0)
        grid.addWidget(label4, 3, 0)
        grid.addWidget(label5, 4, 0)
        grid.addWidget(self.editArea1, 0, 1)
        grid.addWidget(self.editArea2, 1, 1)
        grid.addWidget(self.editArea3, 2, 1)
        grid.addWidget(self.editArea4, 3, 1)
        grid.addWidget(self.editArea5, 4, 1)
        grid.addLayout(buttonHBox, 5, 0, 1, 2)

        self.setLayout(grid)

    # ----------------------------------------------------------------------
    def addData(self):
        """登录"""
        editArea1 = str(self.editArea1.text())
        editArea2 = str(self.editArea2.text())
        editArea3 = str(self.editArea3.text())
        editArea4 = str(self.editArea4.text())
        editArea5 = str(self.editArea5.text())

        # self.mainEngine.addCashDetail(editArea1, editArea2, editArea3, editArea4, editArea5)
        self.insertDB(editArea1, editArea2, editArea3, editArea4, editArea5)
        self.close()
    def close(self):
        self.close()
    # ----------------------------------------------------------------------
    def insertDB(self, editArea1, editArea2, editArea3, editArea4, editArea5):
        """向数据库增加数据"""
        print(editArea1)
        print(editArea2)
        print(editArea3)
        print(editArea4)
        print(editArea5)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    cashInput = CashInput(mainEngine, mainEngine.eventEngine)
    cashInput.show()
    sys.exit(app.exec_())
