# coding:utf8
"""

Author: ilcwd
"""
import flask

from ..services import cart
from . import util


app = flask.Blueprint('ajax.admin', __name__)


@app.route('/order/update', methods=['GET', 'POST'])
def update_orders():
    userid = flask.session['userid']
    orderid = flask.request.form['orderid']
    status = flask.request.form['status']
    comment = flask.request.form.get('comment')
    r = cart.update_order(userid, orderid, status, comment)

    return util.render_dto(r)