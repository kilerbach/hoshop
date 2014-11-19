# coding:utf8
"""

Author: ilcwd
"""


import wsgiapp

from hoshop.models._db import  db


def main():
    db.create_all()

if __name__ == '__main__':
    main()