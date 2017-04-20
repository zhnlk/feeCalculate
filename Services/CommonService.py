# encoding:utf8

from __future__ import unicode_literals

from datetime import date, timedelta

from sqlalchemy import and_

from models.AssetClassModel import AssetClass
from models.AssetTradeModel import AssetTrade
from models.CashModel import Cash
from models.CommonModel import session_deco
from models.TradeFeeModel import TradeFee
from utils import StaticValue as SV


# 通过资产id和交易类型获取现金记录
@session_deco
def get_cash_by_asset_and_type(asset_id='', trade_type=SV.CASH_TYPE_PURCHASE, **kwargs):
    return kwargs[SV.SESSION_KEY].query(Cash).filter(Cash.asset_class == asset_id, Cash.type == trade_type)


# 通过资产id和交易类型获取交易记录
@session_deco
def get_trade_by_asset_and_type(asset_id='', trade_type=SV.ASSET_TYPE_PURCHASE, **kwargs):
    return kwargs[SV.SESSION_KEY].query(AssetTrade).filter(AssetTrade.asset_class == asset_id,
                                                           AssetTrade.type == trade_type)


# 获取交易费用
@session_deco
def get_trade_fee_by_asset_and_type(asset_trade_id='', fee_type=SV.FEE_TYPE_PURCHASE, **kwargs):
    return kwargs[SV.SESSION_KEY].query(TradeFee).filter(TradeFee.asset_trade == asset_trade_id,
                                                         TradeFee.type == fee_type)


# 保存记录
@session_deco
def save(obj=None, **kwargs):
    return kwargs[SV.SESSION_KEY].add(obj)


# 删除记录
@session_deco
def delete(obj=None, key='', **kwargs):
    session = kwargs[SV.SESSION_KEY]
    del_obj = session.query(obj).filter(obj.id == key)
    del_obj.update({obj.is_active: False})


# 查询记录
@session_deco
def query(obj=None, **kwargs):
    session = kwargs[SV.SESSION_KEY]
    return session.query(obj).filter(obj.is_active == True)


# 更新记录
@session_deco
def update(obj=None, query_key='', update_data={}, **kwargs):
    session = kwargs[SV.SESSION_KEY]
    session.query(obj).filter(obj.id == query_key).update(update_data)


@session_deco
def add_asset_class(asset=AssetClass(), asset_fees=[], **kwargs):
    session = kwargs[SV.SESSION_KEY]
    session.add(asset)
    for asset_fee in asset_fees:
        asset_fee.asset_class = asset.id
        session.add(asset_fee)


@session_deco
def get_obj_by_id(obj=None, obj_id='', **kwargs):
    ret = kwargs[SV.SESSION_KEY].query(obj).filter(obj.id == obj_id)
    if ret:
        ret = ret.one()
    return ret


@session_deco
def get_asset_by_name(name='', **kwargs):
    ret = kwargs[SV.SESSION_KEY].query(AssetClass).filter(AssetClass.name == name)
    if ret:
        ret = ret.one()
    return ret


# 买入资产
@session_deco
def purchase(asset=AssetClass(), amount=0.0, cal_date=date.today(), **kwargs):
    session = kwargs[SV.SESSION_KEY]
    session.add(Cash(amount=amount, asset_class=asset.id, type=SV.CASH_TYPE_PURCHASE, cal_date=cal_date))

    # purchase_fees = session.query(AssetFeeRate).filter(AssetFeeRate.asset_class == asset.id,
    #                                                    AssetFeeRate.type == SV.FEE_TYPE_PURCHASE)
    purchase_fees = filter(lambda x: x.type == SV.FEE_TYPE_PURCHASE, asset.asset_fee_rate_list)
    asset_trade = AssetTrade(amount=amount, type=SV.ASSET_TYPE_PURCHASE, asset_class=asset.id, cal_date=cal_date)
    session.add(asset_trade)
    reduce_amount = amount
    for purchase_fee in purchase_fees:
        if purchase_fee.method == SV.FEE_METHOD_TIMES:
            reduce_amount -= purchase_fee.rate
            session.add(TradeFee(asset_trade=asset_trade.id, type=SV.FEE_TYPE_PURCHASE, amount=purchase_fee.rate,
                                 cal_date=cal_date))

        elif purchase_fee.method == SV.FEE_METHOD_RATIO:
            reduce_amount -= amount * purchase_fee.rate
            session.add(
                TradeFee(asset_trade=asset_trade.id, type=SV.FEE_TYPE_PURCHASE, amount=amount * purchase_fee.rate,
                         cal_date=cal_date))


# 卖出资产
@session_deco
def redeem(asset=AssetClass(), amount=0.0, cal_date=date.today(), **kwargs):
    session = kwargs[SV.SESSION_KEY]
    session.add(Cash(amount=amount, asset_class=asset.id, type=SV.CASH_TYPE_REDEEM, cal_date=cal_date))
    # redeem_fees = session.query(AssetFeeRate).filter(AssetFeeRate.asset_class == asset.id,
    #                                                  AssetFeeRate.type == SV.FEE_TYPE_REDEEM)

    redeem_fees = filter(lambda x: x.type == SV.FEE_TYPE_REDEEM, asset.asset_fee_rate_list)
    asset_trade = AssetTrade(amount=amount, type=SV.ASSET_TYPE_REDEEM, asset_class=asset.id, cal_date=cal_date)
    reduce_amount = amount
    session.add(asset_trade)
    for redeem_fee in redeem_fees:
        if redeem_fee.method == SV.FEE_METHOD_TIMES:
            reduce_amount -= redeem_fee.rate
            session.add(TradeFee(asset_trade=asset_trade.id, type=SV.FEE_TYPE_REDEEM, amount=redeem_fee.rate,
                                 cal_date=cal_date))

        elif redeem_fee.method == SV.FEE_METHOD_RATIO:
            reduce_amount -= amount * redeem_fee.rate
            session.add(
                TradeFee(asset_trade=asset_trade.id, type=SV.FEE_TYPE_REDEEM, amount=amount * redeem_fee.rate,
                         cal_date=cal_date))


# 统计各类资产的买入卖出
@session_deco
def get_asset_trade_change(cal_date=date.today(), asset_type=SV.ASSET_CLASS_AGREEMENT_DEPOSIT,
                           trade_type=SV.ASSET_TYPE_PURCHASE, **kwargs):
    session = kwargs[SV.SESSION_KEY]
    assets = session.query(AssetClass).filter(AssetClass.type == asset_type)
    asset_trades = []

    for asset in assets:
        asset_trades += asset.asset_trade_list

    asset_trades = filter(
        lambda y: y.type == trade_type and y.date >= cal_date and y.date < cal_date + timedelta(days=1), asset_trades)

    return list(asset_trades)


# 统计现在流入流出
@session_deco
def get_cash_trade_change(cal_date=date.today(), asset_type=SV.ASSET_CLASS_FUND, trade_type=SV.CASH_TYPE_PURCHASE,
                          **kwargs):
    session = kwargs[SV.SESSION_KEY]
    cashs = session.query(Cash).filter(Cash.asset_class_obj.has(AssetClass.type == asset_type), Cash.type == trade_type,
                                       and_(Cash.date >= cal_date, Cash.date < cal_date + timedelta(days=1)))

    return list(cashs)


if __name__ == '__main__':
    # save(Cash(amount=100000, type=SV.CASH_TYPE_DEPOSIT))
    # save(AssetClass(name='余额宝', code='10001', type=SV.ASSET_CLASS_FUND, ret_rate=0.04))
    # save(AssetClass(name='浦发理财一号', code='20007', type=SV.ASSET_CLASS_AGREEMENT_DEPOSIT, ret_rate=0.035))
    # agree = AssetClass(name='联顺泰', code='20007', type=SV.ASSET_CLASS_MANAGEMENT, ret_rate=0.08)
    #
    # save(AssetFeeRate(asset_class=agree.id, rate=20, type=SV.FEE_TYPE_PURCHASE, method=SV.FEE_METHOD_TIMES))
    # save(AssetFeeRate(asset_class=agree.id, rate=0.015, type=SV.FEE_TYPE_REDEEM, method=SV.FEE_METHOD_RATIO))
    # save(agree)

    # update(AssetClass, query_key='80f6f6baa8a343788c75abf10cf1bae9', update_data={AssetClass.is_active: True})

    asset = get_asset_by_name(name='联顺泰')
    purchase(asset=asset, amount=10000, cal_date=date.today() + timedelta(days=10))
    redeem(asset=asset, amount=5000)
    # print(get_asset_trade_change(asset_type=SV.ASSET_CLASS_FUND, trade_type=SV.ASSET_TYPE_REDEEM))
    # print(get_cash_trade_change())
    # print(asset.cash_list)
    # print(asset.asset_trade_list)
    # print(asset.asset_trade_list[1].trade_fee_list)
    #
    # # pass
    # # save(Cash(amount=100000, type=0))
    # # asset_class = AssetClass(name='现金宝', code='10008', type=1, ret_rate=0.038)
    # # save(AssetFeeRate(asset_class=asset_class.id, rate=5, type=SV.FEE_TYPE_PURCHASE, method=SV.FEE_METHOD_TIMES))
    # # save(AssetFeeRate(asset_class=asset_class.id, rate=0.015, type=SV.FEE_TYPE_PURCHASE, method=SV.FEE_METHOD_RATIO))
    # # save(AssetFeeRate(asset_class=asset_class.id, rate=0.015, type=SV.FEE_TYPE_REDEEM, method=SV.FEE_METHOD_RATIO))
    # # save(AssetFeeRate(asset_class=asset_class.id, rate=0.025, type=SV.FEE_TYPE_REDEEM, method=SV.FEE_METHOD_RATIO))
    # # save(asset_class)
    # #
    # # asset = get_asset_by_name('现金宝')
    # # purchase(asset=asset, amount=10000)
    # # redeem(asset=asset, amount=5000)
