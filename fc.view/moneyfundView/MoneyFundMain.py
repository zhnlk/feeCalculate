# -*- coding: utf-8 -*-
from collections import OrderedDict

from PyQt5.QtWidgets import QAction, QApplication

from BasicWidget import BASIC_FONT, BasicFcView, BasicCell, NumCell
from EventType import EVENT_MF
from MainEngine import MainEngine


class MoneyFundListView(BasicFcView):
    """现金详情"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(MoneyFundListView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()

        d['mf_project_name'] = {'chinese': '货基项目名称', 'cellType': BasicCell}
        d['date'] = {'chinese': '计算日', 'cellType': BasicCell}
        # d['money_fund_amount'] = {'chinese': '货基总额', 'cellType': NumCell}
        # d['money_fund_revenue'] = {'chinese': '货基收益', 'cellType': NumCell}
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
        d['mf_not_carry_forward_amount'] = {'chinese': '未结转收益', 'cellType': BasicCell}
        d['mf_carry_forward_amount'] = {'chinese': '结转金额', 'cellType': BasicCell}

        self.setHeaderDict(d)

        self.setEventType(EVENT_MF)

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
        # result0 = self.mainEngine.getProtocol()
        result1 = self.mainEngine.getProtocolDetail()
        result2 = self.mainEngine.getMoneyFundDetail()
        print(len(result1) + len(result2))
        # self.setRowCount(len(result1)+len(result2))
        self.setRowCount(len(result2))
        row = 0
        for r in result2:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.headerList):
                if header is 'mf_project_name':
                    content = r.getMfProjectName()
                else:
                    content = r.__getattribute__(header)
                cellType = self.headerDict[header]['cellType']
                cell = cellType(content)
                print(cell.text())
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
        self.showMoneyFundListDetail()

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


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    mflv = MoneyFundListView(mainEngine)

    mflv.show()
    sys.exit(app.exec_())
