# -*- coding: utf-8 -*-
from collections import OrderedDict

from PyQt5.QtWidgets import QAction

from BasicWidget import BASIC_FONT, BasicFcView, BasicCell
from EventType import EVENT_AM


class AssertMgtListView(BasicFcView):
    """现金详情"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(AssertMgtListView, self).__init__(parent=parent)

        self.mainEngine = mainEngine

        d = OrderedDict()
        d['retained_amount'] = {'chinese': '存量总额', 'cellType': BasicCell}
        d['retained_pricipal'] = {'chinese': '存量本金', 'cellType': BasicCell}
        d['today_revenue'] = {'chinese': '今日收益', 'cellType': BasicCell}
        d['total_input'] = {'chinese': '总流入', 'cellType': BasicCell}
        d['total_output'] = {'chinese': '总流出', 'cellType': BasicCell}
        d['normal_input'] = {'chinese': '正常流入', 'cellType': BasicCell}
        d['cash_input'] = {'chinese': '现金流入', 'cellType': BasicCell}
        d['expire_output'] = {'chinese': '砍头息/到期流出', 'cellType': BasicCell}
        # 资管项目 委贷要素
        d['short_borrower'] = {'chinese': '借款人简称', 'cellType': BasicCell}
        d['fund_source'] = {'chinese': '资金来源', 'cellType': BasicCell}
        d['loan_amount'] = {'chinese': '放款金额', 'cellType': BasicCell}
        d['delegate_rate'] = {'chinese': '委贷利率', 'cellType': BasicCell}
        d['bearing_days'] = {'chinese': '计息天数', 'cellType': BasicCell}
        d['value_date'] = {'chinese': '起息日', 'cellType': BasicCell}
        d['due_date'] = {'chinese': '到期日', 'cellType': BasicCell}
        d['duration'] = {'chinese': '期限', 'cellType': BasicCell}
        d['delegate_interest'] = {'chinese': '委贷利息', 'cellType': BasicCell}
        # 资管项目 委贷银行费用
        d['delegate_bank_rate'] = {'chinese': '委贷银行费率', 'cellType': BasicCell}
        d['delegate_bearing_days'] = {'chinese': '计息天数/次数', 'cellType': BasicCell}
        d['delegate_bank_fee'] = {'chinese': '委贷银行费用', 'cellType': BasicCell}
        # 资管项目 资管计划费用
        d['assert_mgt_channel_rate'] = {'chinese': '资管通道费率', 'cellType': BasicCell}
        d['assert_mgt_bearing_rate'] = {'chinese': '计息天数/次数', 'cellType': BasicCell}
        d['assert_mgt_fee'] = {'chinese': '资管费用', 'cellType': BasicCell}
        # 资管项目 资管计划收益
        d['assert_mgt_total_revenue'] = {'chinese': '资管计划总收益', 'cellType': BasicCell}
        d['assert_mgt_daily_revenue'] = {'chinese': '资管计划每日收益', 'cellType': BasicCell}
        # 资管计划 估值调整
        d['normal_assert_mgt_daily_revenue_valuation'] = {'chinese': '正常资管每日收益估值', 'cellType': BasicCell}
        # 资管计划 估值调整 调整项
        d['adjust_date'] = {'chinese': '调整日期', 'cellType': BasicCell}
        d['trans_fee'] = {'chinese': '转账费用', 'cellType': BasicCell}
        d['check_fee'] = {'chinese': '支票费用', 'cellType': BasicCell}
        d['total_adjust_fee'] = {'chinese': '总调整费用', 'cellType': BasicCell}
        d['adjust_result'] = {'chinese': '调整结果', 'cellType': BasicCell}
        # 资管计划 估值调整
        d['expire_out_to_fund'] = {'chinese': '砍头息转入货基部分', 'cellType': BasicCell}
        d['delegate_to_assert'] = {'chinese': '委贷户到资管托管户', 'cellType': BasicCell}


        self.setHeaderDict(d)

        self.setEventType(EVENT_AM)

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle('资管明细')
        self.setMinimumSize(800, 800)
        self.setFont(BASIC_FONT)
        self.initTable()
        self.addMenuAction()

    # ----------------------------------------------------------------------
    def showAssertMgtListDetail(self):
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
        # self.showAssertMgtListDetail()

    # ----------------------------------------------------------------------
    def addMenuAction(self):
        """增加右键菜单内容"""
        refreshAction = QAction('刷新', self)
        refreshAction.triggered.connect(self.refresh)

        self.menu.addAction(refreshAction)

    # ----------------------------------------------------------------------
    def show(self):
        """显示"""
        super(AssertMgtListView, self).show()
        self.refresh()
