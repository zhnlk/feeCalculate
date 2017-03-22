# -*- coding: utf-8 -*-
from collections import OrderedDict

from PyQt5.QtWidgets import QAction

from BasicWidget import BASIC_FONT, BasicFcView, BasicCell


class CashListView(BasicFcView):
    """现金详情"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(CashListView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()
        d['date'] = {'chinese': '计算日', 'cellType': BasicCell}
        d['total_cash'] = {'chinese': '现金总额', 'cellType': BasicCell}
        d['cash_to_assert_mgt'] = {'chinese': '现金->资管', 'cellType': BasicCell}
        d['cash_to_money_fund'] = {'chinese': '现金->货基', 'cellType': BasicCell}
        d['cash_to_protocol_deposit'] = {'chinese': '现金->协存', 'cellType': BasicCell}
        d['cash_to_investor'] = {'chinese': '现金->兑付投资人', 'cellType': BasicCell}
        d['assert_mgt_to_cash'] = {'chinese': '资管->现金', 'cellType': BasicCell}
        d['money_fund_to_cash'] = {'chinese': '货基->现金', 'cellType': BasicCell}
        d['protocol_deposit_to_cash'] = {'chinese': '协存->现金', 'cellType': BasicCell}
        d['investor_to_cash'] = {'chinese': '投资人->现金', 'cellType': BasicCell}

        self.setHeaderDict(d)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('现金明细')
        self.setMinimumSize(800, 800)
        self.setFont(BASIC_FONT)
        self.initTable()
        self.addMenuAction()

    # ----------------------------------------------------------------------
    def showCashListDetail(self):
        """显示所有合约数据"""
        l = self.mainEngine.getAllContracts
        # l = self.mainEngine.getCashDetail
        d = {'.'.join([contract.exchange, contract.symbol]): contract for contract in l}
        l2 = d.keys()
        # l2.sort(reverse=True)

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
        # self.showCashListDetail()

    # ----------------------------------------------------------------------
    def addMenuAction(self):
        """增加右键菜单内容"""
        refreshAction = QAction('刷新', self)
        refreshAction.triggered.connect(self.refresh)

        self.menu.addAction(refreshAction)

    # ----------------------------------------------------------------------
    def show(self):
        """显示"""
        super(CashListView, self).show()
        self.refresh()
