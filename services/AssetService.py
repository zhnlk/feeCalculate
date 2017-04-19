# encoding:utf8
from __future__ import unicode_literals

from datetime import date

from models.AssetClassModel import AssetClass
from models.AssetTradeModel import AssetTrade
from models.AssetTradeRetModel import AssetTradeRet
from models.CashModel import Cash
from models.CommonModel import session_deco
from services.CommonService import query, purchase, redeem
from utils import StaticValue as SV


@session_deco
def asset_ret_carry_to_principal(cal_date=date.today(), asset=AssetClass(), amount=0, **kwargs):
    session = kwargs[SV.SESSION_KEY]
    # asset_ret = query(AssetTrade).filter(AssetTradeRet.asset_class == asset_id,
    #                                      AssetTradeRet.date < cal_date + timedelta(days=1),
    #                                      AssetTradeRet.type == SV.RET_TYPE_INTEREST)

    if amount > 0:
        asset_trade_ret = AssetTradeRet(asset_class=asset.id, type=SV.RET_TYPE_PRINCIPAL, amount=amount)
        asset_trade_ret.date = cal_date
        session.add(asset_trade_ret)
        asset_trade = AssetTrade(asset_class=asset.id, amount=amount, type=SV.ASSET_TYPE_RET_CARRY)
        asset_trade.date = cal_date
        session.add(asset_trade)
    else:
        pass


@session_deco
def add_trade_ret(cal_date=date.today(), ret_amount=0, asset=AssetClass(), **kwargs):
    session = kwargs[SV.SESSION_KEY]
    session.add(AssetTradeRet(asset_class=asset.id, amount=ret_amount, type=SV.RET_TYPE_INTEREST, cal_date=cal_date))


@session_deco
def asset_ret_carry_to_cash(cal_date=date.today(), asset=AssetClass(), amount=0, **kwargs):
    session = kwargs[SV.SESSION_KEY]
    if amount > 0:
        session.add(AssetTradeRet(asset_class=asset.id, type=SV.RET_TYPE_CASH, amount=amount, cal_date=cal_date))
        session.add(Cash(asset_class=asset.id, type=SV.CASH_TYPE_CARRY, amount=amount, cal_date=cal_date))


def add_daily_asset_data(cal_date=date.today(), asset_id='', ret_carry_amount=0, purchase_amount=0,
                         redeem_amount=0):
    asset = query(AssetClass).filter(AssetClass.id == asset_id).one()
    asset_ret_carry_to_principal(cal_date=cal_date, asset_id=asset, amount=ret_carry_amount)
    purchase(asset=asset, amount=purchase_amount)
    redeem(asset=asset, amount=redeem_amount)


if __name__ == '__main__':
    # print(list(query(AssetTrade).filter(AssetTrade.type == SV.ASSET_TYPE_REDEEM, AssetTrade.asset_class_obj.has(
    #     AssetClass.type == SV.ASSET_CLASS_FUND))))

    add_daily_asset_data(asset_id='10e8743354f14fa383898d03a494c1af', ret_carry_amount=1001, purchase_amount=1002,
                         redeem_amount=1003)
