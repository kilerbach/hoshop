# coding:utf8
"""

Author: ilcwd
"""
from . import db
from .objects import Cart, CartList, OrderStatus, now


def create_cart(userid):
    cart = Cart(userid=userid, is_commit=False, bill=0, count=0,
                status=Cart.STATUS.UNSET, contactid=0)
    sess = db.DBSession()
    sess.add(cart)
    sess.commit()
    return cart.cartid


def get_cart(cartid):
    sess = db.DBSession()
    return sess.query(Cart).filter(Cart.cartid == cartid).one()


def get_goodlist(cartid):
    sess = db.DBSession()
    return sess.query(CartList).filter(CartList.cartid == cartid).all()


def delete_good(cartid, goodid):
    sess = db.DBSession()

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

    sess.commit()
    return 1


def add_good(cartid, goodid, price, discount=100, comment=''):
    sess = db.DBSession()

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

    sess.commit()
    return 1


def create_order(cartid, contactid):
    if not contactid:
        return 0

    sess = db.DBSession()
    cart = sess.query(Cart).filter(Cart.cartid == cartid).one()
    if cart.is_commit:
        return 0

    orderstatus = OrderStatus(orderid=cartid, modified_userid=cart.userid,
                              to_status=Cart.STATUS.START, from_status=cart.status,
                              comment='')

    cart.contactid = contactid
    cart.is_commit = True
    cart.status = Cart.STATUS.START
    cart.modified_time = now()
    sess.add(cart)
    sess.add(orderstatus)
    sess.commit()
    return cart


def update_order_status(orderid, to_status, userid, comment):
    sess = db.DBSession()
    order = sess.query(Cart).filter(Cart.cartid == orderid).one()
    if not order.is_commit:
        return 0

    orderstatus = OrderStatus(orderid=orderid, modified_user=userid,
                              to_status=to_status, from_status=order.status,
                              comment=comment)
    order.status = to_status
    order.modified_time = now()
    sess.add(order)
    sess.add(orderstatus)
    sess.commit()
    return 1


def find_orders(userid):
    sess = db.DBSession()
    carts = sess.query(Cart).filter(Cart.userid == userid).filter(Cart.is_commit == True).all()
    return carts


def find_order_status(orderid):
    sess = db.DBSession()
    return sess.query(OrderStatus).filter(OrderStatus.orderid == orderid).all()


def find_orders_incrementally(orderid=None, limit=10, asc=True):
    if orderid is None:
        if asc:
            orderid = 0
        else:
            orderid = 0xFFFFFFFF

    sess = db.DBSession()
    if asc:
        orders = sess.query(Cart).filter(Cart.cartid > orderid).filter(Cart.is_commit == True).limit(limit).all()
    else:
        orders = sess.query(Cart).filter(Cart.cartid < orderid).filter(Cart.is_commit == True).limit(limit).all()

    return orders


