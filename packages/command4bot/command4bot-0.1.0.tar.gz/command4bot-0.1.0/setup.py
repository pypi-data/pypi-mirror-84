# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['command4bot']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'command4bot',
    'version': '0.1.0',
    'description': 'A general purpose library for command-based iteraction made for bots',
    'long_description': None,
    'author': 'Allan Chain',
    'author_email': 'allanchain@pku.edu.cn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
