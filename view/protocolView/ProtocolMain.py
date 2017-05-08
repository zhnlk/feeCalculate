# -*- coding: utf-8 -*-
from collections import OrderedDict

from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication

from view.BasicWidget import BASIC_FONT, BasicFcView, BasicCell, NumCell
from controller.EventType import EVENT_PD
from controller.MainEngine import MainEngine


class ProtocolListView(BasicFcView):
    """协存详情"""

    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(ProtocolListView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()
        d['asset_name'] = {'chinese': '协存项目名称', 'cellType': BasicCell}
        d['rate'] = {'chinese': '协存项目利率', 'cellType': BasicCell}

        d['cal_date'] = {'chinese': '计算日', 'cellType': BasicCell}

        # 协存项目
        d['total_amount'] = {'chinese': '总额', 'cellType': NumCell}
        d['asset_ret'] = {'chinese': '协存本金', 'cellType': NumCell}
        # d['pd_interest'] = {'chinese': '协存利息', 'cellType': BasicCell}
        # 协存项目 输入项
        d['ret_carry_principal'] = {'chinese': '利息转结本金', 'cellType': NumCell}
        d['cash_to_agreement'] = {'chinese': '现金->协存', 'cellType': NumCell}
        d['agreement_to_cash'] = {'chinese': '协存->现金', 'cellType': NumCell}

        self.setHeaderDict(d)

        self.setEventType(EVENT_PD)

        self.initUi()

    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('协存明细')
        self.setMinimumSize(1200, 600)
        self.setFont(BASIC_FONT)
        self.initTable()
        self.addMenuAction()

        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(self.eventType, self.signal.emit)

    def showProtocolListDetail(self):
        """显示所有合约数据"""
        result = self.mainEngine.get_agreement_detail_by_days()
        # print(result)
        count = 0
        for d in result:
            for v in d.values():
                count = count + len(v)
        self.setRowCount(count)
        row = 0
        # 遍历资产类型
        for r in result:
            # 遍历对应资产的记录
            for col in r.values():
                for c in col:
                    # print(c)
                    # 按照定义的表头，进行数据填充
                    for n, header in enumerate(self.headerList):
                        content = c[header]
                        cell = self.headerDict[header]['cellType'](content)
                        # print(row,n,content)
                        self.setItem(row, n, cell)

                    row = row + 1

    def refresh(self):
        """刷新"""
        self.menu.close()  # 关闭菜单
        self.clearContents()
        self.setRowCount(0)
        self.showProtocolListDetail()
        print('pd refresh called ....')

    def addMenuAction(self):
        """增加右键菜单内容"""
        refreshAction = QAction('刷新', self)
        refreshAction.triggered.connect(self.refresh)

        self.menu.addAction(refreshAction)

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
