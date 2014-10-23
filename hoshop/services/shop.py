# coding:utf8
"""

Author: ilcwd
"""
from ..models import (
    catalog as _catalog,
    good as _good,
    contact as _contact,
)

from .dtos import HoShopDTO


def find_catalogs():
    return HoShopDTO(data=dict(
        catalogs=_catalog.find_catalogs(),
    ))


def create_catalog(name):
    if _catalog.create_catalog(name) == 1:
        return HoShopDTO(data='')

    return HoShopDTO(error='create catalog fail')


def show_goods():
    catalogs = _catalog.find_catalogs()
    goods = _good.find_goods()

    return HoShopDTO(data=dict(
        catalogs=catalogs,
        goods=goods,
    ))


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


def get_primary_contact(userid):
    cs = _contact.find_contacts(userid)
    for i in cs:
        if i.is_primary:
            return HoShopDTO(data=i)
    return HoShopDTO(error="not found")


def create_good(name, price, catalog, total=99999999, description='', start_time=None, expired_time=None):
    price = encode_price(price)
    c = _catalog.get_or_create_catalog(catalog)
    rows = _good.create_good(name, price, c.catalogid, total, description, start_time, expired_time)

    if rows == 1:
        return HoShopDTO(data='')

    return HoShopDTO(error='create good fail')