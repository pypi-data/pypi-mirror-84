# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mapz', 'mapz.methods', 'mapz.tests', 'mapz.tests.methods']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mapz',
    'version': '0.4.2',
    'description': 'Extension of dict features',
    'long_description': None,
    'author': 'vduseev',
    'author_email': 'vagiz@duseev.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
