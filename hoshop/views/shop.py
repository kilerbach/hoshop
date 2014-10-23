# coding:utf8
"""

Author: ilcwd
"""
import flask

from ..services import shop
from ..services import cart
from ..core import TEMPLATE_ROOT
from ..models import objects

app = flask.Blueprint('shop', __name__, template_folder=TEMPLATE_ROOT)


@app.context_processor
def inject_values():
    return dict(
        order_status_mapping=objects.Cart.STATUS.MAPPING,
    )


@app.route('/catalog/')
def list_catalog():
    r = shop.find_catalogs()
    return flask.render_template('management/catalogs.html', catalogs=r.data['catalogs'])


@app.route('/good/')
def show_goods():
    r = shop.show_goods()
    return flask.render_template('shop/goods.html',
                                 catalogs=r.data['catalogs'], goods=r.data['goods'])


@app.route('/cart/')
def show_cart():
    userid = flask.session['userid']
    cartid = flask.session['cartid']
    r = cart.get_cart_details(cartid)
    c = shop.get_primary_contact(userid)
    if c.ok():
        c = c.data
    else:
        c = None

    return flask.render_template("shop/cart.html", cart=r.data, contact=c)


@app.route('/order/')
def list_orders():
    userid = flask.session['userid']
    r = cart.list_orders(userid)
    print r.data
    return flask.render_template("shop/orders.html", orders=r.data['orders'])


@app.route('/order/submit', methods=['POST'])
def submit_order():
    cartid = flask.session['cartid']
    userid = flask.session['userid']
    # TODO: avoid modify cart in other views

    address = flask.request.form.get('address')
    contactid = flask.request.form.get('contactid')

    r = cart.submit_order(userid, cartid, contactid, address)
    if r.ok():
        flask.session.pop('cartid')

    return flask.redirect(flask.url_for('shop.list_orders'))


@app.route('/cart/deletion/good', methods=['POST'])
def delete_good_from_cart():

    cartid = flask.request.form['cartid']
    goodid = flask.request.form['goodid']

    cart.delete_good(cartid, goodid)
    return flask.redirect(flask.url_for('shop.show_cart'))