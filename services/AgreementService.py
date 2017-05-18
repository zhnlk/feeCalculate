# encoding:utf8

from __future__ import unicode_literals

from datetime import date, timedelta

from services.CommonService import get_asset_total_amount_by_class_and_type, \
    get_asset_ret_total_amount_by_class_and_type
from utils import StaticValue as SV


#
# def add_agreement_class(name=None, rate=0.03, threshold_amount=0, threshold_rate=0):
#     '''
#     添加协存类别
#     :param name:名称
#     :param rate:利率
#     :param threshold_amount:阶梯额度
#     :param threshold_rate:阶梯利率
#     :return:
#     '''
#     agreement = AssetClass(name=name, type=SV.ASSET_CLASS_AGREEMENT, code='1001')
#     save(agreement)
#     save(
#         AssetRetRate(
#             asset_id=agreement.id,
#             ret_rate=rate,
#             threshold=0.0,
#             interest_days=360
#         )
#     )
#     save(
#         AssetRetRate(
#             asset_id=agreement.id,
#             ret_rate=threshold_rate,
#             threshold=threshold_amount,
#             interest_days=360
#         )
#     ) if threshold_amount and threshold_rate else None
#
#
# def add_agreement_daily_data(cal_date=date.today(), asset_id=None, ret_carry_asset_amount=0, purchase_amount=0,
#                              redeem_amount=0):
#     '''
#     添加协存每日记录
#     :param cal_date:计算日期
#     :param asset_id:协存资产id
#     :param ret_carry_asset_amount:收益结转本金
#     :param purchase_amount:申购金额
#     :param redeem_amount:赎回金额
#     :return:None
#     '''
#     add_daily_asset_data(cal_date=cal_date, asset_id=asset_id, ret_carry_asset_amount=ret_carry_asset_amount,
#                          purchase_amount=purchase_amount, redeem_amount=redeem_amount)
#
#
# def cal_agreement_ret(cal_date=date.today(), asset_id=None):
#     '''
#     计算到计算日期的所有利息
#     :param cal_date: 计算日期
#     :param asset_id: 资产id
#     :return:
#     '''
#     init_date = get_asset_ret_last_date_before_cal_date(cal_date, asset_id)
#     while init_date <= cal_date:
#         cal_agreement_ret_of_asset(cal_date=init_date, asset_id=asset_id)
#         init_date += timedelta(days=1)
#
#
# def get_agreement_principal_at_date(cal_date=date.today(), asset_id=None):
#     return get_asset_total_amount_by_asset_and_type(
#         cal_date, asset_id, SV.ASSET_TYPE_PURCHASE
#     ) - get_asset_total_amount_by_asset_and_type(
#         cal_date, asset_id, SV.ASSET_TYPE_REDEEM
#     ) + get_asset_total_amount_by_asset_and_type(
#         cal_date, asset_id, SV.ASSET_TYPE_RET_CARRY
#     ) + get_asset_total_amount_by_asset_and_type(
#         cal_date, asset_id, SV.ASSET_TYPE_INIT
#     )
#
#
# def cal_agreement_ret_of_asset(cal_date=date.today(), asset_id=None):
#     '''
#     计算协存的利息
#     :param cal_date:计算日期
#     :param asset:资产对象
#     :return:
#     '''
#
#     purchase_amount = get_asset_total_amount_by_asset_and_type(
#         cal_date=cal_date,
#         asset_id=asset_id,
#         trade_type=SV.ASSET_TYPE_PURCHASE
#     )  # 计算所有申购金额
#
#     redeem_amount = get_asset_total_amount_by_asset_and_type(
#         cal_date=cal_date,
#         asset_id=asset_id,
#         trade_type=SV.ASSET_TYPE_REDEEM
#     )  # 计算所有赎回金额
#     carry_amount = get_asset_total_amount_by_asset_and_type(
#         cal_date=cal_date,
#         asset_id=asset_id,
#         trade_type=SV.ASSET_TYPE_RET_CARRY
#     )  # 结转本金金额
#
#     init_asset_amount = get_asset_total_amount_by_asset_and_type(
#         cal_date, asset_id, SV.ASSET_TYPE_INIT
#     )  # 初始化金额
#
#     total_amount = purchase_amount + carry_amount - redeem_amount + init_asset_amount
#     asset = query_by_id(obj=AssetClass, obj_id=asset_id)
#     rates = asset.asset_ret_rate_list
#     rate = get_asset_rate_by_amount(rates=rates, amount=total_amount)
#     add_asset_ret_with_asset_and_type(
#         amount=total_amount * rate.ret_rate / 360,
#         asset_id=asset.id,
#         ret_type=SV.RET_TYPE_INTEREST,
#         cal_date=cal_date
#     ) if total_amount else None


def get_total_agreement_statistic_by_date(cal_date=date.today()):
    '''
    :param cal_date: 
    :return: 
    '''
    total_purchase_amount = get_asset_total_amount_by_class_and_type(
        cal_date,
        SV.ASSET_CLASS_AGREEMENT,
        SV.ASSET_TYPE_PURCHASE)

    total_redeem_amount = get_asset_total_amount_by_class_and_type(cal_date, SV.ASSET_CLASS_AGREEMENT,
                                                                   SV.ASSET_TYPE_REDEEM)
    total_init_amount = get_asset_total_amount_by_class_and_type(cal_date, SV.ASSET_CLASS_AGREEMENT, SV.ASSET_TYPE_INIT)
    total_ret_amount = get_asset_ret_total_amount_by_class_and_type(cal_date, SV.ASSET_CLASS_AGREEMENT,
                                                                    SV.RET_TYPE_INTEREST)
    total_ret_init_amount = get_asset_ret_total_amount_by_class_and_type(
        cal_date,
        SV.ASSET_CLASS_AGREEMENT,
        SV.RET_TYPE_INIT
    )
    yes_total_ret_amount = get_asset_ret_total_amount_by_class_and_type(
        cal_date - timedelta(days=1),
        SV.ASSET_CLASS_AGREEMENT,
        SV.RET_TYPE_INTEREST
    )

    return {
        SV.ASSET_KEY_CAL_DATE: cal_date,
        SV.ASSET_KEY_FUND_TOTAL_RET_AMOUNT: total_ret_amount - yes_total_ret_amount,
        SV.ASSET_KEY_ASSET_TOTAL: total_purchase_amount + total_init_amount - total_redeem_amount + total_ret_amount + total_ret_init_amount
    }


def get_total_agreement_statistic_by_period(start_date=date.today(), end_date=date.today()):
    ret = list()
    while start_date <= end_date:
        ret.append(get_total_agreement_statistic_by_date(start_date))
        start_date += timedelta(days=1)
    return ret
