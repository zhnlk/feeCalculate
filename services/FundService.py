# encoding:utf8

from __future__ import unicode_literals

from datetime import date, timedelta

from services.CommonService import get_asset_total_amount_by_class_and_type, \
    get_asset_ret_total_amount_by_class_and_type, get_asset_date
from utils import StaticValue as SV


def get_total_fund_statistic_by_date(cal_date=date.today()):
    '''
    :param cal_date: 
    :return: 
    '''
    total_purchase_amount = get_asset_total_amount_by_class_and_type(
        cal_date,
        SV.ASSET_CLASS_FUND,
        SV.ASSET_TYPE_PURCHASE)

    total_redeem_amount = get_asset_total_amount_by_class_and_type(cal_date, SV.ASSET_CLASS_FUND, SV.ASSET_TYPE_REDEEM)
    total_init_amount = get_asset_total_amount_by_class_and_type(cal_date, SV.ASSET_CLASS_FUND, SV.ASSET_TYPE_INIT)
    total_ret_amount = get_asset_ret_total_amount_by_class_and_type(cal_date, SV.ASSET_CLASS_FUND, SV.RET_TYPE_INTEREST)
    total_ret_init_amount = get_asset_ret_total_amount_by_class_and_type(
        cal_date,
        SV.ASSET_CLASS_FUND,
        SV.RET_TYPE_INIT
    )
    yes_total_ret_amount = get_asset_ret_total_amount_by_class_and_type(
        cal_date - timedelta(days=1),
        SV.ASSET_CLASS_FUND,
        SV.RET_TYPE_INTEREST
    )

    return {
        SV.ASSET_KEY_CAL_DATE: cal_date,
        SV.ASSET_KEY_FUND_TOTAL_RET_AMOUNT: total_ret_amount - yes_total_ret_amount,
        SV.ASSET_KEY_ASSET_TOTAL: total_purchase_amount + total_init_amount - total_redeem_amount + total_ret_amount + total_ret_init_amount
    }


def get_total_fund_statistic_by_days(days=0):
    ret = list()
    dates = get_asset_date(days, SV.ASSET_CLASS_FUND)
    if not dates:
        dates = [date.today()]
    for dat in dates:
        ret.append(get_total_fund_statistic_by_date(dat))

    return ret


def get_total_fund_statistic_by_period(start_date=date.today(), end_date=date.today()):
    ret = list()
    while start_date <= end_date:
        ret.append(get_total_fund_statistic_by_date(start_date))
        start_date += timedelta(days=1)
    return ret
