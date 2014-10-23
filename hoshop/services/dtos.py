# coding:utf8
"""

Author: ilcwd
"""


class HoShopDTO(object):
    OK = 0
    ERR = 1

    def __init__(self, error=None, data=None):
        if error:
            self.status = self.ERR
        else:
            self.status = self.OK

        self.error = error
        self.data = data or {}

    def ok(self):
        return self.status == self.OK