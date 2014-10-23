# coding:utf8
"""

Author: ilcwd
"""
import flask

from ..services import cart
from . import util


app = flask.Blueprint('ajax.cart', __name__)


@app.route('/cart/creation', methods=['GET', 'POST'])
def create_cart():
    r = cart.create_cart(0)
    if r.ok():
        return util.render_data(r.data)

    return util.render_error(u"创建购物车失败")


@app.route('/cart', methods=['GET', 'POST'])
def get_cart():
    cartid = flask.session['cartid']
    r = cart.get_cart(cartid)
    if r.ok():
        return util.render_data(r.data)

    return util.render_error(u"找不到购物车")


@app.route('/cart/addgood', methods=['GET', 'POST'])
def add_good_to_cart():
    cartid = flask.session['cartid']
    goodid = flask.request.form['goodid']
    r = cart.add_good(cartid, goodid)
    if r.ok():
        return util.render_data(r.data)

    return util.render_error(r.error)


@app.route('/order/sync', methods=['POST'])
def sync_orders():
    cursor = flask.request.form.get('cursor')
    limit = int(flask.request.form['limit'])
    asc = int(flask.request.form.get('asc'))
    r = cart.sync_orders(cursor, limit, asc)
    if r.ok():
        return util.render_data(r.data)

    return util.render_error(r.error)
