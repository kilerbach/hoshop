# coding:utf8
"""

Author: ilcwd
"""
from . import _db
from ._objects import Cart, CartList, OrderStatus, now
from hoshop.core import (
    misc,
    spy_logger,
    contants,
)


@misc.log_costtime(spy_logger)
def create_cart(userid):
    cart = Cart(userid=userid, is_commit=False, bill=0, count=0,
                status=contants.ORDER_STATUS.UNSET, contactid=0)
    sess = _db.get_session()
    sess.add(cart)
    sess.flush()
    return cart.cartid


@misc.log_costtime(spy_logger)
def get_cart(cartid):
    sess = _db.get_session()
    cart = sess.query(Cart).filter(Cart.cartid == cartid).all()
    if cart:
        return cart[0]

    return None


@misc.log_costtime(spy_logger)
def get_goodlist(cartid):
    sess = _db.get_session()
    return sess.query(CartList).filter(CartList.cartid == cartid).all()


@misc.log_costtime(spy_logger)
def delete_good(cartid, goodid):
    sess = _db.get_session()

    cart = sess.query(Cart).filter(Cart.cartid == cartid).filter(Cart.is_commit == False).one()

    goodlist = sess.query(CartList).filter(CartList.cartid == cartid)\
        .filter(CartList.goodid == goodid).all()

    if not goodlist:
        return 0

    goodlist = goodlist[0]
    if goodlist.count < 1:
        return 0

    goodlist.count -= 1
    sess.add(goodlist)

    cart.count -= 1
    cart.bill -= goodlist.price
    sess.add(cart)

    sess.flush()
    return 1


@misc.log_costtime(spy_logger)
def add_good(cartid, goodid, price, discount=100, comment=''):
    sess = _db.get_session()

    cart = sess.query(Cart).filter(Cart.cartid == cartid).filter(Cart.is_commit == False).one()

    goodlist = sess.query(CartList).filter(CartList.cartid == cartid)\
        .filter(CartList.goodid == goodid).all()

    if not goodlist:
        cartlist = CartList(cartid=cartid, goodid=goodid,
                            discount=discount, price=price, comment=comment, count=1)
        sess.add(cartlist)
    else:
        goodlist = goodlist[0]
        goodlist.count += 1
        sess.add(goodlist)

    cart.count += 1
    cart.bill += price
    sess.add(cart)

    sess.flush()
    return 1


@misc.log_costtime(spy_logger)
def create_order(cartid, contactid):
    if not contactid:
        return 0

    sess = _db.get_session()
    cart = sess.query(Cart).filter(Cart.cartid == cartid).one()
    if cart.is_commit:
        return 0

    orderstatus = OrderStatus(orderid=cartid, modified_userid=cart.userid,
                              to_status=contants.ORDER_STATUS.START, from_status=cart.status,
                              comment='')

    cart.contactid = contactid
    cart.is_commit = True
    cart.status = contants.ORDER_STATUS.START
    cart.modified_time = now()
    sess.add(cart)
    sess.add(orderstatus)
    sess.flush()
    return cart


@misc.log_costtime(spy_logger)
def update_order_status(orderid, from_status, to_status, userid, comment):
    if contants.ORDER_STATUS.has_value(to_status):
        return 0

    sess = _db.get_session()
    order = sess.query(Cart).filter(Cart.cartid == orderid).one()
    if not order.is_commit:
        return 0

    orderstatus = OrderStatus(orderid=orderid, modified_userid=userid,
                              to_status=to_status, from_status=order.status,
                              comment=comment)
    order.status = to_status
    order.modified_time = now()
    sess.add(order)
    sess.add(orderstatus)
    sess.flush()
    return 1


@misc.log_costtime(spy_logger)
def find_orders(userid):
    sess = _db.get_session()
    carts = sess.query(Cart).filter(Cart.userid == userid).filter(Cart.is_commit == True).all()
    return carts


@misc.log_costtime(spy_logger)
def find_order_status(orderid):
    sess = _db.get_session()
    return sess.query(OrderStatus).filter(OrderStatus.orderid == orderid).all()


@misc.log_costtime(spy_logger)
def find_orders_incrementally(orderid=None, limit=10, asc=True):
    if orderid is None:
        if asc:
            orderid = 0
        else:
            orderid = 0xFFFFFFFF

    sess = _db.get_session()
    if asc:
        orders = sess.query(Cart).filter(Cart.cartid > orderid).filter(Cart.is_commit == True).limit(limit).all()
    else:
        orders = sess.query(Cart).filter(Cart.cartid < orderid).filter(Cart.is_commit == True).limit(limit).all()

    return orders


