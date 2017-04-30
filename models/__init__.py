# encoding:utf8

from __future__ import unicode_literals

from models import CashModel, AssetClassModel, AssetFeeModel, AssetTradeModel, AssetFeeRateModel, AssetTradeRetModel, \
    AssetRetRateModel, DailyFeeModel
from models.CommonModel import init_db


def models_all():
    result = []
    models = [AssetClassModel, CashModel, AssetTradeModel, AssetFeeModel, AssetFeeRateModel, AssetTradeRetModel,
              AssetRetRateModel, DailyFeeModel]
    map(lambda m: result.append(m.__all__), models)
    return result


__all__ = models_all()
init_db()
