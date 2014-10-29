# coding:utf8
"""

Author: ilcwd
"""


import wsgiapp

from hoshop.models._db import db
from hoshop.models import good, catalog, cart, contact

from hoshop.services import user

from Crypto.Cipher import AES
import os
import hashlib

def main():

    print user.hodao_login('publicuser', '', '').data

    db.session.commit()

if __name__ == '__main__':
    main()