# coding:utf8
"""

Author: ilcwd
"""
import datetime

from . import _db
from ._objects import Good, now

from hoshop.core import contants

CATALOG_ROOT = 0


def _set_date(d, default):
    if not d:
        d = default

    if isinstance(d, (datetime.datetime, datetime.date)):
        return d

    return datetime.datetime.strptime(d, '%Y-%m-%d')


def update_good(goodid, **kw):
    sess = _db.get_session()
    good = sess.query(Good).filter(Good.goodid==goodid).one()
    for k, v in kw.iteritems():
        if k in contants.GOOD_EDITABLE_COLUMNS:
            if k == 'count_left':
                setattr(good, 'count_total', good.count_sold+int(v))
            if k == 'count_sold_delta':
                # not enough goods
                if good.count_sold + int(v) > good.count_total:
                    return 0

                setattr(good, 'count_sold', good.count_sold+int(v))
            else:
                setattr(good, k, v)

    sess.add(good)
    return 1


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
    return sess.query(Good).filter(Good.expired_time>now()).filter(Good.count_sold<Good.count_total).all()


def get_good(goodid):
    sess = _db.get_session()
    return sess.query(Good).filter(Good.goodid == goodid).one()