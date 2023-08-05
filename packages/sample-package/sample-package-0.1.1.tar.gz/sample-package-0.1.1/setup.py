# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sample_package']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sample-package',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Mario',
    'author_email': 'mariohdpz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
