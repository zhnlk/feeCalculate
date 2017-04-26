# encoding:utf8
from __future__ import unicode_literals

from datetime import date

from models.AssetClassModel import AssetClass
from models.AssetFeeRateModel import AssetFeeRate
from models.AssetRetRateModel import AssetRetRate
from models.AssetTradeModel import AssetTrade
from services.CommonService import (
    add_asset_ret_with_asset_and_type,
    add_asset_trade_with_asset_and_type,
    add_cash_with_type,
    get_asset_last_total_amount_by_asset_and_type,
    get_asset_ret_last_total_amount_by_asset_and_type,
    add_asset_fee_with_asset_and_type,
    query_by_id, save, get_management_asset_all_ret, get_management_trade_amount, get_management_trade_fees,
    get_all_mamangement_ids)
from services.CommonService import query, purchase, redeem
from utils import StaticValue as SV
from utils.Utils import timer


# Agreement

def asset_ret_carry_to_principal(cal_date=date.today(), asset=AssetClass(), amount=0):
    if amount > 0:
        add_asset_ret_with_asset_and_type(
            amount=amount,
            asset_id=asset.id,
            cal_date=cal_date,
            ret_type=SV.RET_TYPE_PRINCIPAL
        )
        add_asset_trade_with_asset_and_type(
            amount=amount,
            asset_id=asset.id,
            cal_date=cal_date,
            trade_type=SV.ASSET_TYPE_RET_CARRY
        )
    else:
        pass


def get_asset_rate_by_amount(rates=AssetClass().asset_ret_rate_list, amount=10000):
    rate = 0.0
    if len(rates) == 1:
        rate = rates[0].rate
    elif len(rates) > 1:
        rate = list(filter(lambda x: x.threshold <= amount, rates))[-1].ret_rate
    return rate


# Fund

def asset_ret_carry_to_cash(cal_date=date.today(), asset=AssetClass(), amount=0):
    if amount > 0:

        add_asset_ret_with_asset_and_type(
            amount=amount,
            asset_id=asset.id,
            cal_date=cal_date,
            ret_type=SV.RET_TYPE_CASH
        )

        add_cash_with_type(
            amount=amount,
            cash_type=SV.CASH_TYPE_CARRY,
            cal_date=cal_date
        )
    else:
        pass


# Management

def add_management(
        name='',
        trade_amount=1000000,
        ret_rate=0.1,
        rate_days=360,
        start_date=date.today(),
        end_date=date.today(),
        bank_fee_rate=0.0003,
        bank_days=360,
        manage_fee_rate=0.0012,
        manage_days=360,
        cal_date=date.today()
):
    asset = AssetClass(name=name, start_date=start_date, expiry_date=end_date, type=SV.ASSET_CLASS_MANAGEMENT,
                       ret_cal_method=SV.RET_TYPE_CASH_CUT_INTEREST, cal_date=cal_date)

    asset_rate = AssetRetRate(asset_id=asset.id, ret_rate=ret_rate, interest_days=rate_days, cal_date=cal_date)

    asset_fee_rate_bank = AssetFeeRate(asset_class=asset.id, rate=bank_fee_rate, type=SV.FEE_TYPE_PURCHASE,
                                       fee_days=bank_days, cal_date=cal_date)
    asset_fee_rate_manage = AssetFeeRate(asset_class=asset.id, rate=manage_fee_rate, type=SV.FEE_TYPE_PURCHASE,
                                         fee_days=manage_days, cal_date=cal_date)

    purchase(asset=asset, amount=trade_amount, cal_date=cal_date)
    save(asset)
    save(asset_rate)
    save(asset_fee_rate_bank)
    save(asset_fee_rate_manage)


def add_trade_ret(cal_date=date.today(), ret_amount=0, asset=AssetClass()):
    add_asset_ret_with_asset_and_type(
        amount=ret_amount,
        asset_id=asset.id,
        ret_type=SV.RET_TYPE_INTEREST,
        cal_date=cal_date
    )


def add_daily_asset_data(cal_date=date.today(), asset_id='', ret_carry_asset_amount=0, ret_carry_cash_amount=0,
                         purchase_amount=0,
                         redeem_amount=0, ret_amount=0):
    asset = query(AssetClass).filter(AssetClass.id == asset_id).one()
    asset_ret_carry_to_principal(cal_date=cal_date, asset=asset,
                                 amount=ret_carry_asset_amount) if ret_carry_asset_amount else None
    asset_ret_carry_to_cash(cal_date=cal_date, asset=asset,
                            amount=ret_carry_cash_amount) if ret_carry_cash_amount else None
    purchase(asset=asset, amount=purchase_amount, cal_date=cal_date) if purchase_amount else None
    redeem(asset=asset, amount=redeem_amount, cal_date=cal_date) if redeem_amount else None
    add_trade_ret(cal_date=cal_date, ret_amount=ret_amount, asset=asset) if ret_amount else None
    asset = query(AssetClass).filter(AssetClass.id == asset_id).one()
    cal_agreement_ret(cal_date=cal_date, asset=asset) if asset.type == SV.ASSET_CLASS_AGREEMENT else None


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
    return {
        get_key_by_asset_type_and_asset_class(
            asset_type=trade_type,
            asset_class=asset.type
        ): get_asset_last_total_amount_by_asset_and_type(
            cal_date=cal_date,
            asset_id=asset.id,
            trade_type=trade_type
        )
    }


def get_asset_base_detail(cal_date=date.today(), asset=AssetClass()):
    ret = dict()
    ret.update({SV.ASSET_KEY_NAME: asset.name, SV.ASSET_KEY_CAL_DATE: cal_date})
    ret.update(get_asset_trades_sum_dic_by_type(cal_date=cal_date, asset=asset, trade_type=SV.ASSET_TYPE_PURCHASE))
    ret.update(get_asset_trades_sum_dic_by_type(cal_date=cal_date, asset=asset, trade_type=SV.ASSET_TYPE_REDEEM))
    return ret


def add_agreement_daily_data(cal_date=date.today(), asset_id='', ret_carry_asset_amount=0, purchase_amount=0,
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


def add_fund_daily_data(cal_date=date.today(), asset_id='', ret_carry_cash_amount=0, purchase_amount=0, redeem_amount=0,
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
    add_daily_asset_data(cal_date=cal_date, asset_id=asset_id, ret_carry_cash_amount=ret_carry_cash_amount,
                         purchase_amount=purchase_amount, redeem_amount=redeem_amount, ret_amount=ret_amount)


def cal_agreement_ret(cal_date=date.today(), asset=AssetClass()):
    '''
    计算协存的利息
    :param cal_date:计算日期
    :param asset:资产对象
    :return:
    '''
    purchase_amount = get_asset_last_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset.id,
        trade_type=SV.ASSET_TYPE_PURCHASE
    )

    redeem_amount = get_asset_last_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset.id,
        trade_type=SV.ASSET_TYPE_REDEEM
    )
    carry_amount = get_asset_last_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset.id,
        trade_type=SV.ASSET_TYPE_RET_CARRY
    )

    total_amount = purchase_amount + carry_amount - redeem_amount
    asset = query_by_id(obj=AssetClass, obj_id=asset.id)
    rates = asset.asset_ret_rate_list
    rate = get_asset_rate_by_amount(rates=rates, amount=total_amount)
    add_asset_ret_with_asset_and_type(
        amount=total_amount * rate / 360,
        asset_id=asset.id,
        ret_type=SV.RET_TYPE_INTEREST,
        cal_date=cal_date
    ) if total_amount else None


# @timer
def get_asset_agreement_detail(cal_date=date.today(), asset_id=''):
    '''
    获取协存详情
    :param cal_date:计算日期
    :param asset_id:协存资产id
    :return:协存详情字典
    '''
    ret = dict()
    asset = query(AssetClass).filter(AssetClass.id == asset_id).one()
    ret[SV.ASSET_KEY_RATE] = list(map(lambda x: x.ret_rate, asset.asset_ret_rate_list))[
        0] if len(asset.asset_ret_rate_list) > 0 else 0.0
    ret.update(get_asset_base_detail(cal_date=cal_date, asset=asset))
    ret[SV.ASSET_KEY_RET_CARRY_PRINCIPAL] = get_asset_ret_last_total_amount_by_asset_and_type(
        asset_id=asset_id,
        cal_date=cal_date,
        ret_type=SV.RET_CARRY_TO_PRINCIPAL
    )
    ret[SV.ASSET_KEY_ASSET_RET] = get_asset_ret_last_total_amount_by_asset_and_type(
        asset_id=asset_id,
        cal_date=cal_date,
        ret_type=SV.RET_TYPE_INTEREST
    )
    ret.update({SV.ASSET_KEY_RET_CARRY_PRINCIPAL: get_asset_ret_last_total_amount_by_asset_and_type(
        asset_id=asset.id,
        cal_date=cal_date,
        ret_type=SV.RET_TYPE_PRINCIPAL
    )})
    ret.update({SV.ASSET_KEY_ASSET_RET: get_asset_ret_last_total_amount_by_asset_and_type(
        asset_id=asset.id,
        cal_date=cal_date,
        ret_type=SV.RET_TYPE_INTEREST
    ) - ret[SV.ASSET_KEY_RET_CARRY_PRINCIPAL]})
    ret.update({SV.ASSET_KEY_ASSET_TOTAL: ret[SV.ASSET_KEY_PURCHASE_AGREEMENT] + ret[SV.ASSET_KEY_RET_CARRY_PRINCIPAL] +
                                          ret[SV.ASSET_KEY_ASSET_RET] - ret.get(SV.ASSET_KEY_REDEEM_AGREEMENT, 0)})

    return ret


def get_asset_fund_detail(cal_date=date.today(), asset_id=''):
    '''
    获取货基详情
    :param cal_date:计算日期
    :param asset_id:货基资产id
    :return:货基详情字典
    '''
    ret = dict()
    asset = query(AssetClass).filter(AssetClass.id == asset_id).one()
    ret.update(get_asset_base_detail(cal_date=cal_date, asset=asset))
    ret.update({
        SV.ASSET_KEY_ASSET_RET:
            get_asset_ret_last_total_amount_by_asset_and_type(
                cal_date=cal_date,
                asset_id=asset_id,
                ret_type=SV.RET_TYPE_INTEREST
            )})

    ret.update({
        SV.ASSET_KEY_RET_CARRY_CASH:
            get_asset_ret_last_total_amount_by_asset_and_type(
                asset_id=asset_id,
                ret_type=SV.RET_TYPE_CASH,
                cal_date=cal_date
            )
    })

    ret.update({
        SV.ASSET_KEY_RET_NOT_CARRY:
            ret[SV.ASSET_KEY_ASSET_RET] - ret[SV.ASSET_KEY_RET_CARRY_CASH]})
    total_purchase = get_asset_last_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset_id,
        trade_type=SV.ASSET_TYPE_PURCHASE
    )
    total_redeem = get_asset_last_total_amount_by_asset_and_type(
        cal_date=cal_date,
        asset_id=asset_id,
        trade_type=SV.ASSET_TYPE_REDEEM
    )

    ret.update({SV.ASSET_KEY_ASSET_TOTAL: total_purchase - total_redeem + ret[SV.ASSET_KEY_ASSET_RET]})

    return ret


@timer
def get_asset_date(days=0, asset_id=''):
    asset_dates = sorted(set(map(lambda x: x.date, query(AssetTrade).filter(AssetTrade.asset_class == asset_id))))
    if days:
        return asset_dates[-days:]
    return asset_dates


# @timer
def get_single_agreement_detail_by_days(days=0, asset_id=''):
    return list(map(lambda x: get_asset_agreement_detail(cal_date=x, asset_id=asset_id),
                    get_asset_date(days=days, asset_id=asset_id)))


# @timer
def get_agreement_detail_by_days(days=0):
    agreement_ids = list(
        map(lambda x: x.id, query(AssetClass).filter(AssetClass.type == SV.ASSET_CLASS_AGREEMENT)))

    return dict((map(lambda x: (x, get_single_agreement_detail_by_days(days=days, asset_id=x)), agreement_ids)))


def get_single_fund_detail_by_days(days=0, asset_id=''):
    return list(map(lambda x: get_asset_fund_detail(cal_date=x, asset_id=asset_id),
                    get_asset_date(days=days, asset_id=asset_id)))


def get_fund_detail_by_days(days=0):
    fund_ids = list(
        map(lambda x: x.id, query(AssetClass).filter(AssetClass.type == SV.ASSET_CLASS_FUND)))

    return dict(map(lambda x: (x, get_single_fund_detail_by_days(days=days, asset_id=x)), fund_ids))


def cal_daily_ret_and_fee(cal_date=date.today(), asset_id=''):
    '''
    计算资管的收益和费用
    :param cal_date:计算日期
    :param asset_id:资产id
    :return:
    '''
    assetclass = query_by_id(obj=AssetClass, obj_id=asset_id)
    if cal_date < assetclass.expiry_date:
        asset_ret_rates = assetclass.asset_ret_rate_list
        asset_fee_rates = assetclass.asset_fee_rate_list
        asset_trade_amount = get_asset_last_total_amount_by_asset_and_type(asset_id=assetclass.id,
                                                                           trade_type=SV.ASSET_TYPE_PURCHASE,
                                                                           cal_date=cal_date)

        rate = asset_ret_rates[0]
        add_asset_ret_with_asset_and_type(amount=asset_trade_amount * rate.ret_rate / rate.interest_days,
                                          asset_id=asset_id, ret_type=SV.RET_TYPE_INTEREST, cal_date=cal_date)

        for x in asset_fee_rates:
            add_asset_fee_with_asset_and_type(
                amount=asset_trade_amount * x.rate / x.fee_days,
                asset_id=asset_id, fee_type=SV.FEE_TYPE_PURCHASE,
                cal_date=cal_date)


def cal_adjust_fee(cal_date=date.today(), fee_amount=200, asset_id=''):
    '''
    添加调整费用
    :param cal_date:计算日期
    :param fee_amount:调整费用
    :param asset_id:资产id
    :return:
    '''
    add_asset_fee_with_asset_and_type(cal_date=cal_date, asset_id=asset_id, fee_type=SV.FEE_TYPE_ADJUST,
                                      amount=fee_amount)


def management_carry_ret_to_cash(cal_date=date.today(), asset_id=''):
    asset = query_by_id(obj=AssetClass, obj_id=asset_id)
    if asset.ret_cal_method == SV.RET_TYPE_CASH_CUT_INTEREST:
        if asset.start_date == cal_date:
            add_asset_ret_with_asset_and_type(
                cal_date=cal_date,
                amount=get_management_asset_all_ret(asset_id=asset_id, cal_date=cal_date),
                asset_id=asset_id,
                ret_type=SV.RET_TYPE_CASH_CUT_INTEREST
            )
    elif asset.ret_cal_method == SV.RET_TYPE_CASH_ONE_TIME:
        if asset.expiry_date == cal_date:
            add_asset_ret_with_asset_and_type(
                cal_date=cal_date,
                amount=get_management_asset_all_ret(asset_id=asset_id, cal_date=cal_date),
                ret_type=SV.RET_TYPE_CASH_ONE_TIME
            )


def get_single_management_detail(asset_id=''):
    asset = query_by_id(obj=AssetClass, obj_id=asset_id)
    print(asset)
    ret = dict()
    ret.update({SV.ASSET_KEY_NAME: asset.name})
    ret.update({SV.ASSET_KEY_START_DATE: asset.start_date})
    ret.update({SV.ASSET_KEY_EXPIRY_DATE: asset.expiry_date})
    ret.update({SV.ASSET_KEY_MANAGEMENT_DUE: (
        asset.expiry_date - asset.start_date).days}) if asset.expiry_date and asset.start_date else ret.update(
        {SV.ASSET_KEY_MANAGEMENT_DUE: 360})
    ret.update({SV.ASSET_KEY_ASSET_RET: get_management_asset_all_ret(asset_id=asset.id)})
    ret.update({SV.ASSET_KEY_MANAGEMENT_AMOUNT: get_management_trade_amount(asset_id=asset_id)})

    fees = get_management_trade_fees(asset_id=asset_id)
    print(ret)
    ret.update({SV.ASSET_KEY_MANAGEMENT_BANK_FEE: ret.get(SV.ASSET_KEY_MANAGEMENT_AMOUNT) * fees[0].rate * ret.get(
        SV.ASSET_KEY_MANAGEMENT_DUE) / fees[0].fee_days}) if ret.get(SV.ASSET_KEY_MANAGEMENT_DUE) else ret.update(
        {SV.ASSET_KEY_MANAGEMENT_BANK_FEE: 200})
    ret.update({SV.ASSET_KEY_MANAGEMENT_MANAGE_FEE: ret.get(SV.ASSET_KEY_MANAGEMENT_AMOUNT) * fees[1].rate * ret.get(
        SV.ASSET_KEY_MANAGEMENT_DUE) / fees[1].fee_days}) if ret.get(SV.ASSET_KEY_MANAGEMENT_DUE) else ret.update(
        {SV.ASSET_KEY_MANAGEMENT_MANAGE_FEE: 100})
    ret.update({SV.ASSET_KEY_MANAGEMENT_DAILY_RET: (ret.get(SV.ASSET_KEY_ASSET_RET) - ret.get(
        SV.ASSET_KEY_MANAGEMENT_BANK_FEE) - ret.get(
        SV.ASSET_KEY_MANAGEMENT_MANAGE_FEE)) / ret.get(
        SV.ASSET_KEY_MANAGEMENT_DUE)})
    return ret


def get_all_management_detail():
    ret = dict()
    ids = get_all_mamangement_ids()
    for id in ids:
        ret.update({id: get_single_management_detail(asset_id=id)})
    return ret


def get_total_fund_statistic(cal_date=date.today(), asset_id=''):
    total_purchase_amount = get_asset_last_total_amount_by_asset_and_type(cal_date=cal_date, asset_id=asset_id,
                                                                          trade_type=SV.ASSET_TYPE_PURCHASE)
    total_redeem_amount = get_asset_last_total_amount_by_asset_and_type(cal_date=cal_date, asset_id=asset_id,
                                                                        trade_type=SV.ASSET_TYPE_REDEEM)
    total_amount = total_purchase_amount - total_redeem_amount
    total_ret_amount = get_asset_ret_last_total_amount_by_asset_and_type(cal_date=cal_date, asset_id=asset_id,
                                                                         ret_type=SV.RET_TYPE_INTEREST)
    return {
        SV.ASSET_KEY_FUND_TOTAL_AMOUNT: total_amount,
        SV.ASSET_KEY_FUND_TOTAL_PURCHASE_AMOUNT: total_purchase_amount,
        SV.ASSET_KEY_FUND_TOTAL_REDEEM_AMOUNT: total_redeem_amount,
        SV.ASSET_KEY_FUND_TOTAL_RET_AMOUNT: total_ret_amount
    }


if __name__ == '__main__':
    '''
    agreement:{'rate': 0.035, 'asset_name': '浦发理财一号', 'cal_date': datetime.date(2017, 4, 20), 'cash_to_agreement': 20001.0, 'agreement_to_cash': 10001.0, 'ret_carry_principal': 1001.0, 'asset_ret': -1001.0, 'total_amount': 10000.0}
    fund:{'asset_name': '余额宝', 'cal_date': datetime.date(2017, 4, 20), 'cash_to_fund': 13009.0, 'fund_to_cash': 8011.0, 'asset_ret': 3005.0, 'ret_carry_cash': 1005.0, 'ret_not_carry': 2000.0, 'total_amount': 8003.0}
    cash:{'cal_date': datetime.date(2017, 4, 20), 'cash_to_agreement': 20001.0, 'cash_to_fund': 13009.0, 'cash_to_management': 20000.0, 'agreement_to_cash': 10001.0, 'fund_to_cash': 8011.0, 'management_to_cash': 15000.0, 'investor_to_cash': 100000.0, 'cash_to_investor': 0, 'cash_draw_fee': 0, 'cash_return': 0, 'total_amount': 80001.0}
    '''
    print(get_all_management_detail())
    # print(get_single_management_detail(asset_id='8f62d3fb42ec49459de78934753f57ae'))
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
