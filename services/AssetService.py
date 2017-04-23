# encoding:utf8
from __future__ import unicode_literals

from datetime import date, timedelta

from models.AssetClassModel import AssetClass
from models.AssetTradeModel import AssetTrade
from models.AssetTradeRetModel import AssetTradeRet
from models.CashModel import Cash
from models.CommonModel import session_deco
from services.CommonService import query, purchase, redeem, save
from utils import StaticValue as SV
from utils.Utils import timer


@session_deco
def asset_ret_carry_to_principal(cal_date=date.today(), asset=AssetClass(), amount=0, **kwargs):
    session = kwargs[SV.SESSION_KEY]
    if amount > 0:
        asset_trade_ret = AssetTradeRet(asset_class=asset.id, type=SV.RET_TYPE_PRINCIPAL, amount=amount)
        asset_trade_ret.date = cal_date
        session.add(asset_trade_ret)
        asset_trade = AssetTrade(asset_class=asset.id, amount=amount, type=SV.ASSET_TYPE_RET_CARRY)
        asset_trade.date = cal_date
        session.add(asset_trade)
    else:
        pass


@session_deco
def asset_ret_carry_to_cash(cal_date=date.today(), asset=AssetClass(), amount=0, **kwargs):
    session = kwargs[SV.SESSION_KEY]
    if amount > 0:
        session.add(AssetTradeRet(asset_class=asset.id, type=SV.RET_TYPE_CASH, amount=amount, cal_date=cal_date))
        session.add(Cash(asset_class=asset.id, type=SV.CASH_TYPE_CARRY, amount=amount, cal_date=cal_date))
    else:
        pass


def cal_agreement_ret(cal_date=date.today(), asset=AssetClass()):
    purchase_amount = get_asset_trades_total_amount_by_type(cal_date=cal_date, asset=asset,
                                                            trade_type=SV.ASSET_TYPE_PURCHASE)
    redeem_amount = get_asset_trades_total_amount_by_type(cal_date=cal_date, asset=asset,
                                                          trade_type=SV.ASSET_TYPE_REDEEM)
    carry_amount = get_asset_trades_total_amount_by_type(cal_date=cal_date, asset=asset,
                                                         trade_type=SV.ASSET_TYPE_RET_CARRY)
    save(AssetTradeRet(asset_class=asset.id,
                       amount=(purchase_amount - redeem_amount + carry_amount) * asset.ret_rate / 360,
                       cal_date=cal_date))


@session_deco
def add_trade_ret(cal_date=date.today(), ret_amount=0, asset=AssetClass(), **kwargs):
    session = kwargs[SV.SESSION_KEY]
    session.add(AssetTradeRet(asset_class=asset.id, amount=ret_amount, type=SV.RET_TYPE_INTEREST, cal_date=cal_date))


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


@timer
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


def get_asset_trades_total_amount_by_type(cal_date=date.today(), asset=AssetClass(), trade_type=SV.ASSET_TYPE_PURCHASE):
    asset_trades = list(
        filter(lambda x: x.date < cal_date + timedelta(days=1) and x.type == trade_type, asset.asset_trade_list))

    return sum(list(map(lambda x: x.amount, asset_trades)))


def get_asset_trades_sum_dic_by_type(cal_date=date.today(), asset=AssetClass(), trade_type=SV.ASSET_TYPE_PURCHASE):
    ret = dict()

    ret.update({get_key_by_asset_type_and_asset_class(asset_type=trade_type,
                                                      asset_class=asset.type): get_asset_trades_total_amount_by_type(
        cal_date=cal_date, asset=asset, trade_type=trade_type)})
    return ret


def get_asset_ret_by_type(cal_date=None, asset=AssetClass(), ret_type=SV.RET_TYPE_INTEREST):
    asset_rets = query(AssetTradeRet).filter(AssetTradeRet.asset_class == asset.id,
                                             AssetTradeRet.type == ret_type,
                                             AssetTradeRet.date < cal_date + timedelta(days=1))

    return sum(list(map(lambda x: x.amount, asset_rets)))


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


@timer
def get_asset_agreement_detail(cal_date=date.today(), asset_id=''):
    '''
    获取协存详情
    :param cal_date:计算日期
    :param asset_id:协存资产id
    :return:协存详情字典
    '''
    ret = dict()
    asset = query(AssetClass).filter(AssetClass.id == asset_id).one()
    ret.update({SV.ASSET_KEY_RATE: asset.ret_rate})
    ret.update(get_asset_base_detail(cal_date=cal_date, asset=asset))
    ret.update({SV.ASSET_KEY_RET_CARRY_PRINCIPAL: get_asset_trades_total_amount_by_type(cal_date=cal_date, asset=asset,
                                                                                        trade_type=SV.ASSET_TYPE_RET_CARRY)})
    ret.update({SV.ASSET_KEY_ASSET_RET: get_asset_ret_by_type(cal_date, asset, SV.RET_TYPE_INTEREST) - ret[
        SV.ASSET_KEY_RET_CARRY_PRINCIPAL]})
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
    ret.update(
        {SV.ASSET_KEY_ASSET_RET: get_asset_ret_by_type(cal_date=cal_date, asset=asset, ret_type=SV.RET_TYPE_INTEREST)})

    ret.update(
        {SV.ASSET_KEY_RET_CARRY_CASH: get_asset_ret_by_type(cal_date=cal_date, asset=asset, ret_type=SV.RET_TYPE_CASH)})

    ret.update({SV.ASSET_KEY_RET_NOT_CARRY: ret[SV.ASSET_KEY_ASSET_RET] - ret[SV.ASSET_KEY_RET_CARRY_CASH]})
    total_purchase = get_asset_trades_total_amount_by_type(cal_date=cal_date, asset=asset,
                                                           trade_type=SV.ASSET_TYPE_PURCHASE)
    total_redeem = get_asset_trades_total_amount_by_type(cal_date=cal_date, asset=asset,
                                                         trade_type=SV.ASSET_TYPE_REDEEM)

    ret.update({SV.ASSET_KEY_ASSET_TOTAL: total_purchase - total_redeem + ret[SV.ASSET_KEY_ASSET_RET]})

    return ret


def get_asset_date(days=0, asset_id=''):
    asset_dates = sorted(set(map(lambda x: x.date, query(AssetTrade).filter(AssetTrade.asset_class == asset_id))))
    if days:
        return asset_dates[-days:]
    return asset_dates


@timer
def get_single_agreement_detail_by_days(days=0, asset_id=''):
    return list(map(lambda x: get_asset_agreement_detail(cal_date=x, asset_id=asset_id),
                    get_asset_date(days=days, asset_id=asset_id)))


@timer
def get_agreement_detail_by_days(days=0):
    agreement_ids = list(
        map(lambda x: x.id, query(AssetClass).filter(AssetClass.type == SV.ASSET_CLASS_AGREEMENT)))

    return dict(list(map(lambda x: (x, get_single_agreement_detail_by_days(days=days, asset_id=x)), agreement_ids)))


def get_single_fund_detail_by_days(days=0, asset_id=''):
    return list(map(lambda x: get_asset_fund_detail(cal_date=x, asset_id=asset_id),
                    get_asset_date(days=days, asset_id=asset_id)))


def get_fund_detail_by_days(days=0):
    ret = dict()
    fund_ids = list(
        map(lambda x: x.id, query(AssetClass).filter(AssetClass.type == SV.ASSET_CLASS_FUND)))

    map(lambda x: ret.update({x: get_single_fund_detail_by_days(days=days, asset_id=x)}), fund_ids)
    return ret


if __name__ == '__main__':
    '''
    agreement:{'rate': 0.035, 'asset_name': '浦发理财一号', 'cal_date': datetime.date(2017, 4, 20), 'cash_to_agreement': 20001.0, 'agreement_to_cash': 10001.0, 'ret_carry_principal': 1001.0, 'asset_ret': -1001.0, 'total_amount': 10000.0}
    fund:{'asset_name': '余额宝', 'cal_date': datetime.date(2017, 4, 20), 'cash_to_fund': 13009.0, 'fund_to_cash': 8011.0, 'asset_ret': 3005.0, 'ret_carry_cash': 1005.0, 'ret_not_carry': 2000.0, 'total_amount': 8003.0}
    cash:{'cal_date': datetime.date(2017, 4, 20), 'cash_to_agreement': 20001.0, 'cash_to_fund': 13009.0, 'cash_to_management': 20000.0, 'agreement_to_cash': 10001.0, 'fund_to_cash': 8011.0, 'management_to_cash': 15000.0, 'investor_to_cash': 100000.0, 'cash_to_investor': 0, 'cash_draw_fee': 0, 'cash_return': 0, 'total_amount': 80001.0}
    '''
    # print(list(query(AssetTrade).filter(AssetTrade.type == SV.ASSET_TYPE_REDEEM, AssetTrade.asset_class_obj.has(
    #     AssetClass.type == SV.ASSET_CLASS_FUND))))

    # add_daily_asset_data(asset_id='10e8743354f14fa383898d03a494c1af', ret_amount=1000)

    # add_agreement_daily_data(cal_date=date.today() - timedelta(days=5), asset_id='bfc873a575f44aea9b3e433170288562',
    #                          purchase_amount=100000, redeem_amount=5000,
    #                          ret_carry_asset_amount=1000)

    # add_fund_daily_data(cal_date=date.today() - timedelta(days=3), asset_id='b62e634343614618966e0579d154711f',
    #                     ret_carry_cash_amount=1001,
    #                     purchase_amount=10001, ret_amount=2001, redeem_amount=5001)

    # print(list(map(lambda x: x, map(lambda y: y, range(10)))))

    # add_agreement_daily_data(cal_date=date.today() - timedelta(days=1), asset_id='31a3a48e41114308b69f34a2192508fc',
    #                          purchase_amount=10003,
    #                          redeem_amount=1003, ret_carry_asset_amount=5003)

    print(get_agreement_detail_by_days())

    # print(get_asset_date(days=2, asset_id='ec982b61c08d4c1688336a1b01ebb43c'))

    # print(get_agreement_detail_by_days(asset_id='ec982b61c08d4c1688336a1b01ebb43c'))

    # add_fund_daily_data(asset_id='10e8743354f14fa383898d03a494c1af', ret_carry_cash_amount=1005, purchase_amount=1005,
    #                     redeem_amount=1005, ret_amount=1005)

    # print((get_asset_agreement_detail(asset_id='c455e260b3144c7c8dba518dd64aa82a')))
    # print(get_asset_fund_detail(asset_id='10e8743354f14fa383898d03a494c1af'))
    # print(query(AssetClass).filter(AssetClass.id == 'c455e260b3144c7c8dba518dd64aa82a').one().asset_trade_list)
