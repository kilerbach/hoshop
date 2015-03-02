# coding:utf8
"""

Author: ilcwd
"""
import flask

from ..services import cart, shop
from ..views import default
from . import _util


app = flask.Blueprint('ajax.admin', __name__)


@app.route('/order/update', methods=['POST'])
@default.require_admin
def update_order():
    userid = flask.session['userid']
    orderid = flask.request.form['orderid']
    status = flask.request.form['status']
    comment = flask.request.form.get('comment')
    r = cart.update_order(userid, orderid, status, comment)

    return _util.render_dto(r)


@app.route('/good/update', methods=['POST'])
@default.require_admin
def update_good():
    goodid = flask.request.form['goodid']
    key = flask.request.form['key']
    value = flask.request.form['value']
    r = shop.update_goods(goodid, **{key: value})
    return _util.render_dto(r)


@app.route('/category/addition', methods=['POST'])
@default.require_admin
def add_new_category():
    name = flask.request.form['name']
    r = shop.create_catalog(name)
    return _util.render_dto(r)


@app.route('/good/uploadphoto', methods=['POST'])
@default.require_admin
def upload_photo():

    photo_names = []
    for i in xrange(100):
        photo_fs = flask.request.files.get('photo-file-%d' % i)
        if not photo_fs:
            break

        name = shop.save_photo(photo_fs.filename, photo_fs.stream)
        photo_names.append(name)
        photo_fs.close()

    return _util.render_data({'photos': photo_names})