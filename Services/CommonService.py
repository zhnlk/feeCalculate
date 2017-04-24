# encoding:utf8

from __future__ import unicode_literals

from datetime import date, timedelta

from sqlalchemy import and_, func

from models.AssetClassModel import AssetClass
from models.AssetFeeModel import AssetFee
from models.AssetTradeModel import AssetTrade
from models.AssetTradeRetModel import AssetTradeRet
from models.CashModel import Cash
from models.CommonModel import session_deco
from utils import StaticValue as SV


##### Cash


@session_deco
def get_cash_total_amount_by_type(cal_date=date.today(), cash_type=SV.CASH_TYPE_DEPOSIT, **kwargs):
    """
    获取指定日期指定类型的现金总额
    :param cal_date:计算日期
    :param cash_type:现金类型
    :param kwargs:可扩展产数
    :return:指定日期及类型的总额
    """
    session = kwargs.get(SV.SESSION_KEY, None)
    ret = session.query(func.sum(Cash.amount).label('total_amount')).filter(
        Cash.is_active,
        Cash.type == cash_type,
        Cash.date < cal_date + timedelta(days=1)
    ).one()
    return ret.total_amount if ret.total_amount else 0.0


@session_deco
def get_cash_last_total_amount_by_type(cal_date=date.today(), cash_type=SV.CASH_TYPE_PURCHASE, **kwargs):
    session = kwargs.get(SV.SESSION_KEY, None)
    ret = session.query(Cash, func.max(Cash.time).label('max_time')).filter(
        Cash.is_active,
        Cash.date < cal_date + timedelta(days=1),
        Cash.type == cash_type
    ).one()

    return ret.Cash.total_amount if ret.Cash else 0.0


def add_cash_with_type(amount=0, cash_type=SV.CASH_TYPE_DEPOSIT, asset_id='', cal_date=date.today()):
    save(
        Cash(
            amount=amount, type=cash_type,
            cal_date=cal_date,
            total_amount=get_cash_last_total_amount_by_type(cal_date=cal_date, cash_type=cash_type) + amount,
            asset_class=asset_id)
    )


#### AssetTrade

@session_deco
def get_asset_total_amount_by_asset_and_type(cal_date=date.today(), asset_id='', trade_type=SV.ASSET_TYPE_PURCHASE,
                                             **kwargs):
    session = kwargs.get(SV.SESSION_KEY, None)
    ret = session.query(func.sum(AssetTrade.amount).label('total_amount')).filter(
        AssetTrade.is_active,
        AssetTrade.type == trade_type,
        AssetTrade.asset_class == asset_id,
        AssetTrade.date < cal_date + timedelta(days=1)
    ).one()
    return ret.total_amount if ret.total_amount else 0.0


@session_deco
def get_asset_last_total_amount_by_asset_and_type(cal_date=date.today(), asset_id='', trade_type=SV.ASSET_TYPE_PURCHASE,
                                                  **kwargs):
    session = kwargs.get(SV.SESSION_KEY, None)
    ret = session.query(AssetTrade, func.max(AssetTrade.time).label('max_time')).filter(
        AssetTrade.is_active,
        AssetTrade.asset_class == asset_id,
        AssetTrade.type == trade_type,
        AssetTrade.date < cal_date + timedelta(days=1)
    ).one()
    return ret.AssetTrade.total_amount if ret.AssetTrade else 0.0


def add_asset_trade_with_asset_and_type(amount=0.0, trade_type=SV.ASSET_TYPE_PURCHASE, asset_id='',
                                        cal_date=date.today()):
    save(AssetTrade(asset_class=asset_id, amount=amount, type=trade_type,
                    total_amount=get_asset_last_total_amount_by_asset_and_type(cal_date=cal_date, asset_id=asset_id,
                                                                               trade_type=trade_type) + amount,
                    cal_date=cal_date))


#### AssetTradeRet
@session_deco
def get_asset_ret_last_total_amount_by_asset_and_type(cal_date=date.today(), asset_id='', ret_type=SV.RET_TYPE_CASH,
                                                      **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    ret = session.query(AssetTradeRet, func.max(AssetTradeRet.time).label('max_time')).filter(
        AssetTradeRet.is_active,
        AssetTradeRet.asset_class == asset_id,
        AssetTradeRet.type == ret_type,
        AssetTradeRet.date < cal_date + timedelta(days=1)
    ).one()
    return ret.AssetTradeRet.total_amount if ret.AssetTradeRet else 0.0


@session_deco
def get_asset_ret_total_amount_by_asset_and_type(cal_date=date.today(), asset_id='', ret_type=SV.RET_TYPE_CASH,
                                                 **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    ret = session.query(func.sum(AssetTradeRet.amount).label('total_amount')).filter(
        AssetTradeRet.is_active,
        AssetTradeRet.asset_class == asset_id,
        AssetTradeRet.type == ret_type,
        AssetTradeRet.date < cal_date + timedelta(days=1)
    ).one()
    return ret.total_amount if ret.total_amount else 0.0


def add_asset_ret_with_asset_and_type(amount=0.0, asset_id='', ret_type=SV.RET_TYPE_CASH, cal_date=date.today()):
    save(
        AssetTradeRet(
            asset_class=asset_id,
            amount=amount,
            type=ret_type,
            cal_date=cal_date,
            total_amount=get_asset_ret_last_total_amount_by_asset_and_type(cal_date=cal_date,
                                                                           asset_id=asset_id,
                                                                           ret_type=ret_type
                                                                           ) + amount
        )
    )


#### AssetFee


@session_deco
def get_asset_fee_last_total_amount_by_asset_and_type(cal_date=date.today(), asset_id='', fee_type=SV.FEE_TYPE_PURCHASE,
                                                      **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    ret = session.query(AssetFee, func.max(AssetFee.time).label('max_time')).filter(
        AssetFee.is_active,
        AssetFee.asset_class == asset_id,
        AssetFee.type == fee_type,
        AssetFee.date < cal_date + timedelta(days=1)

    ).one()
    return ret.AssetFee.total_amount if ret.AssetFee else 0.0


@session_deco
def get_asset_fee_total_amount_by_asset_and_type(cal_date=date.today(), asset_id='', fee_type=SV.FEE_TYPE_PURCHASE,
                                                 **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    ret = session.query(func.sum(AssetFee.amount).label('total_amount')).filter(
        AssetFee.is_active,
        AssetFee.asset_class == asset_id,
        AssetFee.type == fee_type,
        AssetFee.date < cal_date + timedelta(days=1)
    ).one()
    return ret.total_amount if ret.total_amount else 0.0


def add_asest_fee_with_asset_and_type(amount=0, asset_id='', fee_type=SV.FEE_TYPE_PURCHASE, cal_date=date.today()):
    save(
        AssetFee(
            asset_class=asset_id,
            amount=amount,
            type=fee_type,
            cal_date=cal_date,
            total_amount=get_asset_fee_last_total_amount_by_asset_and_type(
                cal_date=cal_date, asset_id=asset_id, fee_type=fee_type
            ) + amount
        )
    )


#########################



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
    return kwargs[SV.SESSION_KEY].query(AssetFee).filter(AssetFee.asset_trade == asset_trade_id,
                                                         AssetFee.type == fee_type)


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
    return session.query(obj).filter(obj.is_active)


@session_deco
def query_by_id(obj=AssetClass(), obj_id='', **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    return session.query(obj).filter(obj.is_active, obj.id == obj_id).one()


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
def purchase(asset=AssetClass(), amount=0.0, cal_date=date.today()):
    add_cash_with_type(amount=amount, cash_type=-asset.type, asset_id=asset.id, cal_date=cal_date)
    add_asset_trade_with_asset_and_type(
        asset_id=asset.id,
        trade_type=SV.ASSET_TYPE_PURCHASE,
        amount=amount,
        cal_date=cal_date
    )


# 卖出资产
def redeem(asset=AssetClass(), amount=0.0, cal_date=date.today()):
    add_cash_with_type(amount=amount, cash_type=asset.type, asset_id=asset.id, cal_date=cal_date)
    add_asset_trade_with_asset_and_type(
        amount=amount,
        asset_id=asset.id,
        trade_type=SV.ASSET_TYPE_REDEEM,
        cal_date=cal_date
    )
    # asset_trade = AssetTrade(amount=amount, type=SV.ASSET_TYPE_REDEEM, asset_class=asset.id, cal_date=cal_date)
    # reduce_amount = amount
    # session.add(asset_trade)
    # # for redeem_fee in redeem_fees:
    # #     if redeem_fee.method == SV.FEE_METHOD_TIMES:
    # #         reduce_amount -= redeem_fee.rate
    # #         session.add(TradeFee(asset_trade=asset_trade.id, type=SV.FEE_TYPE_REDEEM, amount=redeem_fee.rate,
    # #                              cal_date=cal_date))
    # #
    # #     elif redeem_fee.method == SV.FEE_METHOD_RATIO:
    # #         reduce_amount -= amount * redeem_fee.rate
    # #         session.add(
    # #             TradeFee(asset_trade=asset_trade.id, type=SV.FEE_TYPE_REDEEM, amount=amount * redeem_fee.rate,
    # #                      cal_date=cal_date))
    # asset_trade.amount = reduce_amount
    # session.add(asset_trade)


# 统计各类资产的买入卖出
@session_deco
def get_asset_trade_change(cal_date=date.today(), asset_type=SV.ASSET_CLASS_AGREEMENT,
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
    # agreement = (AssetClass(name='浦发理财一号', code='20007', type=SV.ASSET_CLASS_AGREEMENT, ret_rate=0.035))
    # save(AssetRetRate(asset_id=agreement.id, ret_rate=0.03, threshold=0))
    # save(AssetRetRate(asset_id=agreement.id, ret_rate=0.1, threshold=10000))
    # save(agreement)
    # agree = AssetClass(name='联顺泰', code='20007', type=SV.ASSET_CLASS_MANAGEMENT, ret_rate=0.08)
    #
    # save(AssetFeeRate(asset_class=agree.id, rate=20, type=SV.FEE_TYPE_PURCHASE, method=SV.FEE_METHOD_RATIO_ONE_TIME))
    # save(AssetFeeRate(asset_class=agree.id, rate=0.015, type=SV.FEE_TYPE_REDEEM, method=SV.FEE_METHOD_RATIO_EVERY_DAY))
    # save(agree)

    # update(AssetClass, query_key='80f6f6baa8a343788c75abf10cf1bae9', update_data={AssetClass.is_active: True})

    # print(get_asset_last_total_amount_by_asset_and_type(cal_date=date.today(),
    #                                                     asset_id='6a2686b23dae4296868c2288d28b6a7a',
    #                                                     trade_type=SV.ASSET_TYPE_PURCHASE))

    # add_asset_trade_with_asset_and_type(amount=10000, asset_id='41216cc75f9c455fa4c309a177eef9e7',
    #                                     trade_type=SV.ASSET_TYPE_PURCHASE)
    # cal_date = date.today() - timedelta(days=5)
    asset = get_asset_by_name(name='浦发理财一号')
    purchase(asset=asset, amount=6000)
    # redeem(asset=asset, amount=15000, cal_date=cal_date)
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
