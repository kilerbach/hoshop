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
    error as _views_error,
    management,
)
from hoshop.apis import (
    catalog as _apis_catalog,
    cart as _apis_cart,
)

application.register_blueprint(shop.app)
application.register_blueprint(_apis_catalog.app, url_prefix='/ajax')
application.register_blueprint(_apis_cart.app, url_prefix='/ajax')
application.register_blueprint(management.app, url_prefix='/management')


def main():
    """Debug Mode"""
    host, port = '0.0.0.0', 8080
    print application.url_map
    application.run(host, port, debug=True, use_reloader=False)


if __name__ == '__main__':
    main()
