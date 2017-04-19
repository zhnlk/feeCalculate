# encoding:utf8

from __future__ import unicode_literals

# 资产类型
ASSET_CLASS_AGREEMENT_DEPOSIT = 0  # 协存
ASSET_CLASS_FUND = 1  # 货基
ASSET_CLASS_MANAGEMENT = 2  # 资管

##现金变化类型
CASH_TYPE_PURCHASE = -1  # 申购资产
CASH_TYPE_REDEEM = 1  # 赎回资产
CASH_TYPE_DEPOSIT = 2  # 存入
CASH_TYPE_DRAW = 3  # 提出
CASH_TYPE_FEE = 4  # 提出费用
CASH_TYPE_RET = 5  # 现金收入
CASH_TYPE_CARRY = 6

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
CASH_KEY_CASH_TOTAL = 'cash_total'

# 资产变化类型
ASSET_TYPE_PURCHASE = 1  # 申购资产
ASSET_TYPE_REDEEM = -1  # 赎回资产
ASSET_TYPE_RET_CARRY = 2  # 收益结转
ASSET_TYPE_OTHERS = 0  # 其它

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
