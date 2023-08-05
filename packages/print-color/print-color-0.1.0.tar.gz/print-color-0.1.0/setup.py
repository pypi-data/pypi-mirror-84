# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['print_color']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'print-color',
    'version': '0.1.0',
    'description': 'A simple package to print in color to the terminal',
    'long_description': None,
    'author': 'xy3',
    'author_email': 'a@xsq.pw',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
