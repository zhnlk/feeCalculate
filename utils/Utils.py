# encoding:utf8


from __future__ import unicode_literals

from functools import wraps


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
