# encoding:utf8


from __future__ import unicode_literals

import json
import os
from _datetime import datetime, date
from functools import wraps

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
