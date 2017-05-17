# encoding:utf8
from __future__ import unicode_literals

from datetime import date, timedelta

from models.AssetClassModel import AssetClass
from models.AssetFeeRateModel import AssetFeeRate
from models.AssetRetRateModel import AssetRetRate
from models.AssetTradeRetModel import AssetTradeRet
from services import CommonService
from services.CommonService import (
    add_asset_ret_with_asset_and_type,
    add_asset_trade_with_asset_and_type,
    add_cash_with_type,
    get_asset_ret_total_amount_by_asset_and_type,
    add_asset_fee_with_asset_and_type,
    query_by_id, save, get_management_trade_amount, get_management_trade_fees,
    get_all_mamangement_ids, get_all_asset_ids_by_type, get_expiry_management, get_management_fees_by_id,
    is_date_has_ret, is_date_has_fee, get_asset_total_amount_by_asset_and_type, get_asset_date_by_id,
    get_asset_ret_last_date_before_cal_date, get_asset_total_amount_by_class_and_type,
    get_asset_ret_total_amount_by_class_and_type, get_asset_fee_total_amount_by_class_and_type)
from services.CommonService import query, purchase, redeem
from utils import StaticValue as SV


################################################################
# Agreement relation method
#
#
#
#
#
################################################################

def add_agreement_class(name=None, rate=0.03, threshold_amount=0, threshold_rate=0):
    '''
    添加协存类别
    :param name:名称
    :param rate:利率
    :param threshold_amount:阶梯额度
    :param threshold_rate:阶梯利率
    :return:
    '''
    agreement = AssetClass(name=name, type=SV.ASSET_CLASS_AGREEMENT, code='1001')
    save(agreement)
    save(
        AssetRetRate(
            asset_id=agreement.id,
            ret_rate=rate,
            threshold=0.0,
            interest_days=360
        )
    )
    save(
        AssetRetRate(
            asset_id=agreement.id,
            ret_rate=threshold_rate,
            threshold=threshold_amount,
            interest_days=360
        )
    ) if threshold_amount and threshold_rate else None


# def asset_ret_carry_to_principal(cal_date=date.today(), asset=AssetClass(), amount=0):
#     if amount > 0:
#         add_asset_ret_with_asset_and_type(
#             amount=amount,
#             asset_id=asset.id,
#             cal_date=cal_date,
#             ret_type=SV.RET_TYPE_PRINCIPAL
#         )
#         add_asset_trade_with_asset_and_type(
#             amount=amount,
#             asset_id=asset.id,
#             cal_date=cal_date,
#             trade_type=SV.ASSET_TYPE_RET_CARRY
#         )
#     else:
#         pass


def add_agreement_daily_data(cal_date=date.today(), asset_id=None, ret_carry_asset_amount=0, purchase_amount=0,
                             redeem_amount=0):
    '''
    添加协存每日记录
    :param cal_date:计算日期
    :param asset_id:协存资产id
    :param ret_carry_asset_amount:收益结转本金
    :param purchase_amount:申购金额
    :param redeem_amount:赎回金额
    :return:None
    '''
    add_daily_asset_data(cal_date=cal_date, asset_id=asset_id, ret_carry_asset_amount=ret_carry_asset_amount,
                         purchase_amount=purchase_amount, redeem_amount=redeem_amount)


def cal_agreement_ret(cal_date=date.today(), asset_id=None):
    init_date = get_asset_ret_last_date_before_cal_date(cal_date, asset_id)
    while init_date <= cal_date:
        cal_agreement_ret_of_asset(cal_date=init_date, asset_id=asset_id)
        init_date += timedelta(days=1)


def cal_agreement_ret_of_asset(cal_date=date.today(), asset_id=None):
    '''
    计算协存的利息
    :param cal_date:计算日期
    :param asset:资产对象
    :return:
    '''

    purchase_amount = get_asset_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset_id,
        trade_type=SV.ASSET_TYPE_PURCHASE
    )

    redeem_amount = get_asset_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset_id,
        trade_type=SV.ASSET_TYPE_REDEEM
    )
    carry_amount = get_asset_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset_id,
        trade_type=SV.ASSET_TYPE_RET_CARRY
    )

    init_asset_amount = get_asset_total_amount_by_asset_and_type(
        cal_date, asset_id, SV.ASSET_TYPE_INIT
    )

    total_amount = purchase_amount + carry_amount - redeem_amount + init_asset_amount
    asset = query_by_id(obj=AssetClass, obj_id=asset_id)
    rates = asset.asset_ret_rate_list
    rate = get_asset_rate_by_amount(rates=rates, amount=total_amount)
    add_asset_ret_with_asset_and_type(
        amount=total_amount * rate.ret_rate / 360,
        asset_id=asset.id,
        ret_type=SV.RET_TYPE_INTEREST,
        cal_date=cal_date
    ) if total_amount else None


def cal_all_agreement_ret(cal_date=date.today()):
    '''
    计算所有协存的利息
    :param cal_date:计算日期
    :return:
    '''
    asset_ids = get_all_asset_ids_by_type(asset_type=SV.ASSET_CLASS_AGREEMENT)
    for asset_id in asset_ids:
        cal_agreement_ret(cal_date=cal_date, asset_id=asset_id[0])


# @timer
def get_asset_agreement_detail(cal_date=date.today(), asset_id=None):
    '''
    获取协存详情
    :param cal_date:计算日期
    :param asset_id:协存资产id
    :return:协存详情字典
    '''
    ret = dict()
    # asset = query(AssetClass).filter(AssetClass.id == asset_id).one()
    # # ret[SV.ASSET_KEY_RATE] = list(map(lambda x: x.ret_rate, asset.asset_ret_rate_list))[
    # #     0] if len(asset.asset_ret_rate_list) > 0 else 0.0
    asset = query_by_id(obj=AssetClass, obj_id=asset_id)
    ret.update(get_asset_base_detail(cal_date=cal_date, asset=asset))

    total_carry = get_asset_ret_total_amount_by_asset_and_type(
        asset_id=asset_id,
        cal_date=cal_date,
        ret_type=SV.RET_TYPE_PRINCIPAL
    )
    yes_total_carry = get_asset_ret_total_amount_by_asset_and_type(
        asset_id=asset_id,
        cal_date=cal_date - timedelta(days=1),
        ret_type=SV.RET_TYPE_PRINCIPAL
    )

    ret[SV.ASSET_KEY_RET_CARRY_PRINCIPAL] = total_carry - yes_total_carry

    total_ret = get_asset_ret_total_amount_by_asset_and_type(
        asset_id=asset.id,
        cal_date=cal_date,
        ret_type=SV.RET_TYPE_INTEREST
    )

    yes_total_ret = get_asset_ret_total_amount_by_asset_and_type(
        asset_id=asset.id,
        cal_date=cal_date - timedelta(days=1),
        ret_type=SV.RET_TYPE_INTEREST
    )
    init_trade_amount = get_asset_total_amount_by_asset_and_type(cal_date, asset_id, SV.ASSET_TYPE_INIT)
    init_ret_amount = get_asset_ret_total_amount_by_asset_and_type(cal_date, asset_id, SV.RET_TYPE_INIT)
    total_ret += init_ret_amount
    yes_total_ret += init_ret_amount

    ret.update({SV.ASSET_KEY_ASSET_RET: total_ret - yes_total_ret - ret.get(SV.ASSET_KEY_RET_CARRY_PRINCIPAL, 0)})
    ret.update({
        SV.ASSET_KEY_ASSET_TOTAL: ret.get(SV.ASSET_KEY_PURCHASE_AGREEMENT + '_total', 0) + total_ret - ret.get(
            SV.ASSET_KEY_REDEEM_AGREEMENT + '_total', 0) + init_trade_amount})
    ret.update({
        SV.ASSET_KEY_PRINCIPAL: ret.get(SV.ASSET_KEY_PURCHASE_AGREEMENT + '_total', 0) + total_carry - ret.get(
            SV.ASSET_KEY_REDEEM_AGREEMENT + '_total') + init_trade_amount})
    rates = query_by_id(obj=AssetClass, obj_id=asset_id).asset_ret_rate_list
    ret_rate = get_asset_rate_by_amount(rates=rates, amount=ret.get(SV.ASSET_KEY_PRINCIPAL))
    ret.update({SV.ASSET_KEY_RATE: ret_rate.ret_rate})
    return ret


# @timer
def get_single_agreement_detail_by_days(days=0, asset_id=None):
    asset_dates = get_asset_date_by_id(days=days, asset_id=asset_id)  # get_asset_date(days=days, asset_id=asset_id)
    if not asset_dates:
        asset_dates = [date.today()]
    return list(map(lambda x: get_asset_agreement_detail(cal_date=x, asset_id=asset_id),
                    asset_dates))


def get_single_agreement_detail_by_period(asset_id=None, start=date.today(), end=date.today()):
    ret = list()
    while start <= end:
        ret.append(get_asset_agreement_detail(cal_date=start, asset_id=asset_id))
        start += timedelta(days=1)
    return [{asset_id: ret}]


# @timer
def get_agreement_detail_by_days(days=0):
    '''
    获取协存明细
    :param days:
    :return:
    '''
    # agreement_ids = list(
    #     map(lambda x: x.id, query(AssetClass).filter(AssetClass.type == SV.ASSET_CLASS_AGREEMENT)))
    ret = list()

    agreement_ids = get_all_asset_ids_by_type(asset_type=SV.ASSET_CLASS_AGREEMENT)

    for agreement_id in agreement_ids:
        agreement_ret = get_single_agreement_detail_by_days(days=days, asset_id=agreement_id[0])
        ret.append({agreement_id[0]: agreement_ret})

    return ret


################################################################
#
#
# Fund relation method
#
#
#
################################################################


def add_fund_class(name='XX FUND', code=None):
    '''
    添加货基类别
    :param name:
    :param code:
    :return:
    '''
    save(AssetClass(name=name, code=code, type=SV.ASSET_CLASS_FUND))


def asset_ret_carry_to_principal(cal_date=date.today(), asset=AssetClass(), amount=0):
    '''
    结转货基收益到现金
    :param cal_date:
    :param asset:
    :param amount:
    :return:
    '''
    if amount > 0:

        add_asset_ret_with_asset_and_type(
            amount=amount,
            asset_id=asset.id,
            cal_date=cal_date,
            ret_type=SV.RET_TYPE_PRINCIPAL
        )
        add_asset_trade_with_asset_and_type(amount, SV.ASSET_TYPE_RET_CARRY, asset.id, cal_date)
    else:
        pass


def asset_ret_carry_to_cash(cal_date=date.today(), asset=AssetClass(), amount=0):
    if amount > 0:

        add_asset_ret_with_asset_and_type(
            amount=amount,
            asset_id=asset.id,
            cal_date=cal_date,
            ret_type=SV.RET_TYPE_CASH
        )
        add_cash_with_type(amount=amount, cash_type=SV.CASH_TYPE_CARRY, asset_id=asset.id, cal_date=cal_date)

        # add_asset_ret_with_asset_and_type(amount, asset.id, SV.ASSET_TYPE_RET_CARRY, cal_date)
    else:
        pass


def add_fund_daily_data(cal_date=date.today(), asset_id=None, ret_carry_amount=0, purchase_amount=0, redeem_amount=0,
                        ret_amount=0):
    '''
    添加货基每日记录
    :param cal_date:
    :param asset_id:计算日期
    :param ret_carry_cash_amount:收益结转现金
    :param purchase_amount:申购金额
    :param redeem_amount:赎回金额
    :param ret_amount:收益
    :return:None
    '''

    ret_init = get_asset_ret_total_amount_by_asset_and_type(
        cal_date,
        asset_id,
        SV.RET_TYPE_INIT
    )

    fund_total_ret_amount = get_asset_ret_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset_id,
        ret_type=SV.RET_TYPE_INTEREST
    )  # 所有基金收益
    fund_total_ret_amount += ret_init

    fund_carry_ret_amount = get_asset_ret_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset_id,
        ret_type=SV.RET_TYPE_PRINCIPAL
    )  # 结转基金收益
    ret_amount -= (fund_total_ret_amount - fund_carry_ret_amount)  # 输入未结转收益-当日未结转收益 = 当日收益
    add_daily_asset_data(
        cal_date=cal_date, asset_id=asset_id,
        purchase_amount=purchase_amount,
        redeem_amount=redeem_amount, ret_amount=ret_amount,
        ret_carry_asset_amount=ret_carry_amount
    )


def get_total_fund_statistic_by_id(cal_date=date.today(), asset_id=None):
    total_purchase_amount = get_asset_total_amount_by_asset_and_type(cal_date=cal_date, asset_id=asset_id,
                                                                     trade_type=SV.ASSET_TYPE_PURCHASE)
    total_redeem_amount = get_asset_total_amount_by_asset_and_type(cal_date=cal_date, asset_id=asset_id,
                                                                   trade_type=SV.ASSET_TYPE_REDEEM)

    total_ret_amount = get_asset_ret_total_amount_by_asset_and_type(cal_date=cal_date, asset_id=asset_id,
                                                                    ret_type=SV.RET_TYPE_INTEREST)
    init_ret_amount = get_asset_ret_total_amount_by_asset_and_type(
        cal_date,
        asset_id,
        SV.RET_TYPE_INIT
    )
    total_ret_amount += init_ret_amount
    init_amount = get_asset_total_amount_by_asset_and_type(
        cal_date,
        asset_id,
        SV.ASSET_TYPE_INIT
    )
    total_amount = total_purchase_amount - total_redeem_amount + total_ret_amount
    total_amount += init_amount
    return {
        SV.ASSET_KEY_FUND_TOTAL_AMOUNT: total_amount,
        SV.ASSET_KEY_FUND_TOTAL_PURCHASE_AMOUNT: total_purchase_amount,
        SV.ASSET_KEY_FUND_TOTAL_REDEEM_AMOUNT: total_redeem_amount,
        SV.ASSET_KEY_FUND_TOTAL_RET_AMOUNT: total_ret_amount
    }


def get_total_fund_statistic(cal_date=date.today()):
    '''
    获取货金的统计量
    :param cal_date:计算日期
    :return:
    '''
    assets = get_all_asset_ids_by_type(asset_type=SV.ASSET_CLASS_FUND)
    ret = list()
    for asset in assets:
        fund_ret = get_total_fund_statistic_by_id(cal_date=cal_date, asset_id=asset[0])
        fund_ret.update({SV.ASSET_KEY_NAME: asset[1]})
        ret.append(fund_ret)
    return ret


def get_asset_fund_detail(cal_date=date.today(), asset_id=None):
    '''
    获取货基详情
    :param cal_date:计算日期
    :param asset_id:货基资产id
    :return:货基详情字典
    '''
    ret = dict()
    asset = query_by_id(AssetClass, asset_id)
    ret.update(get_asset_base_detail(cal_date=cal_date, asset=asset))

    total_ret = get_asset_ret_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset_id,
        ret_type=SV.RET_TYPE_INTEREST)  # 总收益
    yes_total_ret = get_asset_ret_total_amount_by_asset_and_type(
        cal_date=cal_date - timedelta(days=1),
        asset_id=asset_id,
        ret_type=SV.RET_TYPE_INTEREST)  # 昨日之前总收益

    init_ret_amount = get_asset_ret_total_amount_by_asset_and_type(cal_date, asset_id, SV.RET_TYPE_INIT)

    ret.update({SV.ASSET_KEY_ASSET_RET: total_ret - yes_total_ret})

    total_ret_carry = get_asset_ret_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset_id,
        ret_type=SV.RET_TYPE_PRINCIPAL)
    yes_total_ret_carry = get_asset_ret_total_amount_by_asset_and_type(
        cal_date=cal_date - timedelta(days=1),
        asset_id=asset_id,
        ret_type=SV.RET_TYPE_PRINCIPAL)

    ret.update({SV.ASSET_KEY_RET_CARRY_CASH: total_ret_carry - yes_total_ret_carry})
    ret.update({SV.ASSET_KEY_RET_NOT_CARRY: total_ret - yes_total_ret_carry + init_ret_amount})  # 未结转收益
    total_purchase = get_asset_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset_id,
        trade_type=SV.ASSET_TYPE_PURCHASE
    )
    total_redeem = get_asset_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset_id,
        trade_type=SV.ASSET_TYPE_REDEEM
    )
    init_asset_amount = get_asset_total_amount_by_asset_and_type(cal_date, asset_id, SV.ASSET_TYPE_INIT)

    ret.update(
        {SV.ASSET_KEY_ASSET_TOTAL: total_purchase - total_redeem + total_ret + init_asset_amount + init_ret_amount})

    return ret


def get_single_fund_detail_by_period(asset_id=None, start=date.today(), end=date.today()):
    ret = list()
    while start <= end:
        ret.append(get_asset_fund_detail(cal_date=start, asset_id=asset_id))
        start += timedelta(days=1)
    return [{asset_id: ret}]


def get_single_fund_detail_by_days(days=0, asset_id=None):
    asset_dates = get_asset_date_by_id(days=days, asset_id=asset_id)
    if not asset_dates:
        asset_dates = [date.today()]
    return list(
        map(
            lambda x: get_asset_fund_detail(cal_date=x, asset_id=asset_id), asset_dates
        )
    )


def get_fund_detail_by_days(days=0):
    '''
    计算货基的明细
    :param days:计算日期
    :return:
    '''

    ret = list()
    fund_ids = get_all_asset_ids_by_type(asset_type=SV.ASSET_CLASS_FUND)
    for fund_id in fund_ids:
        fund_ret = get_single_fund_detail_by_days(days=days, asset_id=fund_id[0])
        ret.append({fund_id[0]: fund_ret})
    return ret
    # return dict(map(lambda x: (x, get_single_fund_detail_by_days(days=days, asset_id=x)), fund_ids))


################################################################
#
#
#
# Management relation detail
#
#
################################################################

def add_management_class(
        name=None,
        trade_amount=1000000,
        ret_rate=0.1,
        rate_days=360,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=360),
        bank_fee_rate=0.0003,
        bank_days=360,
        manage_fee_rate=0.0012,
        manage_days=360,
        cal_date=date.today()
):
    asset = AssetClass(name=name, start_date=start_date, expiry_date=end_date, type=SV.ASSET_CLASS_MANAGEMENT,
                       ret_cal_method=SV.RET_TYPE_CASH_ONE_TIME, cal_date=start_date)
    asset_id = asset.id
    save(asset)
    asset_rate = AssetRetRate(asset_id=asset_id, ret_rate=ret_rate, interest_days=rate_days, cal_date=cal_date)

    asset_fee_rate_bank = AssetFeeRate(asset_class=asset_id, rate=bank_fee_rate, type=SV.FEE_TYPE_LOAN_BANK,
                                       fee_days=bank_days, cal_date=cal_date)
    asset_fee_rate_manage = AssetFeeRate(asset_class=asset_id, rate=manage_fee_rate, type=SV.FEE_TYPE_MANAG_PLAN,
                                         fee_days=manage_days, cal_date=cal_date)
    purchase(asset=asset, amount=trade_amount, cal_date=start_date)

    save(asset_rate)
    save(asset_fee_rate_bank)
    save(asset_fee_rate_manage)

    cal_all_management_ret_and_fee(cal_date=date.today())

    draw_management_ret_by_asset(asset_id=asset_id, ret_method=asset.ret_cal_method)
    draw_management_by_asset(asset_id=asset_id)


def cal_management_ret(cal_date=None, asset_id=None):
    '''
    计算资管的利息
    :param cal_date:计算日期
    :param asset_id:资管资产id
    :return:
    '''

    asset = query_by_id(AssetClass, asset_id)
    if asset.expiry_date > cal_date and asset.start_date <= cal_date and not is_date_has_ret(asset_id=asset_id,
                                                                                             ret_type=SV.RET_TYPE_INTEREST,
                                                                                             cal_date=cal_date):
        rate = get_asset_rate_by_amount(rates=asset.asset_ret_rate_list, amount=0)
        days = rate.interest_days
        asset_trades = asset.asset_trade_list
        amount = asset_trades[-1].total_amount if asset_trades else 0.0
        ret = amount * rate.ret_rate / days
        add_asset_ret_with_asset_and_type(
            asset_id=asset_id,
            amount=ret,
            ret_type=SV.RET_TYPE_INTEREST,
            cal_date=cal_date
        )


def cal_management_ret_and_fee_to_cal_date(cal_date=date.today(), asset_id=''):
    init_date = get_asset_ret_last_date_before_cal_date(cal_date, asset_id)
    while init_date <= cal_date:
        cal_management_ret(init_date, asset_id)
        cal_management_fee(init_date, asset_id)

        init_date += timedelta(days=1)


def cal_all_management_ret_and_fee(cal_date=date.today()):
    '''
    计算资管系统的收益
    :param cal_date:计算时间
    :return:
    '''
    management_ids = get_all_asset_ids_by_type(asset_type=SV.ASSET_CLASS_MANAGEMENT)
    for management_id in management_ids:
        cal_management_ret_and_fee_to_cal_date(cal_date, management_id[0])


def cal_management_fee(cal_date=date.today(), asset_id=None):
    asset = query_by_id(AssetClass, asset_id)
    if asset.expiry_date > cal_date and asset.start_date <= cal_date:
        asset_fee_rates = asset.asset_fee_rate_list

        asset_trades = asset.asset_trade_list
        total_trade_amount = asset_trades[-1].total_amount if asset_trades else 0.0
        for asset_fee_rate in asset_fee_rates:
            add_asset_fee_with_asset_and_type(
                cal_date=cal_date,
                amount=total_trade_amount * asset_fee_rate.rate / asset_fee_rate.fee_days,
                asset_id=asset_id,
                fee_type=asset_fee_rate.type
            ) if not is_date_has_fee(cal_date=cal_date, asset_id=asset_id, fee_type=asset_fee_rate.type) else None
    else:
        pass


def cal_all_manangement_fee(cal_date=date.today()):
    '''
    计算所有的资管费用
    :param cal_date:计算时间
    :return:
    '''
    management_ids = get_all_asset_ids_by_type(asset_type=SV.ASSET_CLASS_MANAGEMENT)
    for management_id in management_ids:
        cal_management_fee(cal_date=cal_date, asset_id=management_id[0])


def get_total_management_statistic_by_id(cal_date=date.today(), asset_id=None):
    total_purchase_amount = get_asset_total_amount_by_asset_and_type(cal_date=cal_date, asset_id=asset_id,
                                                                     trade_type=SV.ASSET_TYPE_PURCHASE)
    total_redeem_amount = get_asset_total_amount_by_asset_and_type(cal_date=cal_date, asset_id=asset_id,
                                                                   trade_type=SV.ASSET_TYPE_REDEEM)
    total_amount = total_purchase_amount - total_redeem_amount

    total_ret_amount = get_asset_ret_total_amount_by_asset_and_type(cal_date=cal_date, asset_id=asset_id,
                                                                    ret_type=SV.RET_TYPE_INTEREST)
    total_carry_ret_amount = get_asset_ret_total_amount_by_asset_and_type(cal_date, asset_id, SV.RET_TYPE_CASH)
    total_ret_amount -= total_carry_ret_amount
    return {
        SV.ASSET_KEY_ASSET_ID: asset_id,
        SV.ASSET_KEY_NAME: query_by_id(AssetClass, asset_id).name,
        SV.ASSET_KEY_MANAGEMENT_AMOUNT: total_amount + total_ret_amount,
        SV.ASSET_KEY_PURCHASE_MANAGEMENT: total_purchase_amount - total_redeem_amount,
        SV.ASSET_KEY_MANAGEMENT_RET: total_ret_amount,
        SV.CASH_KEY_CAL_DATE: cal_date,
    }


def get_total_management_statistic_by_date(cal_date=date.today()):
    total_purchase_amount = get_asset_total_amount_by_class_and_type(cal_date, SV.ASSET_CLASS_MANAGEMENT,
                                                                     SV.ASSET_TYPE_PURCHASE)
    total_redeem_amount = get_asset_total_amount_by_class_and_type(cal_date, SV.ASSET_CLASS_MANAGEMENT,
                                                                   SV.ASSET_TYPE_REDEEM)
    total_ret_amount = get_asset_ret_total_amount_by_class_and_type(cal_date, SV.ASSET_CLASS_MANAGEMENT,
                                                                    SV.RET_TYPE_INTEREST)
    total_ret_carry = get_asset_ret_total_amount_by_class_and_type(cal_date, SV.ASSET_CLASS_MANAGEMENT,
                                                                   SV.RET_TYPE_CASH)
    total_fee_amount = get_asset_fee_total_amount_by_class_and_type(cal_date, SV.ASSET_CLASS_MANAGEMENT,
                                                                    SV.FEE_TYPE_ADJUST_BANK) \
                       + get_asset_fee_total_amount_by_class_and_type(cal_date, SV.ASSET_CLASS_MANAGEMENT,
                                                                      SV.FEE_TYPE_ADJUST_CHECK) \
                       + get_asset_fee_total_amount_by_class_and_type(cal_date, SV.ASSET_CLASS_MANAGEMENT,
                                                                      SV.FEE_TYPE_LOAN_BANK) \
                       + get_asset_fee_total_amount_by_class_and_type(cal_date, SV.ASSET_CLASS_MANAGEMENT,
                                                                      SV.FEE_TYPE_MANAG_PLAN) \
                       + get_asset_fee_total_amount_by_class_and_type(cal_date, SV.ASSET_CLASS_MANAGEMENT,
                                                                      SV.FEE_TYPE_INIT)
    # total_carry_fee_amount = get_asset_fee_total_amount_by_class_and_type(cal_date,SV.ASSET_CLASS_MANAGEMENT,SV.feetype)

    total_amount = total_purchase_amount - total_redeem_amount + total_ret_amount - total_ret_carry - total_fee_amount

    return {
        SV.ASSET_KEY_CAL_DATE: cal_date,
        SV.ASSET_KEY_MANAGEMENT_AMOUNT: total_amount,
        SV.ASSET_KEY_PURCHASE_MANAGEMENT: total_purchase_amount - total_redeem_amount,
        SV.ASSET_KEY_MANAGEMENT_RET: total_ret_amount - total_ret_carry
    }


def get_total_management_statistic_period(start_date=date.today(), end_date=date.today()):
    ret = list()
    while start_date <= end_date:
        ret.append(get_total_management_statistic_by_date(start_date))
        start_date += timedelta(days=1)
    return ret


def get_total_management_statistic_by_days(days=0):
    dates = CommonService.get_asset_date(days)
    ret = list()
    for cal_date in dates:
        ret.append(get_total_management_statistic_by_date(cal_date))
    return ret


def get_total_management_statistic(cal_date=date.today()):
    '''
    计算日期的统计数据
    :param cal_date:计算日期
    :return:
    '''
    assets = get_all_asset_ids_by_type(asset_type=SV.ASSET_CLASS_MANAGEMENT)
    ret = list()
    for asset in assets:
        management_ret = get_total_management_statistic_by_id(cal_date=cal_date, asset_id=asset[0])
        management_ret.update({SV.ASSET_KEY_NAME: asset[1]})
        ret.append(management_ret)

    return ret


def get_management_asset_all_ret(asset_id=None):
    asset_rate_list = query_by_id(obj=AssetClass, obj_id=asset_id).asset_ret_rate_list
    asset_rate = get_asset_rate_by_amount(asset_rate_list)
    asset_trade_list = query_by_id(obj=AssetClass, obj_id=asset_id).asset_trade_list
    asset_trade_amount = asset_trade_list[-1].total_amount
    asset = query_by_id(obj=AssetClass, obj_id=asset_id)
    return asset_trade_amount * asset_rate.ret_rate * (
        asset.expiry_date - asset.start_date).days / asset_rate.interest_days if asset_rate.interest_days else 0.0


def get_single_management_detail(asset_id=None):
    asset = query_by_id(obj=AssetClass, obj_id=asset_id)
    ret = dict()
    ret.update({SV.ASSET_KEY_NAME: asset.name})
    ret.update({SV.ASSET_KEY_ASSET_ID: asset.id})
    ret.update({SV.ASSET_KEY_START_DATE: asset.start_date})
    ret.update({SV.ASSET_KEY_EXPIRY_DATE: asset.expiry_date})
    ret.update({SV.ASSET_KEY_MANAGEMENT_DUE: (
        asset.expiry_date - asset.start_date).days}) if asset.expiry_date and asset.start_date and asset.expiry_date > asset.start_date else ret.update(
        {SV.ASSET_KEY_MANAGEMENT_DUE: 1})
    ret.update({SV.ASSET_KEY_ASSET_RET: get_management_asset_all_ret(asset_id=asset.id)})
    ret.update({SV.ASSET_KEY_MANAGEMENT_AMOUNT: get_management_trade_amount(asset_id=asset_id)})
    asset = query_by_id(obj=AssetClass, obj_id=asset_id)
    ret.update({SV.ASSET_KEY_MANAGEMENT_RET_RATE: asset.asset_ret_rate_list[
        0].ret_rate}) if len(asset.asset_ret_rate_list) else ret.update({SV.ASSET_KEY_MANAGEMENT_RET_RATE: 0.0})

    fees = get_management_trade_fees(asset_id=asset_id)
    if fees:
        ret.update({SV.ASSET_KEY_MANAGEMENT_BANK_FEE: ret.get(SV.ASSET_KEY_MANAGEMENT_AMOUNT) * fees[0].rate * ret.get(
            SV.ASSET_KEY_MANAGEMENT_DUE) / fees[0].fee_days}) if ret.get(SV.ASSET_KEY_MANAGEMENT_DUE) and fees[
            0].fee_days else ret.update(
            {SV.ASSET_KEY_MANAGEMENT_BANK_FEE: 0})
        ret.update(
            {SV.ASSET_KEY_MANAGEMENT_MANAGE_FEE: ret.get(SV.ASSET_KEY_MANAGEMENT_AMOUNT) * fees[1].rate * ret.get(
                SV.ASSET_KEY_MANAGEMENT_DUE) / fees[1].fee_days}) if ret.get(
            SV.ASSET_KEY_MANAGEMENT_DUE) and fees[1].fee_days else ret.update(
            {SV.ASSET_KEY_MANAGEMENT_MANAGE_FEE: 0})

    else:
        ret.update({SV.ASSET_KEY_MANAGEMENT_BANK_FEE: 0, SV.ASSET_KEY_MANAGEMENT_MANAGE_FEE: 0})
    ret.update({SV.ASSET_KEY_MANAGEMENT_DAILY_RET: (ret.get(SV.ASSET_KEY_ASSET_RET) - ret.get(
        SV.ASSET_KEY_MANAGEMENT_BANK_FEE) - ret.get(
        SV.ASSET_KEY_MANAGEMENT_MANAGE_FEE)) / ret.get(
        SV.ASSET_KEY_MANAGEMENT_DUE)}) if ret.get(SV.ASSET_KEY_MANAGEMENT_DUE) else ret.update(
        {SV.ASSET_KEY_MANAGEMENT_DAILY_RET: 0.0})
    return ret


def get_all_management_detail():
    ret = list()
    ids = get_all_mamangement_ids()
    for id in ids:
        ret.append(get_single_management_detail(asset_id=id))
    return ret


def cal_adjust_fee(cal_date=date.today(), fee_amount=200, asset_id=None, adjust_fee_type=SV.FEE_TYPE_ADJUST_BANK):
    '''
    添加调整费用
    :param cal_date:计算日期
    :param fee_amount:调整费用
    :param asset_id:资产id
    :return:
    '''
    add_asset_fee_with_asset_and_type(cal_date=cal_date, asset_id=asset_id, fee_type=adjust_fee_type,
                                      amount=fee_amount)


# def management_carry_ret_to_cash(cal_date=date.today(), asset_id=None):
#     asset = query_by_id(obj=AssetClass, obj_id=asset_id)
#     if asset.ret_cal_method == SV.RET_TYPE_CASH_CUT_INTEREST:
#         if asset.start_date == cal_date:
#             add_asset_ret_with_asset_and_type(
#                 cal_date=cal_date,
#                 amount=get_management_asset_all_ret(asset_id=asset_id, cal_date=cal_date),
#                 asset_id=asset_id,
#                 ret_type=SV.RET_TYPE_CASH_CUT_INTEREST
#             )
#     elif asset.ret_cal_method == SV.RET_TYPE_CASH_ONE_TIME:
#         if asset.expiry_date == cal_date:
#             add_asset_ret_with_asset_and_type(
#                 cal_date=cal_date,
#                 amount=get_management_asset_all_ret(asset_id=asset_id, cal_date=cal_date),
#                 ret_type=SV.RET_TYPE_CASH_ONE_TIME
#             )
#

# def cal_daily_ret_and_fee(cal_date=date.today(), asset_id=None):
#     '''
#     计算资管的收益和费用
#     :param cal_date:计算日期
#     :param asset_id:资产id
#     :return:
#     '''
#     assetclass = query_by_id(obj=AssetClass(), obj_id=asset_id)
#     if cal_date < assetclass.expiry_date:
#         asset_ret_rates = assetclass.asset_ret_rate_list
#         asset_fee_rates = assetclass.asset_fee_rate_list
#         asset_trade_amount = get_asset_last_total_amount_by_asset_and_type(asset_id=assetclass.id,
#                                                                            trade_type=SV.ASSET_TYPE_PURCHASE,
#                                                                            cal_date=cal_date)
#
#         rate = asset_ret_rates[0]
#         add_asset_ret_with_asset_and_type(amount=asset_trade_amount * rate.ret_rate / rate.interest_days,
#                                           asset_id=asset_id, ret_type=SV.RET_TYPE_INTEREST, cal_date=cal_date)
#
#         for x in asset_fee_rates:
#             add_asset_fee_with_asset_and_type(
#                 amount=asset_trade_amount * x.rate / x.fee_days,
#                 asset_id=asset_id, fee_type=SV.FEE_TYPE_PURCHASE,
#                 cal_date=cal_date)


def cal_all_mangement_ret_and_fee(cal_date=date.today()):
    '''
    计算所有的资管资产的收益和费用
    :param cal_date:
    :return:
    '''
    management_ids = get_all_asset_ids_by_type(asset_type=SV.ASSET_CLASS_MANAGEMENT)
    for management_id in management_ids:
        cal_management_ret(cal_date=cal_date, asset_id=management_id[0])
        cal_management_fee(cal_date=cal_date, asset_id=management_id[0])


def draw_management_by_asset(asset_id=None):
    asset = query_by_id(obj=AssetClass, obj_id=asset_id)
    amount = asset.asset_trade_list[0].amount if asset.asset_trade_list else 0.0
    redeem(asset=asset, amount=amount, cal_date=asset.expiry_date)


def draw_management_ret_by_asset(asset_id=None, ret_method=SV.RET_TYPE_CASH_CUT_INTEREST):
    asset = query_by_id(obj=AssetClass, obj_id=asset_id)
    total_ret = get_all_management_ret(asset=asset)
    if ret_method == SV.RET_TYPE_CASH_CUT_INTEREST:
        asset_ret_carry_to_cash(cal_date=asset.start_date, asset=asset, amount=total_ret)
    else:
        asset_ret_carry_to_cash(cal_date=asset.expiry_date, asset=asset, amount=total_ret)

    add_cash_with_type(cal_date=asset.expiry_date, cash_type=SV.CASH_TYPE_CARRY, amount=-get_all_mangement_fee(asset))
    add_asset_fee_with_asset_and_type(cal_date=asset.expiry_date, asset_id=asset.id, fee_type=SV.FEE_TYPE_ADJUST_BANK,
                                      amount=-get_all_mangement_fee(asset))


def carry_management_fee_by_asset(asset_id=None):
    asset = query_by_id(obj=AssetClass, asset_id=asset_id)
    total_fee_amount = get_all_mangement_fee(asset=asset)
    add_cash_with_type(amount=total_fee_amount, cal_date=asset.expiry_date, cash_type=SV.CASH_TYPE_FEE)
    add_asset_fee_with_asset_and_type(amount=total_fee_amount, cal_date=asset.expiry_date, fee_type=SV.FEE_TYPE_REDEEM)


def draw_mangement(cal_date=date.today()):
    mangements = get_expiry_management(cal_date=cal_date)
    for mangement in mangements:
        amount = mangement.asset_trade_list[0].amount
        redeem(amount=amount, cal_date=cal_date, asset=mangement)


def get_all_management_ret(asset=AssetClass()):
    days = (asset.expiry_date - asset.start_date).days
    asset_rate = asset.asset_ret_rate_list[0]
    year_days = asset_rate.interest_days
    rate = asset_rate.ret_rate if asset_rate else 0.0
    amount = asset.asset_trade_list[0].amount if asset.asset_trade_list else 0.0
    return amount * days * rate / year_days


def get_all_mangement_fee(asset=AssetClass()):
    total_fee_amount = 0
    days = (asset.expiry_date - asset.start_date).days
    amount = asset.asset_trade_list[0].amount if asset.asset_trade_list else 0.0
    asset_fee_rates = query_by_id(AssetClass, asset.id).asset_fee_rate_list  # asset.asset_fee_rate_list
    for asset_fee_rate in asset_fee_rates:
        total_fee_amount += amount * days * asset_fee_rate.rate / asset_fee_rate.fee_days if asset_fee_rate.fee_days else 0.0
    return total_fee_amount


# def draw_manangent_ret(cal_date=date.today()):
#     managements = get_start_and_expiry_management(cal_date=cal_date)
#     for management in managements:
#         if management.ret_cal_method == SV.RET_TYPE_CASH_CUT_INTEREST and management.start_date == cal_date:
#             add_cash_with_type(amount=get_all_management_ret(asset=management), cash_type=SV.CASH_TYPE_CARRY,
#                                asset_id=management.id, cal_date=cal_date)
#             add_asset_ret_with_asset_and_type(amount=get_all_management_ret(asset=management), asset_id=management.id,
#                                               ret_type=SV.RET_TYPE_CASH_CUT_INTEREST, cal_date=cal_date)
#         elif management.ret_cal_method == SV.RET_TYPE_CASH_ONE_TIME and management.expiry_date == cal_date:
#             add_cash_with_type(amount=get_all_management_ret(asset=management), cash_type=SV.CASH_TYPE_CARRY,
#                                asset_id=management.id, cal_date=cal_date)
#             add_asset_ret_with_asset_and_type(amount=get_all_management_ret(asset=management), asset_id=management.id,
#                                               ret_type=SV.RET_TYPE_CASH_ONE_TIME, cal_date=cal_date)


def get_management_fee_by_id(cal_date=date.today(), asset_id=None):
    asset_fees = get_management_fees_by_id(cal_date=cal_date, asset_id=asset_id)

    ret = list()
    for asset_fee in asset_fees:
        ret.append({SV.ASSET_KEY_CAL_DATE: asset_fee.date, SV.ASSET_KEY_FEE_AMOUNT: asset_fee.amount,
                    SV.ASSET_KEY_FEE_TYPE: asset_fee.type, SV.ASSET_KEY_ASSET_ID: asset_fee.asset_class})

    return ret


################################################################
#
#
#
# Common Method
#
#
################################################################

def get_asset_rate_by_amount(rates=AssetClass().asset_ret_rate_list, amount=10000):
    rate = AssetRetRate(ret_rate=0.0)
    if len(rates) >= 1:
        rate = list(filter(lambda x: x.threshold <= amount, rates))[-1]
    return rate


def add_trade_ret(cal_date=date.today(), ret_amount=0, asset=AssetClass()):
    add_asset_ret_with_asset_and_type(
        amount=ret_amount,
        asset_id=asset.id,
        ret_type=SV.RET_TYPE_INTEREST,
        cal_date=cal_date
    )


def add_daily_asset_data(cal_date=date.today(), asset_id=None, ret_carry_asset_amount=0,
                         purchase_amount=0,
                         redeem_amount=0, ret_amount=0):
    asset = query(AssetClass).filter(AssetClass.id == asset_id).one()
    asset_ret_carry_to_principal(cal_date=cal_date, asset=asset,
                                 amount=ret_carry_asset_amount) if ret_carry_asset_amount else None
    purchase(asset=asset, amount=purchase_amount, cal_date=cal_date) if purchase_amount else None
    redeem(asset=asset, amount=redeem_amount, cal_date=cal_date) if redeem_amount else None
    add_trade_ret(cal_date=cal_date, ret_amount=ret_amount, asset=asset) if ret_amount else None
    # asset_ret_carry_to_cash(cal_date=cal_date, asset=asset,
    #                         amount=ret_carry_cash_amount) if ret_carry_cash_amount else None
    asset = query(AssetClass).filter(AssetClass.id == asset_id).one()
    cal_agreement_ret(cal_date=cal_date, asset_id=asset.id) if asset.type == SV.ASSET_CLASS_AGREEMENT else None


# @timer
def get_key_by_asset_type_and_asset_class(asset_type=SV.CASH_TYPE_DEPOSIT, asset_class=SV.ASSET_CLASS_MANAGEMENT):
    key_dic = {
        SV.ASSET_TYPE_PURCHASE: {
            SV.ASSET_CLASS_AGREEMENT: SV.CASH_KEY_PURCHASE_AGREEMENT,
            SV.ASSET_CLASS_FUND: SV.CASH_KEY_PURCHASE_FUND,
            SV.ASSET_CLASS_MANAGEMENT: SV.CASH_KEY_PURCHASE_MANAGEMENT

        },
        SV.ASSET_TYPE_REDEEM: {
            SV.ASSET_CLASS_AGREEMENT: SV.CASH_KEY_REDEEM_AGREEMENT,
            SV.ASSET_CLASS_FUND: SV.CASH_KEY_REDEEM_FUND,
            SV.ASSET_CLASS_MANAGEMENT: SV.CASH_KEY_REDEEM_MANAGEMENT
        }
    }
    return key_dic[asset_type][asset_class]


def get_asset_trades_sum_dic_by_type(cal_date=date.today(), asset=AssetClass(), trade_type=SV.ASSET_TYPE_PURCHASE):
    total_amount = get_asset_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset.id,
        trade_type=trade_type
    )

    yes_total_amount = get_asset_total_amount_by_asset_and_type(
        cal_date=cal_date - timedelta(days=1),
        asset_id=asset.id,
        trade_type=trade_type
    )

    return {
        get_key_by_asset_type_and_asset_class(
            asset_type=trade_type,
            asset_class=asset.type
        ): total_amount - yes_total_amount,
        get_key_by_asset_type_and_asset_class(
            asset_type=trade_type,
            asset_class=asset.type
        ) + '_total': total_amount

    }


def get_asset_base_detail(cal_date=date.today(), asset=AssetClass()):
    ret = dict()
    ret.update({SV.ASSET_KEY_NAME: asset.name, SV.ASSET_KEY_CAL_DATE: cal_date})
    ret.update(get_asset_trades_sum_dic_by_type(cal_date=cal_date, asset=asset, trade_type=SV.ASSET_TYPE_PURCHASE))
    ret.update(get_asset_trades_sum_dic_by_type(cal_date=cal_date, asset=asset, trade_type=SV.ASSET_TYPE_REDEEM))
    return ret


# @timer
def get_asset_date(days=0, asset_id=None):
    asset_dates = sorted(set(map(lambda x: x.date, query(AssetTradeRet).filter(AssetTradeRet.asset_class == asset_id,
                                                                               AssetTradeRet.date <= date.today()))))
    if days:
        return asset_dates[-days:]
    return asset_dates


if __name__ == '__main__':
    '''
    agreement:{'rate': 0.035, 'asset_name': '浦发理财一号', 'cal_date': datetime.date(2017, 4, 20), 'cash_to_agreement': 20001.0, 'agreement_to_cash': 10001.0, 'ret_carry_principal': 1001.0, 'asset_ret': -1001.0, 'total_amount': 10000.0}
    fund:{'asset_name': '余额宝', 'cal_date': datetime.date(2017, 4, 20), 'cash_to_fund': 13009.0, 'fund_to_cash': 8011.0, 'asset_ret': 3005.0, 'ret_carry_cash': 1005.0, 'ret_not_carry': 2000.0, 'total_amount': 8003.0}
    cash:{'cal_date': datetime.date(2017, 4, 20), 'cash_to_agreement': 20001.0, 'cash_to_fund': 13009.0, 'cash_to_management': 20000.0, 'agreement_to_cash': 10001.0, 'fund_to_cash': 8011.0, 'management_to_cash': 15000.0, 'investor_to_cash': 100000.0, 'cash_to_investor': 0, 'cash_draw_fee': 0, 'cash_return': 0, 'total_amount': 80001.0}
    '''
    # add_management_class(name='management', trade_amount=10000, ret_rate=0.1, rate_days=360, start_date=date.today(),
    #                      end_date=date.today() + timedelta(days=200), bank_fee_rate=0.0003, manage_fee_rate=0.00015)

    # cal_management_fee(cal_date=date(2017, 1, 14), asset_id='c20d796695ee44eaa4f2f5755bba2767')
    # add_management_class(name='management1')
    # print(get_fund_detail_by_days())
    # print(get_single_agreement_detail_by_period(asset_id='b9537ae533d2487791f10155f814853b',
    #                                             start=date.today() - timedelta(days=10)))
    # print(get_agreement_detail_by_days())
    # cal_management_fee(asset_id='36429917ffd34b02b29f8c49eb25f557')
    # print(get_all_management_detail())
    # print(get_total_fund_statistic())
    # print(get_fund_detail_by_days())
    print(get_management_asset_all_ret('64fb8ad0c30f422bb65edff33535602a'))
    # cal_daily_ret_and_fee(asset_id='7fe9c108cd874c10b167782f798e1d35')
    # cal_agreement_ret(cal_date=date.today(),
    #                   asset=query_by_id(obj=AssetClass, obj_id='7fe9c108cd874c10b167782f798e1d35'))
    # print(get_management_all_ret(asset_id='7fe9c108cd874c10b167782f798e1d35'))
    # print(get_agreement_detail_by_days())

    # cal_adjust_fee(cal_date=date.today(), fee_amount=200, asset_id='85b05920001c41b2bfdef220d86c0125')

    # add_management(name='management2', trade_amount=100000, ret_rate=0.1, rate_days=360, start_date=date.today(),
    #                end_date=date.today() + timedelta(days=365), bank_fee_rate=0.0003, bank_days=360,
    #                manage_fee_rate=0.0012, manage_days=360, cal_date=date.today())

    # cal_daily_ret_and_fee(asset_id='327574da3cf14b368f150fcf7cda6b65')
