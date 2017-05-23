# encoding:utf8

from __future__ import unicode_literals

from datetime import date, timedelta

from services.CommonService import get_asset_total_amount_by_class_and_type, \
    get_asset_ret_total_amount_by_class_and_type, get_asset_date, get_agreement_input_detail_by_id_date
from utils import StaticValue as SV


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


def get_total_agreement_statistic_by_days(days=0):
    dates = get_asset_date(days, SV.ASSET_CLASS_AGREEMENT)
    ret = list()
    if not dates:
        dates = [date.today()]
    for dat in dates:
        ret.append(get_total_agreement_statistic_by_date(dat))
    return ret


def get_agreement_input_detail_by_id_date_dic(agreement_id=None, cal_date=date.today()):
    ret = list()
    for agreement in get_agreement_input_detail_by_id_date(agreement_id, cal_date):
        ret.append(agreement.to_dict())
    return ret




print(get_agreement_input_detail_by_id_date_dic('15cb6beea2f3459ca37d7bcbc4828e0a', date(2017, 5, 23)))

#
# print(get_total_agreement_statistic_by_days(7))
# print(get_total_agreement_statistic_by_period(date.today() - timedelta(days=6)))
