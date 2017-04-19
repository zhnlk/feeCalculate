# encoding:utf8

from __future__ import unicode_literals

from datetime import date, timedelta

from models.AssetClassModel import AssetClass
from models.CommonModel import session_deco
from utils import StaticValue as SV


@session_deco
def cal_principal():
    pass


@session_deco
def cal_agreement_principal(cal_date=date.today(), asset_name='浦发理财一号', **kwargs):
    session = kwargs[SV.SESSION_KEY]
    agreements = session.query(AssetClass).filter(AssetClass.type == SV.ASSET_CLASS_AGREEMENT_DEPOSIT,
                                                  AssetClass.name == asset_name)

    print(agreements[0])
    trades = []
    map(lambda x: map(lambda y: trades.append(y), x.asset_trade_list), agreements)
    return trades

    # return sum(list(map(lambda x: x, agreements)))


@session_deco
def agreement_daily_ret(cal_date=date.today(), **kwargs):
    session = kwargs[SV.SESSION_KEY]
    agreements = session.query(AssetClass).filter(AssetClass.type == SV.ASSET_CLASS_AGREEMENT_DEPOSIT)
    trades = []
    for agreement in agreements:
        trades += list(
            filter(lambda x: x.date >= cal_date and x.date < cal_date + timedelta(days=1), agreement.asset_trade_list))
    return trades


def fund_daily_ret(amount=0, ):
    pass


if __name__ == '__main__':
    print(cal_agreement_principal())
