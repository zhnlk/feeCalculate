# encoding:utf8


from __future__ import unicode_literals

import json
import os
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
