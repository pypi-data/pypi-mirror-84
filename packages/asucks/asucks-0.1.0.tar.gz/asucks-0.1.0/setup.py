# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asucks']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp==3.7.2', 'click==7.1.2']

setup_kwargs = {
    'name': 'asucks',
    'version': '0.1.0',
    'description': 'SOCKS5 async python server',
    'long_description': None,
    'author': 'Gabriel Tincu',
    'author_email': 'gabi@aiven.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
