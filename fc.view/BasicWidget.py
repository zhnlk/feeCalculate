# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QVBoxLayout

from pandas import json


def loadFont():
    """载入字体设置"""
    fileName = 'VT_setting.json'
    path = os.path.abspath(os.path.dirname(__file__))
    fileName = os.path.join(path, fileName)

    try:
        f = open(fileName)
        setting = json.load(f)
        family = setting['fontFamily']
        size = setting['fontSize']
        font = QtGui.QFont(family, size)
    except:
        font = QtGui.QFont(u'微软雅黑', 12)
    return font


BASIC_FONT = loadFont()



class AboutWidget(QDialog):
    """显示关于信息"""

    # ----------------------------------------------------------------------
    def __init__(self, parent=None):
        """Constructor"""
        super(AboutWidget, self).__init__(parent)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """"""
        self.setWindowTitle('About Fee Calculate')

        text = """
                Developed by zhnlk.

                License：MIT

                Mail：yanan.zhang@creditcloud.com

                Github：www.github.com/zhnlk

                """

        label = QLabel()
        label.setText(text)
        label.setMinimumWidth(500)

        vbox = QVBoxLayout()
        vbox.addWidget(label)

        self.setLayout(vbox)





class OutCashData(QTableWidget):

    def __init__(self, parent=None):

        super(OutCashData,self).__init__(parent=parent)

        self.initUI()
    def initUI(self):
        """导出数据"""
        self.setWindowTitle('导出数据')
        self.setMinimumSize(800, 800)
        self.setFont(BASIC_FONT)
        # self.initTable()
        # self.addMenuAction()


class AddCashDetail(QTableWidget):
    # ----------------------------------------------------------------------
    def __init__(self,parent=None):
        """Constructor"""
        super(AddCashDetail, self).__init__(parent=parent)

        # self.mainEngine = mainEngine

        # d = OrderedDict()
        # d['symbol'] = {'chinese': u'合约代码', 'cellType': BasicCell}
        # d['exchange'] = {'chinese': u'交易所', 'cellType': BasicCell}
        # d['vtSymbol'] = {'chinese': u'vt系统代码', 'cellType': BasicCell}
        # d['name'] = {'chinese': u'名称', 'cellType': BasicCell}
        # d['productClass'] = {'chinese': u'合约类型', 'cellType': BasicCell}
        # d['size'] = {'chinese': u'大小', 'cellType': BasicCell}
        # d['priceTick'] = {'chinese': u'最小价格变动', 'cellType': BasicCell}
        # d['strikePrice'] = {'chinese':u'期权行权价', 'cellType':BasicCell}
        # d['underlyingSymbol'] = {'chinese':u'期权标的物', 'cellType':BasicCell}
        # d['optionType'] = {'chinese':u'期权类型', 'cellType':BasicCell}
        # self.setHeaderDict(d)

        self.initUI()

    # ----------------------------------------------------------------------
    def initUI(self):
        """初始化界面"""
        self.setWindowTitle('增加现金明细')
        self.setMinimumSize(800, 800)
        self.setFont(BASIC_FONT)
        # self.initTable()
        self.addMenuAction()

    # ----------------------------------------------------------------------
    def showAllContracts(self):
        """显示所有合约数据"""
        # l = self.mainEngine.getAllContracts()
        # d = {'.'.join([contract.exchange, contract.symbol]): contract for contract in l}
        # l2 = d.keys()
        # l2.sort(reverse=True)
        #
        # self.setRowCount(len(l2))
        # row = 0
        #
        # for key in l2:
        #     contract = d[key]
        #
        #     for n, header in enumerate(self.headerList):
        #         content = safeUnicode(contract.__getattribute__(header))
        #         cellType = self.headerDict[header]['cellType']
        #         cell = cellType(content)
        #
        #         if self.font:
        #             cell.setFont(self.font)  # 如果设置了特殊字体，则进行单元格设置
        #
        #         self.setItem(row, n, cell)
        #
        #     row = row + 1

    # ----------------------------------------------------------------------
    def refresh(self):
        """刷新"""
        # self.menu.close()  # 关闭菜单
        self.clearContents()
        self.setRowCount(0)
        # self.showAllContracts()

    # ----------------------------------------------------------------------
    def addMenuAction(self):
        """增加右键菜单内容"""
        refreshAction = QAction(u'刷新', self)
        refreshAction.triggered.connect(self.refresh)

        # self.menu.addAction(refreshAction)

    # ----------------------------------------------------------------------
    def show(self):
        """显示"""
        super(AddCashDetail, self).show()
        self.refresh()