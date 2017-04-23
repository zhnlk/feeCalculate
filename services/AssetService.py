# encoding:utf8
from __future__ import unicode_literals

from datetime import date

from models.AssetClassModel import AssetClass
from models.AssetTradeModel import AssetTrade
from services.CommonService import (
    add_asset_ret_with_asset_and_type,
    add_asset_trade_with_asset_and_type,
    add_cash_with_type,
    get_asset_last_total_amount_by_asset_and_type,
    get_asset_ret_last_total_amount_by_asset_and_type,
    get_asset_by_name)
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
            ret_type=SV.RET_TYPE_CASH
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
        rate = asset.asset_ret_rate_list[0].rate
    elif len(rates) > 1:
        rate = list(filter(lambda x: x.threshold < amount, asset.asset_ret_rate_list))[-1].ret_rate
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
    rate = get_asset_rate_by_amount(rates=asset.asset_ret_rate_list, amount=total_amount)
    add_asset_ret_with_asset_and_type(
        amount=total_amount * rate / 360,
        asset_id=asset.id,
        ret_type=SV.RET_TYPE_INTEREST,
        cal_date=cal_date
    )


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

    # ret.update({SV.ASSET_KEY_RATE: asset.ret_rate})
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


if __name__ == '__main__':
    '''
    agreement:{'rate': 0.035, 'asset_name': '浦发理财一号', 'cal_date': datetime.date(2017, 4, 20), 'cash_to_agreement': 20001.0, 'agreement_to_cash': 10001.0, 'ret_carry_principal': 1001.0, 'asset_ret': -1001.0, 'total_amount': 10000.0}
    fund:{'asset_name': '余额宝', 'cal_date': datetime.date(2017, 4, 20), 'cash_to_fund': 13009.0, 'fund_to_cash': 8011.0, 'asset_ret': 3005.0, 'ret_carry_cash': 1005.0, 'ret_not_carry': 2000.0, 'total_amount': 8003.0}
    cash:{'cal_date': datetime.date(2017, 4, 20), 'cash_to_agreement': 20001.0, 'cash_to_fund': 13009.0, 'cash_to_management': 20000.0, 'agreement_to_cash': 10001.0, 'fund_to_cash': 8011.0, 'management_to_cash': 15000.0, 'investor_to_cash': 100000.0, 'cash_to_investor': 0, 'cash_draw_fee': 0, 'cash_return': 0, 'total_amount': 80001.0}
    '''
    asset = get_asset_by_name(name='浦发理财一号')
    print(asset.asset_ret_rate_list)
    cal_agreement_ret(asset=asset)
    # asset_ret_carry_to_principal()

    # print(list(query(AssetTrade).filter(AssetTrade.type == SV.ASSET_TYPE_REDEEM, AssetTrade.asset_class_obj.has(
    #     AssetClass.type == SV.ASSET_CLASS_FUND))))

    # add_daily_asset_data(asset_id='10e8743354f14fa383898d03a494c1af', ret_amount=1000)

    # add_agreement_daily_data(cal_date=date.today() - timedelta(days=0), asset_id='a4d124f92eba4d9c92fa1db44a21bc1d',
    #                          purchase_amount=10001, redeem_amount=5001,
    #                          ret_carry_asset_amount=1001)

    # add_fund_daily_data(cal_date=date.today() - timedelta(days=3), asset_id='9e272b078a3f46d0bed66e8665449fa5',
    #                     ret_carry_cash_amount=1002,
    #                     purchase_amount=10002, ret_amount=2002, redeem_amount=5002)

    # print(list(map(lambda x: x, map(lambda y: y, range(10)))))

    # add_agreement_daily_data(cal_date=date.today() - timedelta(days=1), asset_id='31a3a48e41114308b69f34a2192508fc',
    #                          purchase_amount=10003,
    #                          redeem_amount=1003, ret_carry_asset_amount=5003)

    # print(get_agreement_detail_by_days())

    # print(get_asset_date(days=2, asset_id='ec982b61c08d4c1688336a1b01ebb43c'))

    # print(get_agreement_detail_by_days(asset_id='ec982b61c08d4c1688336a1b01ebb43c'))

    # add_fund_daily_data(asset_id='10e8743354f14fa383898d03a494c1af', ret_carry_cash_amount=1005, purchase_amount=1005,
    #                     redeem_amount=1005, ret_amount=1005)

    # print((get_asset_agreement_detail(asset_id='c455e260b3144c7c8dba518dd64aa82a')))
    # print(get_asset_fund_detail(asset_id='10e8743354f14fa383898d03a494c1af'))
    # print(query(AssetClass).filter(AssetClass.id == 'c455e260b3144c7c8dba518dd64aa82a').one().asset_trade_list)
