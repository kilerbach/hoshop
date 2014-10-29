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


def update_goods(goodid, **kw):
    if 'price' in kw:
        kw['price'] = encode_price(int(kw.pop('price')))

    if _good.update_good(goodid, **kw):
        return HoShopDTO()

    return HoShopDTO(error=u'更新商品失败')


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
    c = _contact.get_default_contact(userid)
    if c:
        return HoShopDTO(data=c)
    return HoShopDTO(error="not found")


def set_primary_contact(userid, contactid):
    c = _contact.get_contact(contactid)
    if not c:
        return HoShopDTO(error="contact not found")

    ok = _contact.set_default_contact(userid, contactid) == 1
    if ok:
        return HoShopDTO()

    return HoShopDTO(error="set primary contact fail")


def find_contacts(userid):
    cs = _contact.find_contacts(userid)
    r = {'contacts': cs, 'default': None}
    if cs:
        r['default'] = _contact.get_default_contact(userid)
    return HoShopDTO(data=r)


def delete_contact(userid, contactid):
    if _contact.delete_contact(userid, contactid):
        return HoShopDTO()

    return HoShopDTO(error='delete contact fail')


def set_primary_contact(userid, contactid):
    if _contact.set_default_contact(userid, contactid):
        return HoShopDTO()

    return HoShopDTO(error='update contact fail')


def create_good(name, price, catalog, total=99999999, description='', start_time=None, expired_time=None):
    price = encode_price(price)
    c = _catalog.get_or_create_catalog(catalog)
    rows = _good.create_good(name, price, c.catalogid, total, description, start_time, expired_time)

    if rows == 1:
        return HoShopDTO(data='')

    return HoShopDTO(error='create good fail')