# -*- coding: utf-8 -*-
# @Author:zhnlk
# @Date:  2017/4/25
# @Email: dG9tbGVhZGVyMDgyOEBnbWFpbC5jb20=  
# @Github:github/zhnlk
from collections import OrderedDict

from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication

from BasicWidget import BASIC_FONT, BasicFcView, BasicCell, NumCell
from EventType import EVENT_PD
from MainEngine import MainEngine


class AdjustValuationView(BasicFcView):
    """协存详情"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(AdjustValuationView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()
        d['pd_project_name'] = {'chinese': '调整日期', 'cellType': BasicCell}
        d['pd_project_rate'] = {'chinese': '转账费用', 'cellType': BasicCell}

        d['date'] = {'chinese': '支票费用', 'cellType': BasicCell}
        d['total_to_cash'] = {'chinese': '总调整费用', 'cellType': BasicCell}
        d['pd_pd_to_cash'] = {'chinese': '调整结果', 'cellType': BasicCell}

        self.setHeaderDict(d)

        self.setEventType(EVENT_PD)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('协存明细')
        self.setMinimumSize(600, 200)
        self.setFont(BASIC_FONT)
        self.initTable()
        self.verticalHeader().setVisible(True)
        self.addMenuAction()

    # ----------------------------------------------------------------------
    def showProtocolListDetail(self):
        """显示所有合约数据"""
        # result0 = self.mainEngine.getProtocol()
        result2 = self.mainEngine.getProtocolListDetail()
        # self.setRowCount(len(result1)+len(result2))
        self.setRowCount(len(result2))
        row = 0
        for r in result2:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.headerList):
                name, rate = r.getPdProjectInfo()
                if header is 'pd_project_name':
                    content = name
                elif header is 'pd_project_rate':
                    content = rate
                else:
                    content = r.__getattribute__(header)

                if isinstance(content, float):
                    content = float('%.2f' % content)
                cellType = self.headerDict[header]['cellType']
                cell = cellType(content)
                print(cell.text())
                # if self.font:
                #     cell.setFont(self.font)  # 如果设置了特殊字体，则进行单元格设置

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
        super(AdjustValuationView, self).show()
        self.refresh()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    plv = AdjustValuationView(mainEngine)

    plv.show()
    sys.exit(app.exec_())

