# coding:utf8
"""

Author: ilcwd
"""
from . import db
from .objects import Contact


def create_contact(userid, name='', address='', phone=''):
    sess = db.DBSession()
    contact = Contact(userid=userid, name=name, address=address, phone=phone, is_primary=True)
    sess.add(contact)
    sess.commit()
    return contact.contactid


def find_contacts(userid):
    return db.DBSession().query(Contact).filter(Contact.userid == userid).all()


def get_contact(contactid):
    return db.DBSession().query(Contact).filter(Contact.contactid == contactid).one()