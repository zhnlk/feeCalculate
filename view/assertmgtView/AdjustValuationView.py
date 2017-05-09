# -*- coding: utf-8 -*-
# @Author:zhnlk
# @Date:  2017/4/25
# @Email: dG9tbGVhZGVyMDgyOEBnbWFpbC5jb20=  
# @Github:github/zhnlk
from collections import OrderedDict

from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication

from view.BasicWidget import BASIC_FONT, BasicFcView, BasicCell, NumCell
from controller.EventType import EVENT_PD, EVENT_ADJUST_VIEW
from controller.MainEngine import MainEngine


class AdjustValuationView(BasicFcView):
    """协存详情"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, uuid, parent=None):
        """Constructor"""
        super(AdjustValuationView, self).__init__(parent=parent)

        self.mainEngine = mainEngine
        self.uuid = uuid

        d = OrderedDict()
        d['pd_project_name'] = {'chinese': '调整日期', 'cellType': BasicCell}
        d['pd_project_rate'] = {'chinese': '转账费用', 'cellType': NumCell}

        d['date'] = {'chinese': '支票费用', 'cellType': NumCell}
        d['total_to_cash'] = {'chinese': '总调整费用', 'cellType': NumCell}
        d['pd_pd_to_cash'] = {'chinese': '调整结果', 'cellType': NumCell}

        self.setHeaderDict(d)

        self.setEventType(EVENT_ADJUST_VIEW)

        self.initUi()

    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('估值调整明细')
        self.setMinimumSize(600, 200)
        self.setFont(BASIC_FONT)
        self.initTable()
        self.verticalHeader().setVisible(True)
        self.addMenuAction()

        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(self.eventType, self.signal.emit)

    def showAdjustListDetail(self):
        """显示所有合约数据"""
        result2 = self.mainEngine.get_management_fee_by_id(uuid=self.uuid)
        print(self.uuid, result2)
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
                # print(cell.text())
                # if self.font:
                #     cell.setFont(self.font)  # 如果设置了特殊字体，则进行单元格设置

                self.setItem(row, n, cell)

            row = row + 1

    def refresh(self):
        """刷新"""
        self.menu.close()  # 关闭菜单
        self.clearContents()
        self.setRowCount(0)
        self.showAdjustListDetail()

    def addMenuAction(self):
        """增加右键菜单内容"""
        refreshAction = QAction('刷新', self)
        refreshAction.triggered.connect(self.refresh)

        self.menu.addAction(refreshAction)

    def show(self):
        """显示"""
        super(AdjustValuationView, self).show()
        self.refresh()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    plv = AdjustValuationView(mainEngine,uuid='9cb0b9dd10414b548352f01439f076b5')

    plv.show()
    sys.exit(app.exec_())
