# encoding:utf8

from __future__ import unicode_literals

from models import CashModel, AssetClassModel, TradeFeeModel, AssetTradeModel, AssetFeeRateModel, AssetTradeRetModel
from models.CommonModel import init_db


def models_all():
    result = []
    models = [AssetClassModel, CashModel, AssetTradeModel, TradeFeeModel, AssetFeeRateModel, AssetTradeRetModel]
    map(lambda m: result.append(m.__all__), models)
    return result


__all__ = models_all()
init_db()
