# coding:utf8
"""

Author: ilcwd
"""

from . import db
from .objects import Catalog

CATALOG_ROOT = 0


def create_catalog(name):
    catalog = Catalog(name=name, parentid=CATALOG_ROOT)

    with db.create_session() as sess:
        sess.add(catalog)

    return 1


def get_or_create_catalog(name):
    sess = db.DBSession()
    cs = sess.query(Catalog).filter(Catalog.name == name).all()
    if not cs:
        catalog = Catalog(name=name, parentid=CATALOG_ROOT)
        sess.add(catalog)
        sess.commit()
        c = sess.query(Catalog).filter(Catalog.name == name).one()

        return c

    return cs[0]


def delete_catalog(catalogid):
    with db.create_session() as sess:
        return sess.query(Catalog).filter(Catalog.catalogid == catalogid).delete()


def find_catalogs():
    sess = db.DBSession()
    return sess.query(Catalog).all()

