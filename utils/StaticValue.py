# encoding:utf8

from __future__ import unicode_literals

# 资产类型
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
ASSET_TYPE_OTHERS = 0  # 其它

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
ASSET_KEY_RET_CARRY_CASH = 'ret_carry_cash'
ASSET_KEY_RET_NOT_CARRY = 'ret_not_carry'

# 收益变化类型
RET_TYPE_INTEREST = 1
RET_TYPE_PRINCIPAL = 0
RET_TYPE_CASH = -1

# 费用扣取方式
FEE_METHOD_RATIO = 0  # 按比例
FEE_METHOD_TIMES = 1  # 按次数

# 费用路径
FEE_TYPE_PURCHASE = -1  # 申购
FEE_TYPE_REDEEM = 1  # 赎回

# 结转

RET_CARRY_TO_CASH = 0
RET_CARRY_TO_PRINCIPAL = 1

SESSION_KEY = 'session'
