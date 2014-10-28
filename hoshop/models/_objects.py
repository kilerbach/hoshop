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
    BOOLEAN,
    TEXT,
)
from sqlalchemy import Index

from ._db import Base


def now():
    return datetime.datetime.utcnow()


class DictifyMixin(object):
    def dictify(self):
        d = {}
        for col in self.__table__.columns:
            d[col.name] = getattr(self, col.name)

        return d


class Good(Base, DictifyMixin):
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


class Catalog(Base, DictifyMixin):
    __tablename__ = 'catalog'

    catalogid = Column(INT, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    parentid = Column(INT, nullable=False)

Index('_idx_catalog_parentid', Catalog.parentid)
Index('_uidx_catalog_name', Catalog.name, unique=True)


class Cart(Base, DictifyMixin):
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

Index('_idx_cart_userid', Cart.userid)


class CartList(Base, DictifyMixin):
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


class OrderStatus(Base, DictifyMixin):
    __tablename__ = 'orderStatus'

    autoid = Column(INT, primary_key=True)
    orderid = Column(INT, nullable=False)
    modified_userid = Column(INT, nullable=False)

    created_time = Column(DATETIME(), nullable=False, default=now)
    from_status = Column(INT, nullable=False)
    to_status = Column(INT, nullable=False)
    comment = Column(VARCHAR(256), nullable=False)

Index('_idx_orderstatus_orderid', OrderStatus.orderid)


class Contact(Base, DictifyMixin):
    __tablename__ = 'contact'

    contactid = Column(INT, primary_key=True)
    userid = Column(INT, nullable=False)
    name = Column(VARCHAR(64), nullable=False)
    address = Column(VARCHAR(128), nullable=False)
    phone = Column(VARCHAR(64), nullable=False)
    is_deleted = Column(BOOLEAN, nullable=False)

    created_time = Column(DATETIME(), nullable=False, default=now)


Index('_uidx_contact_uid_n_a_p', Contact.userid, Contact.name, Contact.address, Contact.phone)


class ContactPrimary(Base, DictifyMixin):
    __tablename__ = 'contactPrimary'

    userid = Column(INT, primary_key=True)
    contactid = Column(INT, nullable=False)

    created_time = Column(DATETIME(), nullable=False, default=now)


class User(Base, DictifyMixin):
    __tablename__ = 'user'

    userid = Column(INT, primary_key=True)
    nickname = Column(VARCHAR(64), nullable=False)
    role = Column(INT, nullable=False)
    status = Column(INT, nullable=False)
    password = Column(VARBINARY(128), nullable=False)
    created_time = Column(DATETIME(), nullable=False, default=now)


class UserOAuth(Base, DictifyMixin):
    __tablename__ = 'userOAuth'

    autoid = Column(INT, primary_key=True)
    userid = Column(INT, nullable=False)
    source = Column(INT, nullable=False)
    user = Column(VARCHAR(128), nullable=False)
    created_time = Column(DATETIME(), nullable=False, default=now)

Index('_idx_useroauth_userid', UserOAuth.userid)
Index('_uidx_useroauth_s_user', UserOAuth.source, UserOAuth.user, unique=True)


class UserLogin(Base, DictifyMixin):
    __tablename__ = 'userLogin'

    autoid = Column(INT, primary_key=True)
    userid = Column(INT, nullable=False)
    logintype = Column(INT, nullable=False)
    loginid = Column(VARCHAR(256), nullable=False)
    password = Column(VARBINARY(128), nullable=False)

    created_time = Column(DATETIME(), nullable=False, default=now)

Index('_idx_userlogin_userid', UserLogin.userid)
Index('_uidx_userlogin_t_id', UserLogin.logintype, UserLogin.loginid, unique=True)