# coding:utf8
"""

Author: ilcwd
"""
import hashlib
import time
import urllib

from hoshop.core import C

def sign_request(*a):
    params = list(a)
    params.append(C.SERVER_SIGNATURE_KEY)

    return hashlib.sha1(''.join(sorted(map(str, params)))).hexdigest()

def valid_request(s, u, t):
    # expired
    if abs(int(t) - time.time()) > C.LOGIN_URL_EXPIRES:
        return False

    expect = sign_request(u, t)

    return expect == str(s)
