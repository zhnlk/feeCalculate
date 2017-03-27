# -*- coding: utf-8 -*-
from collections import OrderedDict

from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication

from BasicWidget import BASIC_FONT, BasicFcView, BasicCell, NumCell
from MainEngine import MainEngine


class ProtocolListView(BasicFcView):
    """协存详情"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(ProtocolListView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()
        d['date'] = {'chinese': '计算日', 'cellType': BasicCell}
        # d['protocol_deposit_amount'] = {'chinese': '协存总额', 'cellType': NumCell}
        # d['protocol_deposit_revenue'] = {'chinese': '协存收益', 'cellType': NumCell}
        # d['cash_to_protocol_deposit'] = {'chinese': '现金->协存', 'cellType': NumCell}
        # d['protocol_deposit_to_cash'] = {'chinese': '协存->现金', 'cellType': NumCell}

        # 协存项目
        d['pd_amount'] = {'chinese': '总额', 'cellType': NumCell}
        d['pd_principal'] = {'chinese': '协存本金', 'cellType': NumCell}
        d['pd_interest'] = {'chinese': '协存利息', 'cellType': NumCell}
        # 协存项目 输入项
        d['pd_interest_to_principal'] = {'chinese': '利息转结本金', 'cellType': NumCell}
        d['pd_investor_to_pd'] = {'chinese': '投资人资金->协存', 'cellType': NumCell}
        d['pd_cash_to_pd'] = {'chinese': '现金->协存', 'cellType': NumCell}
        d['pd_pd_to_investor'] = {'chinese': '协存->总付投资人', 'cellType': NumCell}
        d['pd_pd_to_cash'] = {'chinese': '协存->现金', 'cellType': NumCell}

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
        # result0 = self.mainEngine.getProtocol()
        result1 = self.mainEngine.getProtocolDetail()
        result2 = self.mainEngine.getProtocolListDetail()
        print(len(result1)+len(result2))
        # self.setRowCount(len(result1)+len(result2))
        self.setRowCount(len(result2))
        row = 0
        for r in result2:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.headerList):

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
        self.showProtocolListDetail()

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

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    plv = ProtocolListView(mainEngine)

    plv.show()
    sys.exit(app.exec_())
