# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QFileDialog


class MainForm(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)

        self.child = ChildrenForm()  # self.child = children()生成子窗口实例self.child

        self.fileOpen.triggered.connect(self.openMsg)  # 菜单的点击事件是triggered
        self.fileClose.triggered.connect(self.close)
        self.actionTst.triggered.connect(self.childShow)  # 点击actionTst,子窗口就会显示在主窗口的MaingridLayout中

    def childShow(self):
        self.MaingridLayout.addWidget(self.child)  # 添加子窗口
        self.child.show()

    def openMsg(self):
        file, ok = QFileDialog.getOpenFileName(self, "打开", "C:/", "All Files (*);;Text Files (*.txt)")
        self.statusbar.showMessage(file)  # 在状态栏显示文件地址


class ChildrenForm(QtWidgets.QWidget):
    def __init__(self):
        super(ChildrenForm, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myshow = MainForm()
    myshow.show()
    sys.exit(app.exec_())