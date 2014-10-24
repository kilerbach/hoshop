# coding:utf8
"""

Author: ilcwd
"""
import traceback
import logging
import uuid

from flask import jsonify, request, session, render_template

from hoshop.core import application, C
from hoshop.models import db
from hoshop.services import cart as cartService

_logger = logging.getLogger(__name__)


CSRF_TOKEN_KEY = '_csrf_token_'
SESSION_CARTID = 'cartid'
SESSION_USERID = 'userid'



# @application.teardown_appcontext
# def shutdown_db_session(exception=None):
#     db.DBSession.remove()

@application.before_request
def check_session():
    userid = session.get(SESSION_USERID)
    if not userid:
        userid = 0
        session[SESSION_USERID] = userid

    if not session.get(SESSION_CARTID):
        r = cartService.create_cart(userid)
        session[SESSION_CARTID] = r.data['cartid']


@application.errorhandler(500)
def error_handler(ex):
    _logger.error("Exception <%s>, Traceback: %s", str(ex), traceback.format_exc())
    return jsonify({'error_text': u"服务器错误"}), 500


@application.errorhandler(400)
def handle_400(ex):
    return jsonify({'error_text': u"参数错误"}), 400


@application.errorhandler(404)
def handle_404(ex):
    return jsonify({'error_text': u"没有找到该网页"}), 404


def render_error_page(msg, code=200):
    return render_template('error.html', msg=msg), code


@application.before_request
def csrf_protect():
    if request.method == "POST":
        session_token = session.get(CSRF_TOKEN_KEY)
        form_token = request.form.get(CSRF_TOKEN_KEY)

        if not session_token or session_token != form_token:
            return render_error_page(u'跨站错误')


def generate_csrf_token():
    if CSRF_TOKEN_KEY not in session:
        session[CSRF_TOKEN_KEY] = uuid.uuid4().hex
    return session[CSRF_TOKEN_KEY]


application.jinja_env.globals['csrf_token'] = generate_csrf_token
