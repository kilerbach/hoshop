# coding: utf8
#
# hoshop - workinghour
# 
# Author: ilcwd 
# Create: 14/11/19
#
import datetime

import flask
import arrow

from ..models import working


def create_working_hour(start_time, msg):
    try:
        st = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    except (TypeError, ValueError):
        return 0
    
    st = arrow.get(st, flask.g.timezone)
    return working.create_workinghour(datetime.datetime(*st.utctimetuple()[:6]), msg)


def is_rest_time():
    wh = working.get_last_workinghour()
    if wh is not None and wh.enable and wh.start_time > datetime.datetime.utcnow():
        d = wh.dictify()
        for k in d.keys():
            if isinstance(d[k], datetime.datetime):
                d[k] = arrow.get(d[k]).to(flask.g.timezone).strftime('%Y-%m-%d %H:%M')
        return wh.msg % d

    return None


def disable_working_hour(workingid):
    return