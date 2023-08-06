# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xps_crypto',
 'xps_crypto.api',
 'xps_crypto.api.errors',
 'xps_crypto.api.middlewares',
 'xps_crypto.api.wallets',
 'xps_crypto.incoming_request_log',
 'xps_crypto.migrations']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-JSONField>=0.9.0,<0.10.0',
 'alembic>=1.4.3,<2.0.0',
 'fastapi>=0.61.1,<0.62.0',
 'gino-starlette>=0.1.1,<0.2.0',
 'gino>=1.0.1,<2.0.0',
 'gunicorn>=20.0.4,<21.0.0',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'starlette-context>=0.3.1,<0.4.0',
 'telegram-log>=1.0.12,<2.0.0',
 'uvicorn>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'xps-crypto',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'rgilfanov',
    'author_email': 'rgilfanov@fix.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
