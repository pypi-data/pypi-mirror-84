# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioletterxpress']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.6.0,<0.7.0', 'httpx>=0.16.1,<0.17.0']

setup_kwargs = {
    'name': 'aioletterxpress',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sebatian Lübke',
    'author_email': 'sebastian@luebke.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
