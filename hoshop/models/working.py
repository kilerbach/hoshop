# coding: utf8
#
# hoshop - working
# 
# Author: ilcwd 
# Create: 14/11/19
#

from . import _db
from ._objects import NextWorkingHour


def _is_valid_hour(h):
    try:
        return 0 < int(h) < 2359
    except (TypeError, ValueError):
        return False


def create_workinghour(start_time, msg):
    sess = _db.get_session()
    wh = NextWorkingHour(start_time=start_time, msg=msg, enable=True)
    sess.add(wh)
    sess.flush()
    return 1


def get_last_workinghour():
    wh = _db.get_session().query(NextWorkingHour).order_by(NextWorkingHour.autoid.desc()).limit(1).all()
    if wh:
        return wh[0]
    return None


def disable_workinghour(wid):
    sess = _db.get_session()
    wh = sess.query(NextWorkingHour).filter(NextWorkingHour.autoid==wid).one()
    wh.enable = False
    sess.add(wh)
    sess.flush()
    return 1
