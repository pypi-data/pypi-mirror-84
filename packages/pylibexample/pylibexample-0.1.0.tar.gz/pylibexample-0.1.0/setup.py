# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylibexample']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pylibexample',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Brendan',
    'author_email': 'bshizzle1234@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
