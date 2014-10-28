# coding:utf8
"""

Author: ilcwd
"""
import datetime

from . import _db
from ._objects import Good

CATALOG_ROOT = 0


def _set_date(d, default):
    if not d:
        d = default

    if isinstance(d, (datetime.datetime, datetime.date)):
        return d

    return datetime.datetime.strptime(d, '%Y-%m-%d')


def create_good(name, price, catalogid, total=99999999, description='', start_time=None, expired_time=None):
    start_time = _set_date(start_time, '2000-1-1')
    expired_time = _set_date(expired_time, '2099-1-1')

    good = Good(
        name=name,
        price=price,
        catalogid=catalogid,
        count_total=total,
        count_sold=0,
        description=description,
        start_time=start_time,
        expired_time=expired_time,
    )

    _db.get_session().add(good)

    return 1


def find_goods():
    sess = _db.get_session()
    return sess.query(Good).all()


def get_good(goodid):
    sess = _db.get_session()
    return sess.query(Good).filter(Good.goodid == goodid).one()