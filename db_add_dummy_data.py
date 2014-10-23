# coding:utf8
"""

Author: ilcwd
"""


import wsgiapp

from hoshop.models.db import Base, engine
from hoshop.models import good, catalog


def main():

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

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

if __name__ == '__main__':
    main()