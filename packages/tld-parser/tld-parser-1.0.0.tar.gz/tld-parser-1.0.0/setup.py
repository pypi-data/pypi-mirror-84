# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tld_parser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tld-parser',
    'version': '1.0.0',
    'description': 'Parse tlds from domains.',
    'long_description': None,
    'author': 'theelous3',
    'author_email': 'theegrandmaster@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
