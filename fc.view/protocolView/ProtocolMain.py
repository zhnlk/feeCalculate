# -*- coding: utf-8 -*-
from collections import OrderedDict

from PyQt5.QtWidgets import QAction

from BasicWidget import BASIC_FONT, BasicFcView, BasicCell


class ProtocolListView(BasicFcView):
    """现金详情"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(ProtocolListView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()
        d['date'] = {'chinese': '计算日', 'cellType': BasicCell}
        d['protocol_deposit_amount'] = {'chinese': '协存总额', 'cellType': BasicCell}
        d['protocol_deposit_revenue'] = {'chinese': '协存收益', 'cellType': BasicCell}
        d['cash_to_protocol_deposit'] = {'chinese': '现金->协存', 'cellType': BasicCell}
        d['protocol_deposit_to_cash'] = {'chinese': '协存->现金', 'cellType': BasicCell}
        # 协存项目
        d['cash_to_investor'] = {'chinese': '总额', 'cellType': BasicCell}
        d['assert_mgt_to_cash'] = {'chinese': '协存本金', 'cellType': BasicCell}
        d['money_fund_to_cash'] = {'chinese': '协存利息', 'cellType': BasicCell}
        # 协存项目 输入项
        d['protocol_deposit_to_cash'] = {'chinese': '利息转结本金', 'cellType': BasicCell}
        d['investor_to_cash'] = {'chinese': '投资人资金->协存', 'cellType': BasicCell}
        d['investor_to_cash'] = {'chinese': '现金->协存', 'cellType': BasicCell}
        d['investor_to_cash'] = {'chinese': '协存->总付投资人', 'cellType': BasicCell}
        d['investor_to_cash'] = {'chinese': '协存->现金', 'cellType': BasicCell}

        self.setHeaderDict(d)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('协存明细')
        self.setMinimumSize(800, 800)
        self.setFont(BASIC_FONT)
        self.initTable()
        self.addMenuAction()

    # ----------------------------------------------------------------------
    def showProtocolListDetail(self):
        """显示所有合约数据"""
        l = self.mainEngine.getAllContracts()
        d = {'.'.join([contract.exchange, contract.symbol]): contract for contract in l}
        l2 = d.keys()
        l2.sort(reverse=True)

        self.setRowCount(len(l2))
        row = 0

        for key in l2:
            contract = d[key]

            for n, header in enumerate(self.headerList):
                content = contract.__getattribute__(header)
                cellType = self.headerDict[header]['cellType']
                cell = cellType(content)

                if self.font:
                    cell.setFont(self.font)  # 如果设置了特殊字体，则进行单元格设置

                self.setItem(row, n, cell)

            row = row + 1

    # ----------------------------------------------------------------------
    def refresh(self):
        """刷新"""
        self.menu.close()  # 关闭菜单
        self.clearContents()
        self.setRowCount(0)
        # self.showProtocolListDetail()

    # ----------------------------------------------------------------------
    def addMenuAction(self):
        """增加右键菜单内容"""
        refreshAction = QAction('刷新', self)
        refreshAction.triggered.connect(self.refresh)

        self.menu.addAction(refreshAction)

    # ----------------------------------------------------------------------
    def show(self):
        """显示"""
        super(ProtocolListView, self).show()
        self.refresh()



# class OutCashData(QTableWidget):
#
#     def __init__(self, parent=None):
#         super(OutCashData, self).__init__(parent=parent)
#
#         self.initUI()
#
#     def initUI(self):
#         """导出数据"""
#         self.setWindowTitle('导出数据')
#         self.setMinimumSize(800, 800)
#         self.setFont(BASIC_FONT)
#         # self.initTable()
#         self.saveFileDialog()
#         self.addMenuAction()
#
#     def saveFileDialog(self):
#         class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
#             def __init__(self):
#                 super(MyWindow, self).__init__()
#                 self.setupUi(self)
#                 self.fileOpen.triggered.connect(self.openMsg)  # 菜单的点击事件是triggered
#
#             def openMsg(self):
#                 file, ok = QFileDialog.getOpenFileName(self, "打开", "C:/", "All Files (*);;Text Files (*.txt)")
#                 self.statusbar.showMessage(file)  # 在状态栏显示文件地址
#
#
# class AddCashDetail(QTableWidget):
#     # ----------------------------------------------------------------------
#     def __init__(self, parent=None):
#         """Constructor"""
#         super(AddCashDetail, self).__init__(parent=parent)
#
#         self.initUI()
#
#         # self.child = ChildrenForm()  # self.child = children()生成子窗口实例self.child
#         #
#         # self.fileOpen.triggered.connect(self.openMsg)  # 菜单的点击事件是triggered
#         # self.fileClose.triggered.connect(self.close)
#         # self.actionTst.triggered.connect(self.childShow)  # 点击actionTst,子窗口就会显示在主窗口的MaingridLayout中
#
#         # self.mainEngine = mainEngine
#     def childShow(self):
#         self.MaingridLayout.addWidget(self.child)  # 添加子窗口
#         self.child.show()
#
#     def openMsg(self):
#         file, ok = QFileDialog.getOpenFileName(self, "打开", "C:/", "All Files (*);;Text Files (*.txt)")
#         self.statusbar.showMessage(file)  # 在状态栏显示文件地址



        # d = OrderedDict()
        # d['symbol'] = {'chinese': '合约代码', 'cellType': BasicCell}
        # d['exchange'] = {'chinese': '交易所', 'cellType': BasicCell}
        # d['vtSymbol'] = {'chinese': 'vt系统代码', 'cellType': BasicCell}
        # d['name'] = {'chinese': '名称', 'cellType': BasicCell}
        # d['productClass'] = {'chinese': '合约类型', 'cellType': BasicCell}
        # d['size'] = {'chinese': '大小', 'cellType': BasicCell}
        # d['priceTick'] = {'chinese': '最小价格变动', 'cellType': BasicCell}
        # d['strikePrice'] = {'chinese':'期权行权价', 'cellType':BasicCell}
        # d['underlyingSymbol'] = {'chinese':'期权标的物', 'cellType':BasicCell}
        # d['optionType'] = {'chinese':'期权类型', 'cellType':BasicCell}
        # self.setHeaderDict(d)

        # self.initUI()
    #
    # # ----------------------------------------------------------------------
    # def initUI(self):
    #     """初始化界面"""
    #     self.setWindowTitle('增加现金明细')
    #     self.setMinimumSize(800, 800)
    #     self.setFont(BASIC_FONT)
    #     self.initTable()
    #     self.addMenuAction()
    #
    # # ----------------------------------------------------------------------
    # def showAllContracts(self):
    #     """显示所有合约数据"""
    #     # l = self.mainEngine.getAllContracts()
    #     # d = {'.'.join([contract.exchange, contract.symbol]): contract for contract in l}
    #     # l2 = d.keys()
    #     # l2.sort(reverse=True)
    #     #
    #     # self.setRowCount(len(l2))
    #     # row = 0
    #     #
    #     # for key in l2:
    #     #     contract = d[key]
    #     #
    #     #     for n, header in enumerate(self.headerList):
    #     #         content = safeUnicode(contract.__getattribute__(header))
    #     #         cellType = self.headerDict[header]['cellType']
    #     #         cell = cellType(content)
    #     #
    #     #         if self.font:
    #     #             cell.setFont(self.font)  # 如果设置了特殊字体，则进行单元格设置
    #     #
    #     #         self.setItem(row, n, cell)
    #     #
    #     #     row = row + 1
    #
    # # ----------------------------------------------------------------------
    # def initTable(self):
    #
    #     print('......initTable')
    #     pass
    #
    #
    # def refresh(self):
    #     """刷新"""
    #     # self.menu.close()  # 关闭菜单
    #     self.clearContents()
    #     self.setRowCount(0)
    #     # self.showAllContracts()
    #
    # # ----------------------------------------------------------------------
    # def addMenuAction(self):
    #     """增加右键菜单内容"""
    #     refreshAction = QAction('刷新', self)
    #     refreshAction.triggered.connect(self.refresh)
    #
    #     # self.menu.addAction(refreshAction)
    #
    # # ----------------------------------------------------------------------
    # def show(self):
    #     """显示"""
    #     super(AddCashDetail, self).show()
    #     self.refresh()
