# coding:utf8
"""

Author: ilcwd
"""

from . import _db
from ._objects import Contact, ContactPrimary, now


def create_contact(userid, name='', address='', phone=''):
    sess = _db.get_session()
    c = sess.query(Contact).\
        filter(Contact.userid==userid).\
        filter(Contact.name==name).\
        filter(Contact.address==address).filter(Contact.phone==phone).all()
    if c:
        c = c[0]
        if c.is_deleted:
            c.is_deleted = False
            sess.add(c)
            sess.flush()
        return c.contactid

    contact = Contact(userid=userid, name=name, address=address, phone=phone, is_deleted=False)
    sess.add(contact)
    sess.flush()
    return contact.contactid


def delete_contact(userid, contactid):
    sess = _db.get_session()
    if sess.query(Contact).filter(Contact.userid==userid).filter(Contact.contactid==contactid).update({'is_deleted': True}):
        sess.query(ContactPrimary).filter(ContactPrimary.userid==userid).filter(ContactPrimary.contactid==contactid).delete()
        sess.flush()
    return 1


def get_default_contact(userid):
    sess = _db.get_session()
    cp = sess.query(ContactPrimary).filter(ContactPrimary.userid==userid).all()
    if not cp:
        return None

    return sess.query(Contact).filter(Contact.contactid == cp[0].contactid).one()


def set_default_contact(userid, contactid):
    sess = _db.get_session()
    cps = sess.query(ContactPrimary).filter(ContactPrimary.userid==userid).all()
    if not cps:
        cp = ContactPrimary(userid=userid, contactid=contactid)
    else:
        cp = cps[0]
        cp.contactid = contactid
        cp.created_time = now()

    sess.add(cp)
    sess.flush()
    return 1



def find_contacts(userid):
    return _db.get_session().query(Contact).filter(Contact.userid == userid).filter(Contact.is_deleted == False).all()


def get_contact(contactid):
    return _db.get_session().query(Contact).filter(Contact.contactid == contactid).one()