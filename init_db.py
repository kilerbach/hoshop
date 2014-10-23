# coding:utf8
"""

Author: ilcwd
"""


import wsgiapp

from hoshop.models.db import Base, engine


def main():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()