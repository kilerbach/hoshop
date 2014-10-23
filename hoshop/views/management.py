# coding:utf8
"""

Author: ilcwd
"""

import flask

from ..services import shop, cart
from ..models import objects
from ..core import TEMPLATE_ROOT

app = flask.Blueprint('management', __name__, template_folder=TEMPLATE_ROOT)


@app.context_processor
def inject_values():
    return dict(
        order_status_mapping=objects.Cart.STATUS.MAPPING,
    )


@app.route('/good/addition', methods=['GET'])
def add_good_view():
    r = shop.find_catalogs()
    return flask.render_template('management/add_good.html',
                                 catalogs=r.data['catalogs'])


@app.route('/good/addition', methods=['POST'])
def add_good_do():
    args = flask.request.form
    name = args['name']
    price = args['price']
    catalog = args['catalog']
    description = args['description']
    total = args['total']

    r = shop.create_good(name, price, catalog, total, description)
    if r.ok():
        pass

    return flask.redirect('/good/')


@app.route('/order/', methods=['GET', 'POST'])
def list_orders():
    r = cart.sync_orders(limit=10)
    return flask.render_template('management/orders.html',
                                 orders=r.data['orders'],
                                 forward_cursor=r.data.get('forward_cursor', ''))
