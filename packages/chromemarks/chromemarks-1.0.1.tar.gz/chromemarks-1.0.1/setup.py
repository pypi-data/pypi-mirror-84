# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chromemarks']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'chromemarks',
    'version': '1.0.1',
    'description': 'A Python library for accessing the local Google Chrome Bookmarks store.',
    'long_description': '# chromemarks\n\nA Python library for accessing the local Chrome Bookmarks store.\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chromemarks)](https://pypi.org/project/chromemarks/)\n[![PyPI](https://img.shields.io/pypi/v/chromemarks)](https://pypi.org/project/chromemarks/)\n[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/josxa/chromemarks/Build/main)](https://github.com/JosXa/chromemarks/actions?query=workflow%3ABuild)\n\n## Installation\n\n`pip install chromemarks`\n\n## Usage\n\nSee [examples](https://github.com/JosXa/chromemarks/tree/main/examples).\n',
    'author': 'JosXa',
    'author_email': 'joscha.goetzer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JosXa/chromemarks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
