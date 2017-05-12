# encoding:utf8

from __future__ import unicode_literals

from datetime import date

from models.AssetClassModel import AssetClass
from models.AssetRetRateModel import AssetRetRate
from services.CommonService import (
    add_cash_with_type,
    save,
    add_asset_trade_with_asset_and_type,
    add_asset_ret_with_asset_and_type
)
from utils import StaticValue as SV


def init_cash_data(
        cal_date=date.today(),
        cash_total_amount=0,
        p_agree_amount=0,
        p_fund_amount=0,
        p_manage_amount=0,
        r_agree_amount=0,
        r_fund_amount=0,
        r_manage_amount=0,
        investor_deposit_amount=0,
        investor_draw_amount=0,
        fee_amount=0,
        ret_carry_amount=0,
        ret_amount=0
):
    '''
    现金初始化
    :param cal_date: 
    :param cash_total_amount: 
    :param p_agree_amount: 
    :param p_fund_amount: 
    :param p_manage_amount: 
    :param r_agree_amount: 
    :param r_fund_amount: 
    :param r_manage_amount: 
    :param investor_deposit_amount: 
    :param investor_draw_amount: 
    :param fee_amount: 
    :param ret_carry_amount: 
    :param ret_amount: 
    :return: 
    '''
    init_amount = cash_total_amount + r_agree_amount - r_fund_amount - r_manage_amount + p_agree_amount + p_fund_amount \
                  + p_manage_amount + fee_amount - ret_amount - ret_carry_amount - investor_deposit_amount + investor_draw_amount

    add_cash_with_type(
        init_amount,
        cash_type=SV.CASH_TYPE_INIT,
        cal_date=cal_date
    ) if init_amount else None
    add_cash_with_type(
        p_agree_amount,
        SV.CASH_TYPE_PURCHASE_AGREEMENT,
        cal_date=cal_date
    ) if p_agree_amount else None
    add_cash_with_type(
        p_fund_amount,
        SV.CASH_TYPE_PURCHASE_FUND,
        cal_date=cal_date
    ) if p_fund_amount else None
    add_cash_with_type(
        p_manage_amount,
        SV.CASH_TYPE_PURCHASE_MANAGEMENT,
        cal_date=cal_date
    ) if p_manage_amount else None
    add_cash_with_type(
        r_agree_amount,
        SV.CASH_TYPE_REDEEM_AGREEMENT,
        cal_date=cal_date
    ) if init_amount else None
    add_cash_with_type(
        r_fund_amount,
        SV.CASH_TYPE_REDEEM_FUND,
        cal_date=cal_date
    ) if r_agree_amount else None
    add_cash_with_type(
        r_manage_amount,
        SV.CASH_TYPE_REDEEM_MANAGEMENT,
        cal_date=cal_date
    ) if r_fund_amount else None
    add_cash_with_type(
        ret_carry_amount,
        SV.CASH_TYPE_CARRY,
        cal_date=cal_date
    ) if r_manage_amount else None
    add_cash_with_type(
        investor_deposit_amount,
        SV.CASH_TYPE_DEPOSIT,
        cal_date=cal_date
    ) if investor_deposit_amount else None
    add_cash_with_type(
        investor_draw_amount,
        SV.CASH_TYPE_DRAW,
        cal_date=cal_date
    ) if investor_draw_amount else None
    add_cash_with_type(
        fee_amount,
        SV.CASH_TYPE_FEE,
        cal_date=cal_date
    ) if fee_amount else None
    add_cash_with_type(
        ret_amount,
        SV.CASH_TYPE_RET,
        cal_date=cal_date
    ) if ret_amount else None


def init_agreement_data(
        cal_date=date.today(),
        agree_name=None,
        rate=0.03,
        threshold_amount=100000,
        threshold_rate=0.04,
        principal_amount=0,
        total_amount=0,
        ret_amount=0,
        purchase_amount=0,
        redeem_amount=0,
        carry_amount=0
):
    '''
    初始化协存数据
    :param cal_date: 
    :param agree_name: 
    :param rate: 
    :param threshold_amount: 
    :param threshold_rate: 
    :param principal_amount: 
    :param total_amount: 
    :param ret_amount: 
    :param purchase_amount: 
    :param redeem_amount: 
    :param carry_amount: 
    :return: 
    '''
    asset = AssetClass(
        cal_date=cal_date,
        name=agree_name,
        type=SV.ASSET_CLASS_AGREEMENT
    )
    save(
        asset
    )
    asset_rate = AssetRetRate(
        asset_id=asset.id,
        ret_rate=rate,
        cal_date=cal_date
    )
    save(
        asset_rate
    )
    asset_threshold_rate = AssetRetRate(

        asset_id=asset.id,
        ret_rate=threshold_rate,
        threshold=threshold_amount,
        cal_date=cal_date

    )
    save(
        asset_threshold_rate
    ) if threshold_rate else None

    init_principal_amount = principal_amount - purchase_amount + redeem_amount - carry_amount
    add_asset_trade_with_asset_and_type(
        init_principal_amount,
        SV.ASSET_TYPE_INIT,
        asset.id,
        cal_date
    ) if init_principal_amount else None
    add_asset_trade_with_asset_and_type(
        purchase_amount,
        SV.ASSET_TYPE_PURCHASE,
        asset.id,
        cal_date
    ) if purchase_amount else None
    add_asset_trade_with_asset_and_type(
        redeem_amount,
        SV.ASSET_TYPE_REDEEM,
        asset.id,
        cal_date
    ) if redeem_amount else None

    init_ret_amount = total_amount - principal_amount - ret_amount
    add_asset_ret_with_asset_and_type(
        init_ret_amount,
        asset.id,
        SV.RET_TYPE_INIT,
        cal_date
    ) if init_ret_amount else None

    add_asset_ret_with_asset_and_type(
        ret_amount,
        asset.id,
        SV.RET_TYPE_INTEREST,
        cal_date
    ) if ret_amount else None
    add_asset_ret_with_asset_and_type(
        carry_amount,
        asset.id,
        SV.RET_TYPE_PRINCIPAL,
        cal_date
    ) if carry_amount else None


def init_fund_data(
        fund_name='',
        cal_date=date.today(),
        total_amount=0,
        purchase_amount=0,
        redeem_amount=0,
        not_carry_amount=0,
        carry_amount=0,
        ret_amount=0
):
    '''
    初始化协存数据
    :param fund_name: 
    :param cal_date: 
    :param total_amount: 
    :param purchase_amount: 
    :param redeem_amount: 
    :param not_carry_amount: 
    :param carry_amount: 
    :return: 
    '''
    asset = AssetClass(
        name=fund_name,
        type=SV.ASSET_CLASS_FUND
    )
    save(
        asset
    )

    init_total_amount = total_amount - purchase_amount + redeem_amount - not_carry_amount
    add_asset_trade_with_asset_and_type(init_total_amount, SV.ASSET_TYPE_INIT, asset.id,
                                        cal_date) if init_total_amount else None
    add_asset_trade_with_asset_and_type(purchase_amount, SV.ASSET_TYPE_PURCHASE, asset.id,
                                        cal_date) if purchase_amount else None
    add_asset_trade_with_asset_and_type(redeem_amount, SV.ASSET_TYPE_REDEEM, asset.id,
                                        cal_date) if redeem_amount else None
    init_ret_amount = not_carry_amount - ret_amount
    add_asset_ret_with_asset_and_type(init_ret_amount, asset.id, SV.RET_TYPE_INIT,
                                      cal_date) if init_ret_amount else None
    add_asset_ret_with_asset_and_type(ret_amount, asset.id, SV.RET_TYPE_INTEREST,
                                      cal_date) if ret_amount else None
    add_asset_ret_with_asset_and_type(carry_amount, asset.id, SV.RET_TYPE_CASH, cal_date) if carry_amount else None


if __name__ == '__main__':
    # 计算时间
    cal_date = date(2017, 3, 1)
    # 现金初始化
    cash_total_amount = 0
    p_agree_amount = 0
    p_fund_amount = 0
    p_manage_amount = 0
    r_agree_amount = 0
    r_fund_amount = 0
    r_manage_amount = 0
    investor_deposit_amount = 0
    investor_draw_amount = 0
    fee_amount = 0
    ret_carry_amount = 0
    ret_amount = 0
    init_cash_data(
        cal_date,
        cash_total_amount,
        p_agree_amount,
        p_fund_amount,
        p_manage_amount,
        r_agree_amount,
        r_fund_amount,
        r_manage_amount,
        investor_deposit_amount,
        investor_draw_amount,
        fee_amount,
        ret_carry_amount,
        ret_amount
    )

    # 协存初始化
    agree_name = '盛京银行'
    rate = 0.0302
    threshold_amount = 0
    threshold_rate = 0
    principal_amount = 1850901861.79
    total_amount = 1854931311.75
    ret_amount = 155270.10
    purchase_amount = 0
    redeem_amount = 0
    carry_amount = 0
    init_agreement_data(
        cal_date,
        agree_name,
        rate,
        threshold_amount,
        threshold_rate,
        principal_amount,
        total_amount,
        ret_amount,
        purchase_amount,
        redeem_amount,
        carry_amount
    )

    agree_name = '上饶银行'
    rate = 0.0301
    threshold_amount = 0
    threshold_rate = 0
    principal_amount = 0
    total_amount = 0
    ret_amount = 0
    purchase_amount = 0
    redeem_amount = 0
    carry_amount = 0
    init_agreement_data(
        cal_date,
        agree_name,
        rate,
        threshold_amount,
        threshold_rate,
        principal_amount,
        total_amount,
        ret_amount,
        purchase_amount,
        redeem_amount,
        carry_amount
    )

    # 货基初化

    fund_name = '广发基金'
    total_amount = 213624.39
    not_carry_amount = 213624.39
    carry_amount = 0
    purchase_amount = 0
    redeem_amount = 0
    ret_amount = 0
    init_fund_data(
        fund_name,
        cal_date,
        total_amount,
        purchase_amount,
        redeem_amount,
        not_carry_amount,
        carry_amount,
        ret_amount
    )

    fund_name = '易方达基金'
    total_amount = 103301188.11
    not_carry_amount = 114530.21
    carry_amount = 0
    purchase_amount = 46242609.58
    redeem_amount = 79520556.13
    ret_amount = 13905.68
    init_fund_data(
        fund_name,
        cal_date,
        total_amount,
        purchase_amount,
        redeem_amount,
        not_carry_amount,
        carry_amount,
        ret_amount
    )

    fund_name = '易方达天天理财'
    total_amount = 1484276386.28
    not_carry_amount = 174860.39
    carry_amount = 0
    purchase_amount = 0
    redeem_amount = 0
    ret_amount = 174860.39
    init_fund_data(
        fund_name,
        cal_date,
        total_amount,
        purchase_amount,
        redeem_amount,
        not_carry_amount,
        carry_amount,
        ret_amount
    )

    fund_name = '广发钱袋子基金'
    total_amount = 737063855.94
    not_carry_amount = 75204.70
    carry_amount = 75204.70
    purchase_amount = 100000000.00
    redeem_amount = 70000000.00
    ret_amount = 75204.70
    init_fund_data(
        fund_name,
        cal_date,
        total_amount,
        purchase_amount,
        redeem_amount,
        not_carry_amount,
        carry_amount,
        ret_amount
    )
