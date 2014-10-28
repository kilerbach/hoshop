# coding:utf8
"""

Author: ilcwd
"""
from flask_sqlalchemy import SQLAlchemy

from hoshop.core import C, application

db = SQLAlchemy(application)
application.config['SQLALCHEMY_DATABASE_URI'] = C.DB_FILE
application.config['SQLALCHEMY_ECHO'] = C.DEBUG
application.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

Base = db.Model


def get_session():
    return db.session