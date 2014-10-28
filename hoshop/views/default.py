# coding:utf8
"""

Author: ilcwd
"""
import traceback
import logging
import uuid
import functools

import flask
from flask import jsonify, request, session, render_template

from hoshop.core import application, contants
from hoshop.services import cart as cartService

_logger = logging.getLogger(__name__)


CSRF_TOKEN_KEY = '_csrf_token_'
SESSION_CARTID = 'cartid'
SESSION_USERID = 'userid'
SESSION_USERROLE = 'user.role'

@application.context_processor
def inject_values():
    return dict(
        order_status_mapping=contants.ORDER_STATUS_MAPPING,
        user_role=contants.USER_ROLE,
    )


def require_user(func):
    @functools.wraps(func)
    def go(*a, **kw):
        userid = session.get(SESSION_USERID)
        if not userid:
            return flask.redirect(flask.url_for('user.login', next=request.url))

        return func(*a, **kw)

    return go


def require_admin(func):
    @functools.wraps(func)
    def go(*a, **kw):
        userid = session.get(SESSION_USERID)
        if not userid or session.get(SESSION_USERROLE) != contants.USER_ROLE.ADMIN:
            # TODO: admin require prompt
            return flask.redirect(flask.url_for('user.login', next=request.url))

        return func(*a, **kw)

    return go


def require_cart(func):
    @functools.wraps(func)
    def go(*a, **kw):
        userid = session.get(SESSION_USERID)
        if not userid:
            return flask.redirect(flask.url_for('user.login', next=request.url))

        cartid = session.get(SESSION_CARTID)
        if cartid:
            r = cartService.get_cart(userid, cartid)
            if not r.ok() or r.data['is_commit']:
                cartid = None

        if not cartid:
            r = cartService.create_cart(userid)
            session[SESSION_CARTID] = r.data['cartid']

        return func(*a, **kw)

    return go


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
