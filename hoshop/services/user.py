# coding: utf8
#
# hoshop - user
# 
# Author: ilcwd 
# Create: 14-10-28
#
#

from ..models import user as userDAO
from .dtos import HoShopDTO
from . import util
from hoshop.core import constants

def login(logintype, loginid, password):

    # len(base64(sha256("password"))) == 44
    if len(password) != 44:
        return HoShopDTO(error=u'账号不存在或者密码错误')
    else:
        password = password.decode('base64')

    user = userDAO.login(int(logintype), loginid, password)

    if not user:
        return HoShopDTO(error=u'账号不存在或者密码错误')

    user = user.dictify()
    user.pop('password')
    return HoShopDTO(data=user)


def login_oauth(source, user):
    user = userDAO.login_oauth(source, user)
    if not user:
        return HoShopDTO(error=u'账号不存在或者密码错误')

    user = user.dictify()
    user.pop('password')
    return HoShopDTO(data=user)


def hodao_login(user, signature, timestamp):
    # ok = util.valid_request(signature, user, timestamp)
    # if not ok:
    #     return HoShopDTO(error=u'无效用户')

    user = userDAO.login_oauth(constants.USER_OAUTH_SOURCE.WECHAT, user)
    user = user.dictify()
    user.pop('password')
    return HoShopDTO(data=user)


def get_user(userid):
    u = userDAO.get_user(userid)
    if u is None:
        return HoShopDTO(error=u'用户不存在')

    return HoShopDTO(data=u)