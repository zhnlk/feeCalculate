# encoding:utf8

from __future__ import unicode_literals

from datetime import date, timedelta

from models.CashModel import Cash
from services.CommonService import query, add_cash_with_type, get_cash_last_total_amount_by_type
from utils import StaticValue as SV
from utils.Utils import timer


def get_key_by_cash_type(cash_type=SV.CASH_TYPE_DEPOSIT):
    key_dict = {
        SV.CASH_TYPE_DEPOSIT: SV.CASH_KEY_INVESTOR_DEPOSIT,
        SV.CASH_TYPE_DRAW: SV.CASH_KEY_INVESTOR_DRAW,
        SV.CASH_TYPE_FEE: SV.CASH_KEY_DRAW_FEE,
        SV.CASH_TYPE_RET: SV.CASH_KEY_RET,
        SV.CASH_TYPE_PURCHASE_AGREEMENT: SV.CASH_KEY_PURCHASE_AGREEMENT,
        SV.CASH_TYPE_PURCHASE_FUND: SV.CASH_KEY_PURCHASE_FUND,
        SV.CASH_TYPE_PURCHASE_MANAGEMENT: SV.CASH_KEY_PURCHASE_MANAGEMENT,
        SV.CASH_TYPE_REDEEM_AGREEMENT: SV.CASH_KEY_REDEEM_AGREEMENT,
        SV.CASH_TYPE_REDEEM_FUND: SV.CASH_KEY_REDEEM_FUND,
        SV.CASH_TYPE_REDEEM_MANAGEMENT: SV.CASH_KEY_REDEEM_MANAGEMENT
    }
    return key_dict[cash_type]


def get_cash_with_type(cal_date=date.today(), cash_type=SV.CASH_TYPE_DEPOSIT):
    return {
        get_key_by_cash_type(cash_type=cash_type):
            get_cash_last_total_amount_by_type(
                cal_date=cal_date,
                cash_type=cash_type
            )

    }


def get_cash_date(days=0):
    dates = sorted(
        list(set(map(lambda x: x.date, query(Cash)))))
    if days:
        return dates[-days:]
    else:
        return dates


def add_cash_daily_data(cal_date=date.today(), draw_amount=0, draw_fee=0, deposit_amount=0, ret_amount=0):
    '''
    添加现在记录
    :param draw_amount:兑付
    :param draw_fee:提出费用
    :param deposit_amount:流入
    :param ret_amount:现金收入
    :return: None
    '''
    add_cash_with_type(amount=draw_amount, cash_type=SV.CASH_TYPE_DRAW, cal_date=cal_date) if draw_amount else None
    add_cash_with_type(amount=draw_fee, cash_type=SV.CASH_TYPE_FEE, cal_date=cal_date) if draw_fee else None
    add_cash_with_type(amount=deposit_amount, cash_type=SV.CASH_TYPE_DEPOSIT,
                       cal_date=cal_date) if deposit_amount else None
    add_cash_with_type(amount=ret_amount, cash_type=SV.CASH_TYPE_RET, cal_date=cal_date) if ret_amount else None


def get_cash_daily_detail(cal_date=date.today()):
    '''
    获取现金详情
    :param cal_date:计算日期
    :return: 详情字典
    '''
    ret = {SV.CASH_KEY_CAL_DATE: cal_date}
    ret.update(get_cash_with_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_PURCHASE_AGREEMENT))
    ret.update(get_cash_with_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_PURCHASE_FUND))
    ret.update(get_cash_with_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_PURCHASE_MANAGEMENT))
    ret.update(get_cash_with_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_REDEEM_AGREEMENT))
    ret.update(get_cash_with_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_REDEEM_FUND))
    ret.update(get_cash_with_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_REDEEM_MANAGEMENT))
    ret.update(get_cash_with_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_DEPOSIT))
    ret.update(get_cash_with_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_DRAW))
    ret.update(get_cash_with_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_FEE))
    ret.update(get_cash_with_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_RET))
    ret.update({SV.CASH_KEY_CASH_TOTAL: ret[SV.CASH_KEY_REDEEM_AGREEMENT] + ret[SV.CASH_KEY_REDEEM_FUND] + ret[
        SV.CASH_KEY_REDEEM_MANAGEMENT] + ret[SV.CASH_KEY_INVESTOR_DEPOSIT] + ret[SV.CASH_KEY_RET] - ret[
                                            SV.CASH_KEY_PURCHASE_AGREEMENT] - ret[SV.CASH_KEY_PURCHASE_FUND] - ret[
                                            SV.CASH_KEY_PURCHASE_AGREEMENT] - ret[SV.CASH_KEY_INVESTOR_DRAW] - ret[
                                            SV.CASH_KEY_INVESTOR_DRAW] - ret[SV.CASH_KEY_DRAW_FEE]})
    return ret


@timer
def get_cash_detail_by_days(days=0):
    '''
    按天数获取现金详情，天数为0时，获取所有详情
    :param days:天数
    :return:
    '''
    return list(map(lambda x: get_cash_daily_detail(cal_date=x), get_cash_date(days=days)))


if __name__ == '__main__':
    print((get_cash_last_total_amount_by_type(cash_type=SV.CASH_TYPE_DEPOSIT)))
    # print(get_last_total_amount_by_type(cash_type=SV.CASH_TYPE_PURCHASE))
    add_cash_daily_data(cal_date=date.today() - timedelta(days=9), draw_amount=10001, draw_fee=10.01,
                        deposit_amount=1000000,
                        ret_amount=4000)
    # print(get_cash_date())


    # print(get_cash_detail_by_days(days=3))
    # import time
    #
    # print(get_last_total_amount_by_type(cal_date=date.today() - timedelta(days=0), cash_type=SV.CASH_TYPE_DEPOSIT))
    #
    # start_time = time.time()
    # print(get_cash_detail_by_days())
    # end_time = time.time()
    # print(end_time - start_time)
    # print(get_detail())
    # add_cash_with_type(amount=1000, cash_type=SV.CASH_TYPE_DEPOSIT)
    # add_cash(0, 0, 10000, 10000)
    # print(get_cash_with_type(cal_date=cal_date,cash_type=SV.CASH_TYPE_REDEEM))
    # print(get_cash_with_type(cal_date=cal_date,cash_type=SV.CASH_TYPE_PURCHASE))
    # print(get_key_by_cash_type_and_asset_class(SV.CASH_TYPE_PURCHASE, SV.ASSET_CLASS_MANAGEMENT))
    # print(get_key_by_cash_type_and_asset_class(SV.CASH_TYPE_REDEEM, SV.ASSET_CLASS_MANAGEMENT))
