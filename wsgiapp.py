#coding:utf8
"""
Created on Jun 18, 2014

@author: ilcwd
"""
import logging.config
import logging
import os

import yaml

from hoshop.core import application, C

_parent = os.path.join(os.path.dirname(__file__), 'deployment')
logging_config_path = os.path.join(_parent, 'logging.yaml')
app_config_path = os.path.join(_parent, 'config.json')

with open(logging_config_path, 'r') as f:
    logging.config.dictConfig(yaml.load(f))

C.load_config(app_config_path)
_logger = logging.getLogger(__name__)

application.secret_key = C.SERVER_SESSION_KEY
# register APIs after `C.load_config()`
from hoshop.views import (
    shop,
    default,
    admin,
    user,
    static,
)
from hoshop.apis import (
    catalog as _apis_catalog,
    cart as _apis_cart,
    admin as _apis_admin,
)

application.register_blueprint(shop.app, url_prefix='/hoshop')
application.register_blueprint(user.app, url_prefix='/hoshop/user')
application.register_blueprint(_apis_catalog.app, url_prefix='/hoshop/ajax')
application.register_blueprint(_apis_cart.app, url_prefix='/hoshop/ajax')
application.register_blueprint(admin.app, url_prefix='/hoshop/admin')
application.register_blueprint(_apis_admin.app, url_prefix='/hoshop/admin')

application.register_blueprint(static.app, url_prefix='/hoshop/s')


def main():
    """Debug Mode"""
    host, port = '0.0.0.0', 8080
    print application.url_map
    application.run(host, port, debug=True, use_reloader=False)


if __name__ == '__main__':
    main()
