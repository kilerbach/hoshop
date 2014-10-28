#coding:utf8
"""

Global objects collection.

@author: ilcwd
"""
import logging
import json

import flask

from .exceptions import *
from .misc import get_template_path, TEMPLATE_ROOT, STATIC_ROOT

# Main application
print "##", STATIC_ROOT
application = flask.Flask(__name__, static_folder=STATIC_ROOT)

# logger for RPC time cost.
spy_logger = logging.getLogger('hoshop.spy')
# logger for request/response (if need).
request_logger = logging.getLogger('hoshop.request')


class C(object):
    """
    Global configuration for application.
    """

    # Define your attributes here first.
    DEBUG = False

    DB_FILE = None

    SERVER_SESSION_KEY = None

    SERVER_PASSWORD_KEY = None

    @classmethod
    def load_config(cls, config_file):
        with open(config_file, 'r') as f:
            content = json.loads(f.read())

        for k, v in cls.__dict__.iteritems():
            if k.startswith('_') or k == 'load_config':
                continue

            setattr(cls, k, content[k])