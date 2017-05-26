# encoding:utf8


from __future__ import unicode_literals

import json
import os
from _datetime import datetime, date
from functools import wraps

from utils import StaticValue as SV

BASE_DIR = os.path.dirname(__file__)

FEE_CONFIG_FILE = os.path.join(BASE_DIR, '../fee.config')


def timer(func):
    import time
    @wraps(func)
    def _wrapper(*args, **kwargs):
        start_time = time.time()
        ret = func(*args, **kwargs)
        end_time = time.time()
        print(end_time - start_time, func.__name__, args, kwargs)
        return ret

    return _wrapper


def get_fee_config_dic(file_name=FEE_CONFIG_FILE):
    with open(file_name) as fp:
        return json.load(fp)


def get_value_by_key(dic=dict(), key=None):
    return dic.get(key)


def get_fund_value_by_key(dic=dict(), is_asset=True, key=None):
    return dic[is_asset][key]


def cash_key_to_type(key=None):
    return SV.CASH_KEY_TO_TYPE_DIC.get(key)


def cash_type_to_key(cash_type=1):
    return SV.CASH_TYPE_TO_KEY_DIC.get(cash_type)


def agreement_key_to_type(key=None):
    return SV.AGREEMENT_KEY_TO_TYPE_DIC.get(key)


def agreement_type_to_key(agreement_type=1):
    return SV.AGREEMENT_TYPE_TO_KEY_DIC.get(agreement_type)


def fund_key_to_type(is_asset=True, key=None):
    return get_fund_value_by_key(SV.FUND_KEY_TO_TYPE_DIC, is_asset, key)


def fund_type_to_key(is_asset=True, fund_type=None):
    return get_fund_value_by_key(SV.FUND_TYPE_TO_KEY_DIC, is_asset, fund_type)


def strToDate(dateStr=None):
    """
    yyyy-MM-dd parse to date(yyyy,MM,dd)
    :param dateStr: 
    :return: 
    """

    return datetime.strptime(dateStr, '%Y-%m-%d').date() if dateStr else date.today()
    # dateArr = dateStr.split('-')
    # d = datetime.date.today()
    # if dateArr is not None:
    #     date = datetime.date(d.year, d.month, d.day)
    # else:
    #     date = datetime.date(int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", dateArr[0])),
    #                          int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", dateArr[1])),
    #                          int(re.sub(r"\b0*([1-9][0-9]*|0)", r"\1", dateArr[2])))
    # return date


if __name__ == '__main__':
    # print(get_value_by_key(CASH_TYPE_TO_KEY_DIC, 5))
    dateStr = '2017-05-25'
    print(type(strToDate(dateStr)))
