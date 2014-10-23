# coding:utf8
"""

Author: ilcwd
"""


import wsgiapp

from hoshop.models.db import Base, engine
from hoshop.models import good, catalog, cart
from hoshop.models.objects import object_to_dict


def main():
    # print cart.create_cart(1)
    # print cart.create_cart(2)
    # print cart.add_good(1, 1, 10000)

    # print cart.get_cart(1).bill

    # print cart.delete_good(1, 1)
    # print object_to_dict(cart.get_cart(1))
    #
    # print object_to_dict(cart.get_cart(48))
    # print cart.create_cart(0)
    for i in cart.find_orders(0):
        print object_to_dict(i)


if __name__ == '__main__':
    main()