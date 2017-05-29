# encoding:utf8

from __future__ import unicode_literals

from datetime import date, timedelta

from models.AssetTradeRetModel import AssetTradeRet
from services.CommonService import get_asset_total_amount_by_class_and_type, \
    get_asset_ret_total_amount_by_class_and_type, get_asset_date, get_fund_princinal_input_by_id_date, \
    get_fund_ret_input_by_id_date, update_fund_asset_input_by_id, update_fund_ret_input_by_id, query_by_id, \
    cal_fund_ret_period
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


def get_fund_input_by_id_date_dic(fund_id=None, cal_date=date.today()):
    ret = list()
    for fund in get_fund_princinal_input_by_id_date(fund_id, cal_date):
        fund_dic = fund.to_dict()
        fund_dic.update({'is_asset': True})
        ret.append(fund_dic)

    for fund_ret in get_fund_ret_input_by_id_date(fund_id, cal_date):
        ret_dic = fund_ret.to_dict()
        ret_dic.update({'is_asset': False})
        ret.append(ret_dic)

    return ret


def update_fund_input_by_id_date(fund_trade_id=None, cal_date=date.today(), amount=0, is_asset=True):
    if is_asset:
        update_fund_asset_input_by_id(fund_trade_id, amount, cal_date)
    else:
        asset_id = query_by_id(AssetTradeRet, fund_trade_id).asset_class
        update_fund_ret_input_by_id(fund_trade_id, amount, cal_date)
        cal_fund_ret_period(asset_id, cal_date, date.today())
