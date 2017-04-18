# encoding:utf8

from __future__ import unicode_literals

# 资产类型
ASSET_CLASS_AGREEMENT_DEPOSIT = 0  # 协存
ASSET_CLASS_FUND = 1  # 货基
ASSET_CLASS_MANAGEMENT = 2  # 资管

##现金变化类型
CASH_TYPE_PURCHASE = -1  # 申购资产
CASH_TYPE_REDEEM = 1  # 赎回资产
CASH_TYPE_DEPOSIT = 0  # 充值

# 资产变化类型
ASSET_TYPE_PURCHASE = 1  # 申购资产
ASSET_TYPE_REDEEM = -1  # 赎回资产
ASSET_TYPE_OTHERS = 0  # 其它

# 费用扣取方式
FEE_METHOD_RATIO = 0  # 按比例
FEE_METHOD_TIMES = 1  # 按次数

# 费用路径
FEE_TYPE_PURCHASE = -1  # 申购
FEE_TYPE_REDEEM = 1  # 赎回

SESSION_KEY = 'session'
