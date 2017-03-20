# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


# 创建数据库连接
def createConnection():
    # 选择数据库类型，这里为sqlite3数据库
    db = QSqlDatabase.addDatabase('QSQLITE')
    # 创建数据库test0.db,如果存在则打开，否则创建该数据库
    db.setDatabaseName("data-test.db")
    # 打开数据库
    db.open()

class Model(QSqlTableModel):
    def __init__(self, parent):
        QSqlTableModel.__init__(self, parent)
        # 设置要载入的表名
        self.setTable("User")
        # self.setHeaderData(0,Qt.PrimaryOrientation,'111')
        # 这一步应该是执行查询的操作，不太理解
        self.select()
        # 数据更新的策略，详细可以查看Qt文档
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)


class teastDBWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        vbox = QVBoxLayout(self)
        self.view = QTableView()
        self.model = Model(self.view)
        self.view.setModel(self.model)
        # 将表格宽度与窗口大小相适应
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        vbox.addWidget(self.view)


if __name__ == "__main__":
    a = QApplication(sys.argv)
    createConnection()
    # createTable()
    w = teastDBWidget()
    w.show()
    sys.exit(a.exec_())
