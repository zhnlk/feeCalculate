# encoding:utf8

from __future__ import unicode_literals

from datetime import date, timedelta

from models.CashModel import Cash
from models.CommonModel import session_deco
from services.CommonService import save
from utils import StaticValue as SV


def add_cash_with_type(amount=0, cash_type=SV.CASH_TYPE_DEPOSIT):
    save(Cash(amount=amount, type=cash_type))


def get_key_by_cash_type(cash_type=SV.CASH_TYPE_DEPOSIT):
    key_dict = {
        SV.CASH_TYPE_DEPOSIT: SV.CASH_KEY_INVESTOR_DEPOSIT,
        SV.CASH_TYPE_DRAW: SV.CASH_KEY_INVESTOR_DRAW,
        SV.CASH_TYPE_FEE: SV.CASH_KEY_DRAW_FEE,
        SV.CASH_TYPE_RET: SV.CASH_KEY_RET
    }
    return key_dict[cash_type]


def get_key_by_cash_type_and_asset_class(cash_type=SV.CASH_TYPE_DEPOSIT, asset_class=SV.ASSET_CLASS_MANAGEMENT):
    key_dic = {
        SV.CASH_TYPE_PURCHASE: {
            SV.ASSET_CLASS_AGREEMENT_DEPOSIT: SV.CASH_KEY_PURCHASE_AGREEMENT,
            SV.ASSET_CLASS_FUND: SV.CASH_KEY_PURCHASE_FUND,
            SV.ASSET_CLASS_MANAGEMENT: SV.CASH_KEY_PURCHASE_MANAGEMENT

        },
        SV.CASH_TYPE_REDEEM: {
            SV.ASSET_CLASS_AGREEMENT_DEPOSIT: SV.CASH_KEY_REDEEM_AGREEMENT,
            SV.ASSET_CLASS_FUND: SV.CASH_KEY_REDEEM_FUND,
            SV.ASSET_CLASS_MANAGEMENT: SV.CASH_KEY_REDEEM_MANAGEMENT
        }
    }
    return key_dic[cash_type][asset_class]


@session_deco
def get_cash_with_type(cal_date=date.today(), cash_type=SV.CASH_TYPE_DEPOSIT, **kwargs):
    ret = dict()
    session = kwargs[SV.SESSION_KEY]
    cash_records = session.query(Cash).filter(Cash.type == cash_type, Cash.date < cal_date + timedelta(days=1))
    if cash_type not in [SV.CASH_TYPE_PURCHASE, SV.CASH_TYPE_REDEEM]:
        ret.update({get_key_by_cash_type(cash_type=cash_type): sum(
            list(map(lambda x: x.amount, cash_records)))}) if cash_records else ret.update(
            {get_key_by_cash_type(cash_type=cash_type): 0})
    else:
        ret.update(get_cash_with_purchase(cash_records=cash_records, cash_type=cash_type))

    return ret


def get_cash_with_purchase(cash_records=[], cash_type=SV.CASH_TYPE_PURCHASE):
    ret = {}
    cash_purchase_agreements = list(filter(
        lambda x: x.asset_class_obj.type == SV.ASSET_CLASS_AGREEMENT_DEPOSIT, cash_records))
    ret.update(
        {get_key_by_cash_type_and_asset_class(cash_type=cash_type, asset_class=SV.ASSET_CLASS_AGREEMENT_DEPOSIT): sum(
            list(map(lambda x: x.amount, cash_purchase_agreements)))}) if cash_purchase_agreements else ret.update(
        {get_key_by_cash_type_and_asset_class(cash_type=cash_type, asset_class=SV.ASSET_CLASS_AGREEMENT_DEPOSIT): 0})
    cash_purchase_fund = list(filter(
        lambda x: x.asset_class_obj.type == SV.ASSET_CLASS_FUND, cash_records))
    ret.update({get_key_by_cash_type_and_asset_class(cash_type=cash_type, asset_class=SV.ASSET_CLASS_FUND): sum(
        list(map(lambda x: x.amount, cash_purchase_fund)))}) if cash_purchase_fund else ret.update(
        {get_key_by_cash_type_and_asset_class(cash_type=cash_type, asset_class=SV.ASSET_CLASS_FUND): 0})
    cash_purchase_managements = list(filter(
        lambda x: x.asset_class_obj.type == SV.ASSET_CLASS_MANAGEMENT, cash_records))
    ret.update({get_key_by_cash_type_and_asset_class(cash_type=cash_type, asset_class=SV.ASSET_CLASS_MANAGEMENT): sum(
        list(map(lambda x: x.amount, cash_purchase_managements)))}) if cash_purchase_managements else ret.update(
        {get_key_by_cash_type_and_asset_class(cash_type=cash_type, asset_class=SV.ASSET_CLASS_MANAGEMENT): 0})
    return ret


def add_cash_daily_data(draw_amount=0, draw_fee=0, deposit_amount=0, ret_amount=0):
    '''
    添加现在记录
    :param draw_amount:兑付
    :param draw_fee:提出费用
    :param deposit_amount:流入
    :param ret_amount:现金收入
    :return: None
    '''
    add_cash_with_type(amount=draw_amount, cash_type=SV.CASH_TYPE_DRAW) if draw_amount else None
    add_cash_with_type(draw_fee, SV.CASH_TYPE_FEE) if draw_fee else None
    add_cash_with_type(deposit_amount, SV.CASH_TYPE_DEPOSIT) if deposit_amount else None
    add_cash_with_type(ret_amount, SV.CASH_TYPE_RET) if ret_amount else None


def get_detail(cal_date=date.today()):
    '''
    获取现金详情
    :param cal_date:计算日期
    :return: 详情字典
    '''
    ret = {SV.CASH_KEY_CAL_DATE: cal_date}
    ret.update(get_cash_with_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_PURCHASE))
    ret.update(get_cash_with_type(cal_date=cal_date, cash_type=SV.CASH_TYPE_REDEEM))
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


if __name__ == '__main__':
    print(get_detail())
    # add_cash_with_type(amount=1000, cash_type=SV.CASH_TYPE_DEPOSIT)
    # add_cash(0, 0, 10000, 10000)
    # print(get_cash_with_type(cal_date=cal_date,cash_type=SV.CASH_TYPE_REDEEM))
    # print(get_cash_with_type(cal_date=cal_date,cash_type=SV.CASH_TYPE_PURCHASE))
    # print(get_key_by_cash_type_and_asset_class(SV.CASH_TYPE_PURCHASE, SV.ASSET_CLASS_MANAGEMENT))
    # print(get_key_by_cash_type_and_asset_class(SV.CASH_TYPE_REDEEM, SV.ASSET_CLASS_MANAGEMENT))
