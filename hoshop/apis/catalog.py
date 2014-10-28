# coding:utf8
"""

Author: ilcwd
"""
import flask

from ..services import shop
from . import _util


app = flask.Blueprint('ajax.catalog', __name__)


@app.route('/catalog/creation', methods=['POST'])
def create_catalog():
    name = flask.request.form['name']
    ok = shop.create_catalog(name)
    if ok:
        return _util.render_data()

    return _util.render_error(u"创建失败")


