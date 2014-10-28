# coding:utf8
"""

Author: ilcwd
"""
import hashlib

import wsgiapp

from hoshop.models._db import db
from hoshop.models import _objects
from hoshop.models import good, catalog, user


def main():
    def h(p):
        return hashlib.sha256(str(p)).digest()

    db.drop_all()
    db.create_all()

    catalog.create_catalog(u"饮品")
    catalog.create_catalog(u"烟类")
    catalog.create_catalog(u"泡面")
    catalog.create_catalog(u"零食")

    good.create_good(u"可乐350ml", 3500, 1)
    good.create_good(u"雪碧350ml", 3000, 1)

    good.create_good(u"黑曼", 10000, 2)
    good.create_good(u"芙蓉王", 12000, 2)

    good.create_good(u"康师傅", 2000, 3)
    good.create_good(u"出前一丁", 2500, 3)

    good.create_good(u"威化饼", 5500, 4)

    user.create_user(_objects.UserLogin.LOGINTYPE.NAME, 'admin', h('111111'), role=_objects.User.ROLE.ADMIN)
    user.create_user(_objects.UserLogin.LOGINTYPE.NAME, 'test', h('111111'), role=_objects.User.ROLE.NORMAL)

    db.session.commit()

if __name__ == '__main__':
    main()