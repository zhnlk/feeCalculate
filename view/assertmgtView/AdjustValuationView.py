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
        d['cal_date'] = {'chinese': '调整日期', 'cellType': BasicCell}
        d['fee_type'] = {'chinese': '转账类型', 'cellType': BasicCell}
        d['fee_amount'] = {'chinese': '总调整费用', 'cellType': NumCell}
        # d['pd_pd_to_cash'] = {'chinese': '调整结果', 'cellType': NumCell}

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
        # self.addMenuAction()

        self.signal.connect(self.refresh)
        self.mainEngine.eventEngine.register(self.eventType, self.signal.emit)

    def showAdjustListDetail(self):
        """显示所有合约数据"""
        result = self.mainEngine.get_management_adjust_fee_by_id(uuid=self.uuid)
        print(self.uuid, result)
        self.setRowCount(len(result))
        row = 0

        for r in result:
            # 按照定义的表头，进行数据填充
            for n, header in enumerate(self.headerList):
                if header is 'fee_type':
                    if r[header] is 2:
                        content = '转账费用'
                    elif r[header] is 3:
                        content = '支票费用'
                else:
                    content = r[header]

                cellType = self.headerDict[header]['cellType']
                cell = cellType(content)
                self.setItem(row, n, cell)

            row = row + 1

    def refresh(self):
        """刷新"""
        # self.menu.close()  # 关闭菜单
        self.clearContents()
        self.setRowCount(0)
        self.showAdjustListDetail()

    def addMenuAction(self):
        """增加右键菜单内容"""
        refreshAction = QAction('刷新', self)
        refreshAction.triggered.connect(self.refresh)

        # self.menu.addAction(refreshAction)

    def show(self):
        """显示"""
        super(AdjustValuationView, self).show()
        self.refresh()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainEngine = MainEngine()
    plv = AdjustValuationView(mainEngine,uuid='21c5407b0578465ba61d87388d1b5537')

    plv.show()
    sys.exit(app.exec_())
