# coding:utf8
"""

Author: ilcwd
"""
from ..models import (
    cart as _cart,
    good as _good,
    contact as _contact,
    objects,
)

from .dtos import HoShopDTO


def add_good(cartid, goodid):
    # TODO: check permission
    good = _good.get_good(goodid)
    ok = _cart.add_good(cartid, goodid, good.price) == 1

    if ok:
        return HoShopDTO(data='')

    return HoShopDTO(error='can not add good to cart')


def delete_good(cartid, goodid):
    # TODO: check permission
    ok = _cart.delete_good(cartid, goodid)
    if ok:
        return HoShopDTO(data='')

    return HoShopDTO(error='can not delete good from cart')


def create_cart(userid):
    cartid = _cart.create_cart(userid)
    return HoShopDTO(data={'cartid': cartid})


def get_cart(cartid):
    # TODO: check permission
    cart = _cart.get_cart(cartid)
    return HoShopDTO(data=objects.object_to_dict(cart))


def get_cart_details(cartid):
    # TODO: check permission
    cart = objects.object_to_dict(_cart.get_cart(cartid))

    goodlist = _cart.get_goodlist(cartid)
    cart['goodlist'] = []
    for g in goodlist:
        gdict = objects.object_to_dict(g)
        gdict['name'] = _good.get_good(g.goodid).name
        cart['goodlist'].append(gdict)

    return HoShopDTO(data=cart)


def submit_order(userid, cartid, contactid=None, address=None):
    cart = _cart.get_cart(cartid)

    if int(userid) != cart.userid:
        return HoShopDTO(error=u"无权限提交订单")

    if contactid:
        contact = _contact.get_contact(contactid)
    else:
        contactid = _contact.create_contact(userid, address=address)

    _cart.create_order(cartid, contactid)
    return HoShopDTO()


def _get_order_details(order):
    od = objects.object_to_dict(order)
    od['goodlist'] = []
    contact = objects.object_to_dict(_contact.get_contact(order.contactid))
    status = _cart.find_order_status(order.cartid)
    goodlist = _cart.get_goodlist(order.cartid)
    for g in goodlist:
        gdict = objects.object_to_dict(g)
        gdict['name'] = _good.get_good(g.goodid).name
        od['goodlist'].append(gdict)
    od['status'] = [objects.object_to_dict(i) for i in status]
    od['contact'] = contact
    return od


def list_orders(userid):
    orders = _cart.find_orders(userid)

    result = []
    for cart in orders:
        result.append(_get_order_details(cart))

    return HoShopDTO(data={'orders': result})


def sync_orders(cursor=None, limit=10, asc=False):
    # TODO: check permission
    if not cursor:
        cursor = None
    else:
        cursor = int(cursor)

    orders = _cart.find_orders_incrementally(cursor, limit, asc)
    result = {'orders': [_get_order_details(o) for o in orders]}
    if orders:
        forward_cursor = str(max(o.cartid for o in orders))
        backward_cursor = str(min(o.cartid for o in orders))
        result['forward_cursor'] = forward_cursor
        result['backward_cursor'] = backward_cursor

    return HoShopDTO(data=result)


