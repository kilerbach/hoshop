# coding:utf8
"""

Author: ilcwd
"""
import datetime

from sqlalchemy import (
    Column,
    INT,
    VARCHAR,
    VARBINARY,
    DATETIME,
    BIGINT,
    BOOLEAN,
    TEXT,
)
from sqlalchemy import Index

from .db import Base


def now():
    return datetime.datetime.utcnow()


def object_to_dict(obj):
    d = {}
    for col in obj.__table__.columns:
        d[col.name] = getattr(obj, col.name)

    return d


class Good(Base):
    __tablename__ = 'good'

    goodid = Column(INT, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    catalogid = Column(INT, nullable=False)
    price = Column(INT, nullable=False)
    description = Column(TEXT, nullable=False)

    count_total = Column(INT, nullable=False)
    count_sold = Column(INT, nullable=False)

    created_time = Column(DATETIME(), nullable=False, default=now)
    modified_time = Column(DATETIME(), nullable=False, default=now)

    start_time = Column(DATETIME(), nullable=False)
    expired_time = Column(DATETIME(), nullable=False)


Index('_idx_good_catalogid', Good.catalogid)


class Catalog(Base):
    __tablename__ = 'catalog'

    catalogid = Column(INT, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    parentid = Column(INT, nullable=False)

Index('_idx_catalog_parentid', Catalog.parentid)
Index('_uidx_catalog_name', Catalog.name, unique=True)


class Cart(Base):
    __tablename__ = 'cart'

    cartid = Column(INT, primary_key=True)
    userid = Column(INT, nullable=False)

    created_time = Column(DATETIME(), nullable=False, default=now)
    modified_time = Column(DATETIME(), nullable=False, default=now)

    count = Column(INT, nullable=False)
    bill = Column(INT, nullable=False)

    is_commit = Column(BOOLEAN, nullable=False)
    contactid = Column(INT, nullable=False)
    status = Column(INT, nullable=False)

    class STATUS:
        UNSET = 0
        START = 10
        CONFIRM = 20
        SHIPING = 30
        SUCCESS = 40
        CANCEL = 50

        ALL = (UNSET, START, CONFIRM, SHIPING, SUCCESS, CANCEL)

        MAPPING = {
            UNSET: u"等待下单",
            START: u"下单成功",
            CONFIRM: u"已确定",
            SHIPING: u"配送中",
            SUCCESS: u"已成功",
            CANCEL: u"取消",
        }

Index('_idx_cart_userid', Cart.userid)


class CartList(Base):
    __tablename__ = 'cartList'

    autoid = Column(INT, primary_key=True)
    cartid = Column(INT, nullable=False)
    goodid = Column(INT, nullable=False)

    count = Column(INT, nullable=False)
    discount = Column(INT, nullable=False)
    price = Column(INT, nullable=False)

    created_time = Column(DATETIME(), nullable=False, default=now)
    comment = Column(VARCHAR(64), nullable=False)

Index('_uidx_cartlist_cartid_goodid', CartList.cartid, CartList.goodid, unique=True)


class OrderStatus(Base):
    __tablename__ = 'orderStatus'

    autoid = Column(INT, primary_key=True)
    orderid = Column(INT, nullable=False)
    modified_userid = Column(INT, nullable=False)

    created_time = Column(DATETIME(), nullable=False, default=now)
    from_status = Column(INT, nullable=False)
    to_status = Column(INT, nullable=False)
    comment = Column(VARCHAR(256), nullable=False)

Index('_idx_orderstatus_orderid', OrderStatus.orderid)


class Contact(Base):
    __tablename__ = 'contact'

    contactid = Column(INT, primary_key=True)
    userid = Column(INT, nullable=False)
    name = Column(VARCHAR(64), nullable=False)
    address = Column(VARCHAR(128), nullable=False)
    phone = Column(VARCHAR(64), nullable=False)
    is_primary = Column(BOOLEAN, nullable=False)

Index('_idx_contact_userid', Contact.userid)


class User(Base):
    __tablename__ = 'user'

    userid = Column(INT, primary_key=True)
    role = Column(INT, nullable=False)
    password = Column(VARBINARY(128), nullable=False)
    created_time = Column(DATETIME(), nullable=False, default=now)

    class ROLE:
        NORMAL = 0
        ADMIN = 0xFFFFFFFF


class UserOAuth(Base):
    __tablename__ = 'userOAuth'

    autoid = Column(INT, primary_key=True)
    userid = Column(INT, nullable=False)
    source = Column(INT, nullable=False)
    user = Column(VARBINARY(128), nullable=False)
    created_time = Column(DATETIME(), nullable=False, default=now)

    class SOURCE:
        WECHAT = 1
        QQ = 2
        SINA = 3

Index('_idx_useroauth_userid', UserOAuth.userid)
Index('_uidx_useroauth_s_user', UserOAuth.source, UserOAuth.user, unique=True)


class UserLogin(Base):
    __tablename__ = 'userLogin'

    autoid = Column(INT, primary_key=True)
    userid = Column(INT, nullable=False)
    logintype = Column(INT, nullable=False)
    loginid = Column(VARBINARY(256), nullable=False)
    password = Column(VARBINARY(128), nullable=False)

    created_time = Column(DATETIME(), nullable=False, default=now)

    class LOGINTYPE:
        MOBILE = 0
        EMAIL = 1
        NAME = 2

Index('_idx_userlogin_userid', UserLogin.userid)
Index('_uidx_userlogin_t_id', UserLogin.logintype, UserLogin.loginid, unique=True)