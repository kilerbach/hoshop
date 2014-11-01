# coding:utf8
"""

Author: ilcwd
"""
import sqlalchemy.exc

from . import _db
from ._objects import Catalog

CATALOG_ROOT = 0


def create_catalog(name):
    catalog = Catalog(name=name, parentid=CATALOG_ROOT)

    sess = _db.get_session()
    sess.add(catalog)
    try:
        sess.flush()
    except sqlalchemy.exc.IntegrityError:
        sess.rollback()
        return None

    return catalog


def get_catalog(catalogid):
    return _db.get_session().query(Catalog).filter(Catalog.catalogid==catalogid).one()


def get_or_create_catalog(name):
    sess = _db.get_session()
    cs = sess.query(Catalog).filter(Catalog.name == name).all()
    if not cs:
        catalog = Catalog(name=name, parentid=CATALOG_ROOT)
        sess.add(catalog)
        sess.flush()
        c = sess.query(Catalog).filter(Catalog.name == name).one()
        return c

    return cs[0]


def delete_catalog(catalogid):
    return _db.get_session().query(Catalog).filter(Catalog.catalogid == catalogid).delete()


def find_catalogs():
    sess = _db.get_session()
    return sess.query(Catalog).all()

