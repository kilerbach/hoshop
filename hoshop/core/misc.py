# coding:utf8
"""

Author: ilcwd
"""
import inspect
import time
import functools
import os

import arrow

__root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

TEMPLATE_ROOT = os.path.join(__root, 'templates')

STATIC_ROOT = os.path.join(__root, 'static')


def get_template_path(name):
    return os.path.join(TEMPLATE_ROOT, name)


def log_costtime(logger):
    def _d(func):
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        funcname = mod.__name__ + '.' + func.__name__

        @functools.wraps(func)
        def wrapper(*a, **kw):
            st = time.time()
            try:
                return func(*a, **kw)
            finally:
                ct = time.time() - st
                logger.info("%s - %dms", funcname, int(ct))

        return wrapper
    return _d


class DatetimeFormatter(object):

    def __init__(self, tz):
        self.tz = tz

    def _to_local_time(self, d):
        return arrow.get(d).to(self.tz)

    def precise_datetime(self, d):
        return self._to_local_time(d).strftime("%Y-%m-%d %H:%M")

    def only_time(self, d):
        return self._to_local_time(d).strftime("%H:%M")


def encode_price(price):
    """
    存储中价格是精确到厘的
    """
    idx = price.find('.')
    if idx < 0:
        return int(price) * 1000

    tailing = price[idx+1:]
    if len(tailing) < 3:
        tailing += '0' * (3-len(tailing))

    return int(price[:idx]) * 1000 + int(tailing[:3])


def decode_price(price):
    price = int(price)
    if not price:
        return '0'

    r = ''
    for i in xrange(3):
        if not price:
            break

        r = str(price % 10) + r
        price /= 10

    r = r.rstrip('0')
    if not r:
        return str(price)

    return str(price) + '.' + r