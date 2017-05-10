# encoding:utf8

from __future__ import unicode_literals

from datetime import date, timedelta

from sqlalchemy import and_, func, or_

from models.AssetClassModel import AssetClass
from models.AssetFeeModel import AssetFee
from models.AssetFeeRateModel import AssetFeeRate
from models.AssetRetRateModel import AssetRetRate
from models.AssetTradeModel import AssetTrade
from models.AssetTradeRetModel import AssetTradeRet
from models.CashModel import Cash
from models.CommonModel import session_deco
from models.DailyFeeModel import DailyFee
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
    # try:
    ret = session.query(Cash, func.max(Cash.time).label('max_time')).filter(
        Cash.is_active,
        Cash.date < cal_date + timedelta(days=1),
        Cash.type == cash_type
    ).one()

    return ret.Cash.total_amount if ret.Cash else 0.0


def add_cash_with_type(amount=0, cash_type=SV.CASH_TYPE_DEPOSIT, asset_id=None, cal_date=date.today()):
    save(
        Cash(
            amount=amount, type=cash_type,
            cal_date=cal_date,
            total_amount=get_cash_last_total_amount_by_type(cal_date=cal_date, cash_type=cash_type) + amount,
            asset_class=asset_id
        )
    )


#### AssetTrade

@session_deco
def get_asset_total_amount_by_asset_and_type(cal_date=date.today(), asset_id=None, trade_type=SV.ASSET_TYPE_PURCHASE,
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
def get_asset_last_total_amount_by_asset_and_type(cal_date=date.today(), asset_id=None,
                                                  trade_type=SV.ASSET_TYPE_PURCHASE,
                                                  **kwargs):
    session = kwargs.get(SV.SESSION_KEY, None)
    ret = session.query(AssetTrade, func.max(AssetTrade.time).label('max_time')).filter(
        AssetTrade.is_active,
        AssetTrade.asset_class == asset_id,
        AssetTrade.type == trade_type,
        AssetTrade.date < cal_date + timedelta(days=1)
    ).one()
    return ret.AssetTrade.total_amount if ret.AssetTrade else 0.0


def add_asset_trade_with_asset_and_type(amount=0.0, trade_type=SV.ASSET_TYPE_PURCHASE, asset_id=None,
                                        cal_date=date.today()):
    save(AssetTrade(asset_class=asset_id, amount=amount, type=trade_type,
                    total_amount=get_asset_last_total_amount_by_asset_and_type(cal_date=cal_date, asset_id=asset_id,
                                                                               trade_type=trade_type) + amount,
                    cal_date=cal_date))


#### AssetTradeRet
@session_deco
def get_asset_ret_last_total_amount_by_asset_and_type(cal_date=date.today(), asset_id=None, ret_type=SV.RET_TYPE_CASH,
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
def get_asset_ret_total_amount_by_asset_and_type(cal_date=date.today(), asset_id=None, ret_type=SV.RET_TYPE_CASH,
                                                 **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    ret = session.query(func.sum(AssetTradeRet.amount).label('total_amount')).filter(
        AssetTradeRet.is_active,
        AssetTradeRet.asset_class == asset_id,
        AssetTradeRet.type == ret_type,
        AssetTradeRet.date < cal_date + timedelta(days=1)
    ).one()
    return ret.total_amount if ret.total_amount else 0.0


@session_deco
def del_ret_by_asset_and_date(asset_id=None, cal_date=date.today(), ret_type=SV.RET_TYPE_CASH_CUT_INTEREST, **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    session.query(AssetTradeRet).filter(
        AssetTradeRet.is_active,
        AssetTradeRet.asset_class == asset_id,
        AssetTradeRet.date == cal_date,
        AssetTradeRet.type == ret_type,
        AssetTradeRet.asset_class_obj.has(AssetClass.type == SV.ASSET_CLASS_AGREEMENT)
    ).update(
        {AssetTradeRet.is_active: False},
        synchronize_session='fetch'
    )


def add_asset_ret_with_asset_and_type(amount=0.0, asset_id=None, ret_type=SV.RET_TYPE_CASH, cal_date=date.today()):
    if is_date_has_ret(asset_id=asset_id, cal_date=cal_date, ret_type=ret_type):
        del_ret_by_asset_and_date(asset_id=asset_id, cal_date=cal_date, ret_type=ret_type)
    last_total_amount = get_asset_ret_last_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset_id,
        ret_type=ret_type
    )
    save(
        AssetTradeRet(
            asset_class=asset_id,
            amount=amount,
            type=ret_type,
            cal_date=cal_date,
            total_amount=last_total_amount + amount
        )
    )


#### AssetFee


@session_deco
def get_asset_fee_last_total_amount_by_asset_and_type(cal_date=date.today(), asset_id=None,
                                                      fee_type=SV.FEE_TYPE_PURCHASE,
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
def get_asset_fee_total_amount_by_asset_and_type(cal_date=date.today(), asset_id=None, fee_type=SV.FEE_TYPE_PURCHASE,
                                                 **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    ret = session.query(func.sum(AssetFee.amount).label('total_amount')).filter(
        AssetFee.is_active,
        AssetFee.asset_class == asset_id,
        AssetFee.type == fee_type,
        AssetFee.date < cal_date + timedelta(days=1)
    ).one()
    return ret.total_amount if ret.total_amount else 0.0


def add_asset_fee_with_asset_and_type(amount=0, asset_id=None, fee_type=SV.FEE_TYPE_PURCHASE, cal_date=date.today()):
    save(
        AssetFee(
            asset_class=asset_id,
            amount=amount,
            type=fee_type,
            cal_date=cal_date,
            total_amount=get_asset_fee_last_total_amount_by_asset_and_type(
                cal_date=cal_date, asset_id=asset_id, fee_type=fee_type
            ) + amount,
        )
    )


# Management




#########################



# 通过资产id和交易类型获取现金记录
@session_deco
def get_cash_by_asset_and_type(asset_id=None, trade_type=SV.CASH_TYPE_PURCHASE, **kwargs):
    return kwargs[SV.SESSION_KEY].query(Cash).filter(Cash.asset_class == asset_id, Cash.type == trade_type)


# 通过资产id和交易类型获取交易记录
@session_deco
def get_trade_by_asset_and_type(asset_id=None, trade_type=SV.ASSET_TYPE_PURCHASE, **kwargs):
    return kwargs[SV.SESSION_KEY].query(AssetTrade).filter(AssetTrade.asset_class == asset_id,
                                                           AssetTrade.type == trade_type)


# 获取交易费用
@session_deco
def get_trade_fee_by_asset_and_type(asset_trade_id=None, fee_type=SV.FEE_TYPE_PURCHASE, **kwargs):
    return kwargs[SV.SESSION_KEY].query(AssetFee).filter(AssetFee.asset_trade == asset_trade_id,
                                                         AssetFee.type == fee_type)


# 保存记录
@session_deco
def save(obj=None, **kwargs):
    return kwargs[SV.SESSION_KEY].add(obj)


# 删除记录
@session_deco
def delete(obj=None, key=None, **kwargs):
    session = kwargs[SV.SESSION_KEY]
    del_obj = session.query(obj).filter(obj.id == key)
    del_obj.update({obj.is_active: False})


# 查询记录
@session_deco
def query(obj=None, **kwargs):
    session = kwargs[SV.SESSION_KEY]
    return session.query(obj).filter(obj.is_active)


@session_deco
def query_by_id(obj=AssetClass(), obj_id=None, **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    return session.query(obj).filter(obj.is_active, obj.id == obj_id).one()


# 更新记录
@session_deco
def update(obj=None, query_key=None, update_data={}, **kwargs):
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
def get_obj_by_id(obj=None, obj_id=None, **kwargs):
    ret = kwargs[SV.SESSION_KEY].query(obj).filter(obj.id == obj_id)
    if ret:
        ret = ret.one()
    return ret


@session_deco
def get_asset_by_name(name=None, **kwargs):
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


@session_deco
def get_management_asset_all_ret(asset_id=None, cal_date=date.today(), **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    asset = session.query(AssetClass).filter(AssetClass.is_active, AssetClass.id == asset_id).one()
    asset_ret = session.query(AssetRetRate).filter(AssetRetRate.is_active, AssetRetRate.asset_class == asset_id)
    if asset_ret.count():
        asset_ret = asset_ret.one()
    else:
        return 0.0

    return asset_ret.ret_rate * get_asset_last_total_amount_by_asset_and_type(cal_date=cal_date, asset_id=asset_id,
                                                                              trade_type=SV.ASSET_TYPE_PURCHASE) * (
               asset.expiry_date - asset.start_date).days / asset_ret.interest_days if asset_ret else 0.0


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


@session_deco
def get_management_trade_amount(asset_id=None, **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    managements = session.query(AssetTrade).filter(AssetTrade.is_active, AssetTrade.asset_class == asset_id)

    return managements[-1].total_amount if managements.count() else 0.0


@session_deco
def get_management_trade_fees(asset_id=None, **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    total_amount = get_management_trade_amount(asset_id=asset_id)
    fees = session.query(AssetFeeRate).filter(AssetFeeRate.is_active, AssetFeeRate.asset_class == asset_id)
    asset = query_by_id(obj=AssetClass, obj_id=asset_id)
    return list(map(lambda x: x, fees))


@session_deco
def get_all_mamangement_ids(**kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    ids = session.query(AssetClass.id).filter(AssetClass.is_active, AssetClass.type == SV.ASSET_CLASS_MANAGEMENT)
    return list(map(lambda x: x[0], ids))


@session_deco
def get_all_asset_ids_by_type(asset_type=SV.ASSET_CLASS_AGREEMENT, **kwargs):
    session = kwargs.get(SV.SESSION_KEY)

    assets = session.query(AssetClass.id, AssetClass.name).filter(AssetClass.is_active, AssetClass.type == asset_type)
    return list(assets)


@session_deco
def get_management_fees_by_id(cal_date=date.today(), asset_id=None, **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    fees = session.query(AssetFee).filter(
        AssetFee.is_active,
        AssetFee.date < cal_date + timedelta(days=1),
        AssetFee.asset_class == asset_id
    )
    return fees


def get_all_cash(cal_date=date.today()):
    purchase_amount = get_cash_total_amount_by_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_PURCHASE_FUND) \
                      + get_cash_total_amount_by_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_PURCHASE_AGREEMENT) \
                      + get_cash_total_amount_by_type(cal_date=cal_date,
                                                      cash_type=SV.CASH_TYPE_PURCHASE_MANAGEMENT)

    redeem_amount = get_cash_total_amount_by_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_REDEEM_AGREEMENT) \
                    + get_cash_total_amount_by_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_REDEEM_FUND) \
                    + get_cash_total_amount_by_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_REDEEM_MANAGEMENT)

    deposit_amount = get_cash_total_amount_by_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_DEPOSIT)
    ret_amount = get_cash_total_amount_by_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_RET)
    carry_amount = get_cash_total_amount_by_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_CARRY)
    draw_amount = get_cash_total_amount_by_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_DRAW)
    draw_fee_amount = get_cash_total_amount_by_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_FEE)
    return redeem_amount + deposit_amount + carry_amount + ret_amount - draw_fee_amount - draw_amount - purchase_amount


@session_deco
def get_all_agreement(cal_date=date.today(), **kwargs):
    session = kwargs.get(SV.SESSION_KEY)

    purchase_obj = session.query(func.sum(AssetTrade.amount).label('total_amount')).filter(AssetTrade.is_active,
                                                                                           AssetTrade.type == SV.ASSET_TYPE_PURCHASE,
                                                                                           AssetTrade.date < cal_date + timedelta(
                                                                                               days=1),
                                                                                           AssetTrade.asset_class_obj.has(
                                                                                               AssetClass.type == SV.ASSET_CLASS_AGREEMENT)).one()
    purchase_amount = purchase_obj.total_amount if purchase_obj.total_amount else 0.0

    redeem_obj = session.query(func.sum(AssetTrade.amount).label('total_amount')).filter(AssetTrade.is_active,
                                                                                         AssetTrade.type == SV.ASSET_TYPE_REDEEM,
                                                                                         AssetTrade.date < cal_date + timedelta(
                                                                                             days=1),
                                                                                         AssetTrade.asset_class_obj.has(
                                                                                             AssetClass.type == SV.ASSET_CLASS_AGREEMENT)).one()
    redeem_amount = redeem_obj.total_amount if redeem_obj.total_amount else 0.0
    ret_obj = session.query(func.sum(AssetTradeRet.amount).label('total_amount')).filter(AssetTradeRet.is_active,
                                                                                         AssetTradeRet.date < cal_date + timedelta(
                                                                                             days=1),
                                                                                         AssetTradeRet.type == SV.RET_TYPE_INTEREST,
                                                                                         AssetTradeRet.asset_class_obj.has(
                                                                                             AssetClass.type == SV.ASSET_CLASS_AGREEMENT)).one()
    ret_amount = ret_obj.total_amount if ret_obj.total_amount else 0.0
    return purchase_amount + ret_amount - redeem_amount


@session_deco
def get_all_fund(cal_date=date.today(), **kwargs):
    session = kwargs.get(SV.SESSION_KEY)

    purchase_obj = session.query(func.sum(AssetTrade.amount).label('total_amount')).filter(AssetTrade.is_active,
                                                                                           AssetTrade.type == SV.ASSET_TYPE_PURCHASE,
                                                                                           AssetTrade.date < cal_date + timedelta(
                                                                                               days=1),
                                                                                           AssetTrade.asset_class_obj.has(
                                                                                               AssetClass.type == SV.ASSET_CLASS_FUND)).one()
    purchase_amount = purchase_obj.total_amount if purchase_obj.total_amount else 0.0

    redeem_obj = session.query(func.sum(AssetTrade.amount).label('total_amount')).filter(AssetTrade.is_active,
                                                                                         AssetTrade.type == SV.ASSET_TYPE_REDEEM,
                                                                                         AssetTrade.date < cal_date + timedelta(
                                                                                             days=1),
                                                                                         AssetTrade.asset_class_obj.has(
                                                                                             AssetClass.type == SV.ASSET_CLASS_FUND)).one()
    redeem_amount = redeem_obj.total_amount if redeem_obj.total_amount else 0.0

    ret_obj = session.query(func.sum(AssetTradeRet.amount).label('total_amount')).filter(
        AssetTradeRet.is_active,
        AssetTradeRet.date < cal_date + timedelta(days=1),
        AssetTradeRet.type == SV.RET_TYPE_INTEREST,
        AssetTradeRet.asset_class_obj.has(AssetClass.type == SV.ASSET_CLASS_FUND)).one()

    ret_amount = ret_obj.total_amount if ret_obj.total_amount else 0.0
    return purchase_amount + ret_amount - redeem_amount


@session_deco
def get_all_management(cal_date=date.today(), **kwargs):
    session = kwargs.get(SV.SESSION_KEY)

    purchase_obj = session.query(func.sum(AssetTrade.amount).label('total_amount')).filter(
        AssetTrade.is_active,
        AssetTrade.type == SV.ASSET_TYPE_PURCHASE,
        AssetTrade.date < cal_date + timedelta(days=1),
        # and_(
        AssetTrade.asset_class_obj.has(AssetClass.type == SV.ASSET_CLASS_MANAGEMENT)
        # AssetTrade.asset_class_obj.has((AssetClass.expiry_date > cal_date))
        # )
    ).one()
    purchase_amount = purchase_obj.total_amount if purchase_obj.total_amount else 0.0

    redeem_obj = session.query(func.sum(AssetTrade.amount).label('total_amount')).filter(
        AssetTrade.is_active,
        AssetTrade.type == SV.ASSET_TYPE_REDEEM,
        AssetTrade.date < cal_date + timedelta(days=1),
        AssetTrade.asset_class_obj.has(
            AssetClass.type == SV.ASSET_CLASS_MANAGEMENT)).one()
    redeem_amount = redeem_obj.total_amount if redeem_obj.total_amount else 0.0

    ret_obj = session.query(func.sum(AssetTradeRet.amount).label('total_amount')).filter(
        AssetTradeRet.is_active,
        AssetTradeRet.date < cal_date + timedelta(days=1),
        AssetTradeRet.type == SV.RET_TYPE_INTEREST,
        AssetTradeRet.asset_class_obj.has(
            AssetClass.type == SV.ASSET_CLASS_MANAGEMENT)).one()
    ret_amount = ret_obj.total_amount if ret_obj.total_amount else 0.0

    fee_obj = session.query(func.sum(AssetFee.amount).label('total_amount')).filter(
        AssetFee.is_active,
        AssetFee.date < cal_date + timedelta(days=1),
        AssetFee.asset_class_obj.has(
            AssetClass.type == SV.ASSET_CLASS_MANAGEMENT
        )
    ).one()

    car_ret_obj = session.query(func.sum(AssetTradeRet.amount).label('total_amount')).filter(
        AssetTradeRet.is_active,
        AssetTradeRet.date < cal_date + timedelta(days=1),
        AssetTradeRet.type == SV.RET_TYPE_CASH,
        AssetTradeRet.asset_class_obj.has(
            AssetClass.type == SV.ASSET_CLASS_MANAGEMENT)).one()
    car_ret_amount = ret_obj.total_amount if car_ret_obj.total_amount else 0.0

    fee_amount = fee_obj.total_amount if fee_obj.total_amount else 0.0

    return purchase_amount + ret_amount - redeem_amount - fee_amount - car_ret_amount


@session_deco
def get_all_ret_daily(cal_date=date.today(), **kwargs):
    session = kwargs.get(SV.SESSION_KEY)

    ret_obj = session.query(func.sum(AssetTradeRet.amount).label('total_amount')).filter(AssetTradeRet.is_active,
                                                                                         AssetTradeRet.date == cal_date,
                                                                                         AssetTradeRet.type == SV.RET_TYPE_INTEREST).one()

    return ret_obj.total_amount if ret_obj.total_amount else 0.0


@session_deco
def get_asset_date(days=0, **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    dates = session.query(AssetTrade.date).filter(AssetTrade.is_active).distinct()
    dates = sorted(map(lambda x: x.date, dates))
    if days:
        return dates[-days:]
    return dates


@session_deco
def get_asset_classes_by_type(asset_type=SV.ASSET_CLASS_AGREEMENT, **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    return session.query(AssetClass).filter(AssetClass.is_active, AssetClass.type == asset_type).all()


@session_deco
def get_expiry_management(cal_date=date.today(), **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    return session.query(AssetClass).filter(AssetClass.is_active, AssetClass.type == SV.ASSET_CLASS_MANAGEMENT,
                                            AssetClass.expiry_date == cal_date).all()


@session_deco
def get_start_and_expiry_management(cal_date=date.today(), **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    return session.query(AssetClass).filter(AssetClass.is_active, AssetClass.type == SV.ASSET_CLASS_MANAGEMENT,
                                            or_(AssetClass.expiry_date == cal_date,
                                                AssetClass.start_date == cal_date)).all()


# @session_deco
def get_total_evaluate_detail_by_date(cal_date=date.today()):
    ret = dict()
    cash_amount = get_all_cash(cal_date=cal_date)
    fund_amount = get_all_fund(cal_date=cal_date)
    agreement_amount = get_all_agreement(cal_date=cal_date)
    management_amount = get_all_management(cal_date=cal_date)
    ret_amount = get_all_ret_daily(cal_date=cal_date)

    ret[SV.ASSET_KEY_CAL_DATE] = cal_date
    ret[SV.ASSET_KEY_ALL_EVALUATE_CASH] = cash_amount
    ret[SV.ASSET_KEY_ALL_EVALUATE_AGREEMENT] = agreement_amount
    ret[SV.ASSET_KEY_ALL_EVALUATE_FUND] = fund_amount
    ret[SV.ASSET_KEY_ALL_EVALUATE_MANAGEMENT] = management_amount
    ret[SV.ASSET_KEY_ALL_EVALUATE_RET] = ret_amount
    ret[SV.ASSET_KEY_ALL_VALUE] = cash_amount + fund_amount + management_amount + agreement_amount
    ret[SV.ASSET_KEY_ALL_CURRENT_RATE] = (cash_amount + fund_amount + agreement_amount) / ret.get(
        SV.ASSET_KEY_ALL_VALUE) if ret.get(SV.ASSET_KEY_ALL_VALUE) else 0.0
    ret['fee1'] = ret.get(SV.ASSET_KEY_ALL_VALUE) * 0.02 / 36000
    ret['fee2'] = ret.get(SV.ASSET_KEY_ALL_VALUE) * 0.03 / 36000
    ret['fee3'] = ret.get(SV.ASSET_KEY_ALL_VALUE) * 0.04 / 36500

    ret['fee4'] = ret.get(SV.ASSET_KEY_ALL_EVALUATE_RET) - ret['fee1'] - ret['fee2'] - ret['fee3'] - get_daily_fee(
        cal_date=cal_date)

    return ret


def get_total_evaluate_detail(days=0):
    ret = list()
    for cal_date in get_asset_date(days=days):
        ret.append(get_total_evaluate_detail_by_date(cal_date=cal_date))

    if not ret:
        ret.append(get_total_evaluate_detail_by_date(cal_date=date.today()))
    return ret


def get_today_fees():
    return get_total_evaluate_detail_by_date(cal_date=date.today())


@session_deco
def get_daily_fee_last_total_amount_by_date(cal_date=date.today(), **kwargs):
    session = kwargs.get(SV.SESSION_KEY, None)
    ret = session.query(DailyFee, func.max(DailyFee.time).label('max_time')).filter(
        DailyFee.is_active,
        DailyFee.date == cal_date
    ).one()

    return ret.DailyFee.total_amount if ret.DailyFee else 0.0


def add_fee_with_date(cal_date=date.today(), amount=0.0):
    save(
        DailyFee(
            cal_date=cal_date,
            amount=get_daily_fee_last_total_amount_by_date(cal_date=cal_date) + amount
        )
    )


def get_daily_fee(cal_date=date.today()):
    fees = query(DailyFee).filter(DailyFee.date == cal_date)
    if fees.count() > 0:
        return fees[-1].amount
    else:
        return 0.0


@session_deco
def is_date_has_ret(cal_date=date.today(), ret_type=SV.RET_TYPE_INTEREST, asset_id=None, **kwargs):
    session = kwargs.get(SV.SESSION_KEY)
    ret = session.query(AssetTradeRet).filter(
        AssetTradeRet.is_active,
        AssetTradeRet.asset_class == asset_id,
        AssetTradeRet.date == cal_date,
        AssetTradeRet.type == ret_type
    )
    return bool(ret.count())


@session_deco
def is_date_has_fee(cal_date=date.today(), asset_id=None, fee_type=SV.FEE_TYPE_LOAN_BANK, **kwargs):
    session = kwargs.get(SV.SESSION_KEY)

    ret = session.query(AssetFee).filter(
        AssetFee.is_active,
        AssetFee.asset_class == asset_id,
        AssetFee.date == cal_date,
        AssetFee.type == fee_type
    )
    return bool(ret.count())


if __name__ == '__main__':
    print(get_total_evaluate_detail_by_date())
    # print(is_date_has_ret(cal_date=date(2017, 5, 2), asset_id='3e8a5c5e23104beda418ea4a30df0acd'))
    # print(get_all_cash())
    # get_all_fund()
    # get_today_fees()
    # add_fee_with_date(cal_date=date.today(), amount=10000)
    # print(get_total_evaluate_detail())
