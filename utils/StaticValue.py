# encoding:utf8

from __future__ import unicode_literals

# 资产类型
import os
import sys

ASSET_CLASS_AGREEMENT = 2  # 协存
ASSET_CLASS_FUND = 3  # 货基
ASSET_CLASS_MANAGEMENT = 4  # 资管

##现金变化类型
CASH_TYPE_PURCHASE = -1  # 申购资产
CASH_TYPE_PURCHASE_AGREEMENT = -2
CASH_TYPE_PURCHASE_FUND = -3
CASH_TYPE_PURCHASE_MANAGEMENT = -4
CASH_TYPE_REDEEM = 1  # 赎回资产
CASH_TYPE_REDEEM_AGREEMENT = 2
CASH_TYPE_REDEEM_FUND = 3
CASH_TYPE_REDEEM_MANAGEMENT = 4
CASH_TYPE_DEPOSIT = 5  # 存入
CASH_TYPE_DRAW = 6  # 提出
CASH_TYPE_FEE = 7  # 提出费用
CASH_TYPE_RET = 8  # 现金收入
CASH_TYPE_CARRY = 9  # 收益结转
CASH_TYPE_INIT = 0  # 初始化

CASH_KEY_TOTAL_AMOUNT = 'cash_total_amount'
CASH_KEY_PURCHASE_MANAGEMENT = 'cash_to_management'
CASH_KEY_PURCHASE_FUND = 'cash_to_fund'
CASH_KEY_PURCHASE_AGREEMENT = 'cash_to_agreement'
CASH_KEY_INVESTOR_DRAW = 'cash_to_investor'
CASH_KEY_REDEEM_MANAGEMENT = 'management_to_cash'
CASH_KEY_REDEEM_FUND = 'fund_to_cash'
CASH_KEY_REDEEM_AGREEMENT = 'agreement_to_cash'
CASH_KEY_INVESTOR_DEPOSIT = 'investor_to_cash'
CASH_KEY_RET = 'cash_return'
CASH_KEY_DRAW_FEE = 'cash_draw_fee'
CASH_KEY_CAL_DATE = 'cal_date'
CASH_KEY_CASH_TOTAL = 'total_amount'

# 资产变化类型
ASSET_TYPE_PURCHASE = 1  # 申购资产
ASSET_TYPE_REDEEM = -1  # 赎回资产
ASSET_TYPE_RET_CARRY = 2  # 收益结转
ASSET_TYPE_INIT = 0  # 初始化

ASSET_KEY_NAME = 'asset_name'
ASSET_KEY_CAL_DATE = CASH_KEY_CAL_DATE
ASSET_KEY_PURCHASE_AGREEMENT = CASH_KEY_PURCHASE_AGREEMENT
ASSET_KEY_PURCHASE_FUND = CASH_KEY_PURCHASE_FUND
ASSET_KEY_PURCHASE_MANAGEMENT = CASH_KEY_PURCHASE_MANAGEMENT
ASSET_KEY_REDEEM_AGREEMENT = CASH_KEY_REDEEM_AGREEMENT
ASSET_KEY_REDEEM_FUND = CASH_KEY_REDEEM_FUND
ASSET_KEY_REDEEM_MANAGEMENT = CASH_KEY_REDEEM_MANAGEMENT
ASSET_KEY_ASSET_TOTAL = CASH_KEY_CASH_TOTAL
ASSET_KEY_ASSET_RET = 'asset_ret'
ASSET_KEY_RATE = 'rate'
ASSET_KEY_RET_CARRY_PRINCIPAL = 'ret_carry_principal'
ASSET_KEY_PRINCIPAL = 'total_principal'
ASSET_KEY_RET_CARRY_CASH = 'ret_carry_cash'
ASSET_KEY_RET_NOT_CARRY = 'ret_not_carry'
ASSET_KEY_START_DATE = 'start_date'
ASSET_KEY_EXPIRY_DATE = 'expiry_date'
ASSET_KEY_MANAGEMENT_DUE = 'management_due'
ASSET_KEY_MANAGEMENT_BANK_FEE = 'bank_fee'
ASSET_KEY_MANAGEMENT_MANAGE_FEE = 'manage_fee'
ASSET_KEY_MANAGEMENT_AMOUNT = 'management_amount'
ASSET_KEY_MANAGEMENT_DAILY_RET = 'mamangement_daily_ret'
ASSET_KEY_MANAGEMENT_RET = 'management_ret'
ASSET_KEY_MANAGEMENT_RET_RATE = 'ret_rate'

ASSET_KEY_FUND_TOTAL_AMOUNT = 'total_amount'
ASSET_KEY_FUND_TOTAL_PURCHASE_AMOUNT = 'total_purchase_amount'
ASSET_KEY_FUND_TOTAL_REDEEM_AMOUNT = 'total_redeem_amount'
ASSET_KEY_FUND_TOTAL_RET_AMOUNT = 'total_ret_amount'

ASSET_KEY_ASSET_ID = 'uuid'

ASSET_KEY_ALL_EVALUATE_CASH = 'cash'
ASSET_KEY_ALL_EVALUATE_AGREEMENT = 'agreement'
ASSET_KEY_ALL_EVALUATE_FUND = 'fund'
ASSET_KEY_ALL_EVALUATE_MANAGEMENT = 'management'
ASSET_KEY_ALL_EVALUATE_RET = 'all_ret'
ASSET_KEY_ALL_VALUE = 'all_value'
ASSET_KEY_ALL_CURRENT_RATE = 'curr_rate'
ASSET_KEY_FEE_AMOUNT = 'fee_amount'
ASSET_KEY_FEE_TYPE = 'fee_type'

# 收益变化类型
RET_TYPE_INTEREST = 1  # 收益
RET_TYPE_PRINCIPAL = 0  # 结转本金
RET_TYPE_CASH = -1  # 结转现金
RET_TYPE_CASH_CUT_INTEREST = 2  # 砍头息
RET_TYPE_CASH_ONE_TIME = 3  # 到期结息
RET_TYPE_INIT = -2  # 初始化
RET_TYPE_NOT_CARRY = -3

# 费用扣取方式
FEE_METHOD_RATIO_ONE_TIME = 0
FEE_METHOD_RATIO_EVERY_DAY = 1
FEE_METHOD_RATIO_TIMES = 2

# 费用路径
FEE_TYPE_PURCHASE = 0  # 申购
FEE_TYPE_REDEEM = 1  # 赎回
FEE_TYPE_ADJUST_BANK = 2  # 银行费用
FEE_TYPE_ADJUST_CHECK = 3  # 支票费用
FEE_TYPE_LOAN_BANK = 4  # 委贷银行费率
FEE_TYPE_MANAG_PLAN = 5  # 资管计划费用
FEE_TYPE_INIT = -1  # 初始化
FEE_TYPE_COST = 6  # 资金成本

# 结转

RET_CARRY_TO_CASH = 0
RET_CARRY_TO_PRINCIPAL = 1

SESSION_KEY = 'session'

EMPTY_STRING = ''
EMPTY_UNICODE = ''
EMPTY_INT = 0
EMPTY_FLOAT = 0.0

####################
# 程序相关设置
####################
ICON_FILENAME = 'zhnlk.ico'
DB_FILENAME = 'data-beta.db'


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


path = os.path.dirname(__file__)
ICON_FILENAME = resource_path(os.path.join(path, ICON_FILENAME))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + resource_path(os.path.join(path, DB_FILENAME))

CASH_TYPE_TO_KEY_DIC = {
    CASH_TYPE_DEPOSIT: "现金->兑付投资人",
    CASH_TYPE_DRAW: "投资人->现金",
    CASH_TYPE_RET: "现金收入",
    CASH_TYPE_FEE: "提出费用"
}

CASH_KEY_TO_TYPE_DIC = {
    "现金->兑付投资人": CASH_TYPE_DEPOSIT,
    "投资人->现金": CASH_TYPE_DRAW,
    "现金收入": CASH_TYPE_RET,
    "提出费用": CASH_TYPE_FEE
}

AGREEMENT_TYPE_TO_KEY_DIC = {
    ASSET_TYPE_PURCHASE: '现金->协存',
    ASSET_TYPE_REDEEM: '协存->现金',
    ASSET_TYPE_RET_CARRY: '利息结转本金'
}

AGREEMENT_KEY_TO_TYPE_DIC = {
    '现金->协存': ASSET_TYPE_PURCHASE,
    '协存->现金': ASSET_TYPE_REDEEM,
    '利息结转本金': ASSET_TYPE_RET_CARRY
}

FUND_TYPE_TO_KEY_DIC = {
    True: {
        ASSET_TYPE_PURCHASE: "申购(现金)",
        ASSET_TYPE_REDEEM: "赎回",
    },
    False: {
        RET_TYPE_PRINCIPAL: "结转金额",
        RET_TYPE_INTEREST: "未结转金额"
    }
}

FUND_KEY_TO_TYPE_DIC = {
    True: {
        "申购(现金)": ASSET_TYPE_PURCHASE,
        "赎回": ASSET_TYPE_REDEEM,
    },
    False: {
        "结转金额": RET_TYPE_PRINCIPAL,
        "未结转金额": RET_TYPE_INTEREST
    }
}
