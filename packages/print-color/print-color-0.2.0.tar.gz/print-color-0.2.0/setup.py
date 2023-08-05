# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['print_color']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'print-color',
    'version': '0.2.0',
    'description': 'A simple package to print in color to the terminal',
    'long_description': '# print-color\n\n---\n\n### Installing\n\n```\npip3 install print-color\n```\n\n### Requirements\n\n- python 3.5^\n\n### Usage\n\n```\nfrom print_color import print\n\nprint("Hello world", tag=\'success\', tag_color=\'green\', color=\'white\')\n```\n\nImg\n\n```\nprint("Error detected", tag=\'failure\', tag_color=\'red\', color=\'magenta\')\n```\n\nImg\n\n```\nprint("Printing in color", color=\'green\', format=\'underline\', background=\'cyan\')\n```\n\nImg\n\n\n',
    'author': 'xy3',
    'author_email': 'a@xsq.pw',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xy3/print-color',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
