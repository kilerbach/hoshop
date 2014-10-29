# coding: utf8
#
# hoshop - roles
# 
# Author: ilcwd 
# Create: 14-10-28
#
# 

class Enum(object):
    @classmethod
    def has_value(cls, value):
        for k, v in cls.__dict__.iteritems():
            if k.startswith('_') or not isinstance(v, int):
                continue

            if v == value:
                return True

        return False


class USER_ROLE(Enum):
    NORMAL = 0
    ADMIN = 0xFFFFFFFF


class USER_STATUS(Enum):
    NORMAL = 0
    DISABLE = 1


class USER_OAUTH_SOURCE(Enum):
    WECHAT = 1
    QQ = 2
    SINA = 3


class USER_LOGIN_TYPE(Enum):
    MOBILE = 1
    EMAIL = 2
    NAME = 3


class ORDER_STATUS(Enum):
    UNSET = 0
    START = 10
    CONFIRM = 20
    SHIPING = 30
    SUCCESS = 40
    CANCEL = 50


ORDER_STATUS_MAPPING = {
    ORDER_STATUS.UNSET: u"等待下单",
    ORDER_STATUS.START: u"下单成功",
    ORDER_STATUS.CONFIRM: u"已确定",
    ORDER_STATUS.SHIPING: u"配送中",
    ORDER_STATUS.SUCCESS: u"已成功",
    ORDER_STATUS.CANCEL: u"取消",
}

ORDER_UPDATE_USER_RULES = {
    USER_ROLE.ADMIN: {
        ORDER_STATUS.START: (ORDER_STATUS.CONFIRM, ORDER_STATUS.SHIPING, ORDER_STATUS.SUCCESS, ORDER_STATUS.CANCEL),
        ORDER_STATUS.CONFIRM: (ORDER_STATUS.SHIPING, ORDER_STATUS.SUCCESS),
        ORDER_STATUS.SHIPING: ORDER_STATUS.SUCCESS,
    },

    USER_ROLE.NORMAL: {
        ORDER_STATUS.UNSET: ORDER_STATUS.START,
        ORDER_STATUS.START: ORDER_STATUS.CANCEL,
        ORDER_STATUS.SHIPING: ORDER_STATUS.SUCCESS,
    }
}


GOOD_EDITABLE_COLUMNS = {'name', 'price', 'count_total', 'count_left', 'count_sold_delta', 'expired_time', 'description', 'catalogid'}


def can_change_status(userrole, from_status, to_status):
    userrole = int(userrole)
    from_status = int(from_status)
    to_status = int(to_status)

    role = ORDER_UPDATE_USER_RULES.get(userrole)
    if not role:
        return False

    to_statuses = role.get(from_status)
    if not to_statuses:
        return False

    if isinstance(to_statuses, (list, tuple)):
        return to_status in to_statuses

    return to_status == to_statuses

