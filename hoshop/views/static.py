# coding:utf8
"""

Author: ilcwd
"""

import flask

from ..biz import workinghour
from ..services import shop, cart
from ..core import C
from .default import require_admin

app = flask.Blueprint('static', __name__, static_folder=C.PHOTO_DIR)


@app.route('/<path:name>')
def serve_static(name):
    return app.send_static_file(name)