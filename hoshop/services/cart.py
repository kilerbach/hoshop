# coding:utf8
"""

Author: ilcwd
"""
from ..models import (
    cart as _cart,
    good as _good,
    contact as _contact,
    _db,
)
from ..biz import workinghour

from .dtos import HoShopDTO


def _validate_cart_op(userid, cartid):
    cart = _cart.get_cart(cartid)
    if not cart:
        return None, HoShopDTO(error='cart not found')

    if int(userid) != cart.userid:
        return None, HoShopDTO(error='forbidden')

    return cart, None


def add_good(userid, cartid, goodid):
    good = _good.get_good(goodid)

    cart, err = _validate_cart_op(userid, cartid)
    if err:
        return err

    ok = _cart.add_good(cartid, goodid, good.price) == 1
    if ok:
        return HoShopDTO()

    return HoShopDTO(error=u'库存不足')


def delete_good(userid, cartid, goodid):
    cart, err = _validate_cart_op(userid, cartid)
    if err:
        return err

    ok = _cart.delete_good(cartid, goodid)
    if ok:
        return HoShopDTO(data='')

    return HoShopDTO(error='can not delete good from cart')


def create_cart(userid):
    cartid = _cart.create_cart(userid)
    return HoShopDTO(data={'cartid': cartid})


def get_cart(userid, cartid):
    cart, err = _validate_cart_op(userid, cartid)
    if err:
        return err

    if cart:
        return HoShopDTO(data=cart.dictify())
    return HoShopDTO(error='no cart')


def get_cart_details(userid, cartid):
    cart, err = _validate_cart_op(userid, cartid)
    if err:
        return err

    cart = cart.dictify()

    goodlist = _cart.get_goodlist(cartid)
    cart['goodlist'] = []
    for g in goodlist:
        gdict = g.dictify()
        gdict['name'] = _good.get_good(g.goodid).name
        cart['goodlist'].append(gdict)

    return HoShopDTO(data=cart)


def submit_order(userid, cartid, address=None, set_default=False):
    rest_time = workinghour.is_rest_time()
    if rest_time:
        return HoShopDTO(error=rest_time)

    cart = _cart.get_cart(cartid)

    if int(userid) != cart.userid:
        return HoShopDTO(error=u"无权限提交订单")

    if cart.count<=0:
        return HoShopDTO(error=u"还没选择商品")

    contactid = _contact.create_contact(userid, address=address)
    if set_default:
        _contact.set_default_contact(userid, contactid)

    _cart.create_order(cartid, contactid)
    goodlist = _cart.get_goodlist(cartid)
    for g in goodlist:
        if not _good.update_good(g.goodid, count_sold_delta=g.count):
            _db.get_session().rollback()
            good = _good.get_good(g.goodid)
            return HoShopDTO(error=u'商品“%s”库存不足' % good.name)
    # TODO: update goods
    return HoShopDTO()


def _get_order_details(order):
    od = order.dictify()
    od['goodlist'] = []
    contact = _contact.get_contact(order.contactid).dictify()
    status = _cart.find_order_status(order.cartid)
    goodlist = _cart.get_goodlist(order.cartid)
    for g in goodlist:
        gdict = g.dictify()
        gdict['name'] = _good.get_good(g.goodid).name
        od['goodlist'].append(gdict)
    od['current_status'] = od.pop('status')
    od['status'] = [i.dictify() for i in status]
    od['contact'] = contact
    return od


def list_orders(userid):
    orders = _cart.find_orders(userid)

    result = []
    for cart in orders:
        result.append(_get_order_details(cart))

    return HoShopDTO(data={'orders': result})


def sync_orders(cursor=None, limit=10, asc=False):
    # admin only

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

    latest_order = _cart.find_orders_incrementally(None, 1, False)
    if latest_order:
        latest_order = latest_order[0]
        latest_cursor = str(latest_order.cartid)
        result['latest_cursor'] = latest_cursor
    else:
        result['latest_cursor'] = 0

    return HoShopDTO(data=result)


def update_order(userid, orderid, status, comment):
    # admin only


    status = int(status)
    ok = _cart.update_order_status(orderid, status, userid, comment) == 1
    if ok:
        return HoShopDTO()

    return HoShopDTO(error=u'更新订单失败')

