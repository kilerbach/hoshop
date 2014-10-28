# coding:utf8
"""

Author: ilcwd
"""
import re
import os
import hashlib

from Crypto.Cipher import AES

from . import _db
from ._objects import UserLogin, User, UserOAuth
from hoshop.core import C, contants


DEFAULT_NICKNAME = u'登陆用户'

LOGINID_VALID = {
    contants.USER_LOGIN_TYPE.EMAIL: lambda x: True,
    contants.USER_LOGIN_TYPE.MOBILE: lambda x: True,
    contants.USER_LOGIN_TYPE.NAME: lambda x: re.match(r"[a-z]{1}[a-z0-9]{3,10}", x),
}

class PasswordFactory(object):
    """

    Save Password

    Password in database:
        [IV][Magic][Data: [[Salt][Sha256]][Padding]]

        16bytes + 16bytes + 8bytes + 32bytes + 8bytes = 80bytes
    """

    SALT_LENGTH = 8

    def __init__(self, key):
        self.k = hashlib.sha256(key).digest()
        self.magic = r'BNP4Uk1rE1CUW6rB'

    @staticmethod
    def pkcs5_padding(s):
        length = len(s)
        return s + (16 - length%16) * chr(16 - length%16)

    @staticmethod
    def pkcs5_unpadding(s):
        print ord(s[-1])
        return s[0:-ord(s[-1])]

    def encrypt(self, text):
        iv = os.urandom(16)
        aes = AES.new(self.k, mode=AES.MODE_CBC, IV=iv)
        return iv + aes.encrypt(self.pkcs5_padding(self.magic + text))

    def save_password(self, password):
        salt = os.urandom(self.SALT_LENGTH)
        raw = salt + hashlib.sha256(salt + password).digest()
        return self.encrypt(raw)

    def match_password(self, saved_password, password):
        raw = self.decrypt(saved_password)
        salt = raw[:self.SALT_LENGTH]
        calc = hashlib.sha256(salt + password).digest()
        return calc == raw[self.SALT_LENGTH:]

    def decrypt(self, cipher):
        print '####', cipher.encode('hex'), type(cipher)
        iv = cipher[:16]
        cipher = cipher[16:]

        aes = AES.new(self.k, mode=AES.MODE_CBC, IV=iv)
        text = self.pkcs5_unpadding(aes.decrypt(cipher))

        if not self._match_magic_code(text):
            return None

        return text[len(self.magic):]

    def _match_magic_code(self, d):
        return d.startswith(self.magic)


_passwordFactory = PasswordFactory(C.SERVER_PASSWORD_KEY)


def _normalize_loginid(loginid):
    if isinstance(loginid, (unicode)):
        loginid = loginid.encode('utf8')
    return loginid.lower()


def login_oauth(source, user):
    """
    Login or Create a new OAuth user.
    :param user:
    :param source:
    :return:
    """
    source = int(source)
    if source not in contants.USER_OAUTH_SOURCE.ALL:
        return None

    sess = _db.get_session()
    u = sess.query(UserOAuth).filter(UserOAuth.source==source).filter(UserOAuth.user==user).one()
    if not u:
        user = User(nickname=DEFAULT_NICKNAME, role=User.ROLE.NORMAL, status=User.STATUS.NORMAL, password='')
        sess.add(user)
        sess.flush()

        u = UserOAuth(source=source, user=user, userid=user.userid)
        sess.add(u)
        sess.flush()
    else:
        user = sess.query(User).filter(User.userid==u.userid).one()

    return user



def login(logintype, loginid, password):
    sess = _db.get_session()
    loginid = _normalize_loginid(loginid)

    u = sess.query(UserLogin).filter(UserLogin.logintype==logintype).filter(UserLogin.loginid==loginid).all()
    if not u:
        return None

    u = u[0]
    user = sess.query(User).filter(User.userid==u.userid).one()

    if not _passwordFactory.match_password(user.password, password):
        return None

    return user


def get_user(userid):
    sess = _db.get_session()
    us = sess.query(User).filter(User.userid==userid).all()
    if not us:
        return None

    u = us[0]
    return u


def create_user(logintype, loginid, password, userid=None, role=contants.USER_ROLE.NORMAL, status=contants.USER_STATUS.NORMAL):
    if not logintype in UserLogin.LOGINTYPE.ALL:
        return 0

    loginid = _normalize_loginid(loginid)

    if not LOGINID_VALID[logintype](loginid):
        return 0

    sess = _db.get_session()
    if not userid:
        user = User(nickname=loginid, role=role, status=status,
                    password=_passwordFactory.save_password(password))
        sess.add(user)
        sess.flush()
    else:
        user = sess.query(User).filter(User.userid==userid).one()
        if user.password:
            if not _passwordFactory.match_password(user.password, password):
                return 0
        else:
            user.password = _passwordFactory.save_password(password)
            sess.add(user)

    login = UserLogin(userid=user.userid, logintype=logintype, loginid=loginid, password='')
    sess.add(login)
    sess.flush()
    return 1


