# -*- coding: utf-8 -*-
from collections import OrderedDict

from PyQt5.QtWidgets import QAction

from BasicWidget import BASIC_FONT, BasicFcView, BasicCell


class MoneyFundListView(BasicFcView):
    """现金详情"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(MoneyFundListView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()
        d['date'] = {'chinese': '计算日', 'cellType': BasicCell}
        d['money_fund_amount'] = {'chinese': '货基总额', 'cellType': BasicCell}
        d['money_fund_revenue'] = {'chinese': '货基收益', 'cellType': BasicCell}
        # 货基项目
        d['mf_amount'] = {'chinese': '金额', 'cellType': BasicCell}
        d['mf_revenue'] = {'chinese': '收益', 'cellType': BasicCell}
        d['mf_subscribe_amount'] = {'chinese': '申购总额', 'cellType': BasicCell}
        d['mf_redeem_amount'] = {'chinese': '赎回总额', 'cellType': BasicCell}
        # 货基项目 输入项
        d['mf_subscribe_normal'] = {'chinese': '正常申购', 'cellType': BasicCell}
        d['mf_subscribe_from_assert_mgt'] = {'chinese': '申购(资管)', 'cellType': BasicCell}
        d['mf_subscribe_from_cash'] = {'chinese': '申购(现金)', 'cellType': BasicCell}
        d['mf_redeem_normal'] = {'chinese': '正常赎回', 'cellType': BasicCell}
        d['mf_redeem_to_assert_mgt'] = {'chinese': '赎回(进资管)', 'cellType': BasicCell}
        d['mf_redeem_to_cash'] = {'chinese': '赎回(进现金)', 'cellType': BasicCell}
        d['mf_redeem_fee'] = {'chinese': '赎回(费用)', 'cellType': BasicCell}
        d['mf_not_carry_forward_revenue'] = {'chinese': '未结转收益', 'cellType': BasicCell}
        d['mf_carry_forward_revenue'] = {'chinese': '结转金额', 'cellType': BasicCell}

        self.setHeaderDict(d)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('货基明细')
        self.setMinimumSize(800, 800)
        self.setFont(BASIC_FONT)
        self.initTable()
        self.addMenuAction()

    # ----------------------------------------------------------------------
    def showMoneyFundListDetail(self):
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
        # self.showMoneyFundListDetail()

    # ----------------------------------------------------------------------
    def addMenuAction(self):
        """增加右键菜单内容"""
        refreshAction = QAction('刷新', self)
        refreshAction.triggered.connect(self.refresh)

        self.menu.addAction(refreshAction)

    # ----------------------------------------------------------------------
    def show(self):
        """显示"""
        super(MoneyFundListView, self).show()
        self.refresh()
