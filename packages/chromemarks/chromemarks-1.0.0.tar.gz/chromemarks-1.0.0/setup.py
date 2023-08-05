# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chrome_bookmarks']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'chromemarks',
    'version': '1.0.0',
    'description': 'A Python library for accessing the local Google Chrome Bookmarks store.',
    'long_description': '',
    'author': 'JosXa',
    'author_email': 'joscha.goetzer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JosXa/chrome-bookmarks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
