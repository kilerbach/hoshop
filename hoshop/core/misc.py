# coding:utf8
"""

Author: ilcwd
"""
import inspect
import time
import functools
import os

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