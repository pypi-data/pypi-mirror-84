# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yofx']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2020.1,<2021.0',
 'requests>=2.24.0,<3.0.0',
 'typing_extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['yofx = yofx.cli:main']}

setup_kwargs = {
    'name': 'yofx',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Carlo Holl',
    'author_email': 'carloholl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
