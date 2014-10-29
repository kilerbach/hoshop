# coding:utf8
"""

Author: ilcwd
"""
import flask

from ..services import shop
from ..services import cart
from ..core import TEMPLATE_ROOT
from .default import require_user, require_cart

app = flask.Blueprint('shop', __name__, template_folder=TEMPLATE_ROOT)


@app.route('/')
@app.route('/good/')
@require_cart
def list_goods():
    r = shop.show_goods()
    return flask.render_template('shop/goods.html',
                                 catalogs=r.data['catalogs'], goods=r.data['goods'])


@app.route('/cart/')
@require_cart
def get_cart():
    userid = flask.session['userid']
    cartid = flask.session['cartid']
    r = cart.get_cart_details(userid, cartid)
    cs = shop.find_contacts(userid)

    error = flask.request.values.get('error', '')

    return flask.render_template("shop/cart.html", cart=r.data,
                                 contacts=cs.data['contacts'],
                                 default_contact=cs.data['default'],
                                 error=error)


@app.route('/order/')
@require_cart
def list_orders():
    userid = flask.session['userid']
    r = cart.list_orders(userid)
    return flask.render_template("shop/orders.html", orders=r.data['orders'])


@app.route('/order/submit', methods=['POST'])
def submit_order():
    cartid = flask.session['cartid']
    userid = flask.session['userid']
    # TODO: avoid modify cart in other views

    address = flask.request.form.get('address')
    setdefault = flask.request.form['setdefault'].lower() == 'on'

    r = cart.submit_order(userid, cartid, address, setdefault)
    if r.ok():
        flask.session.pop('cartid')
    else:
        return flask.redirect(flask.url_for('shop.get_cart', error=r.error))

    return flask.redirect(flask.url_for('shop.list_orders'))


@app.route('/cart/deletion/good', methods=['POST'])
@require_cart
def delete_good_from_cart():
    userid = flask.session['userid']
    cartid = flask.request.form['cartid']
    goodid = flask.request.form['goodid']

    cart.delete_good(userid, cartid, goodid)
    return flask.redirect(flask.url_for('shop.get_cart'))