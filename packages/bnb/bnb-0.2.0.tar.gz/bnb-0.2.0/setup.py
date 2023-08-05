# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bnb']

package_data = \
{'': ['*'], 'bnb': ['assets/*']}

install_requires = \
['attr>=0.3.1,<0.4.0',
 'click>=7.1.2,<8.0.0',
 'markdown>=3.3.3,<4.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'questionary>=1.5.2,<2.0.0',
 'smart_getenv>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['bnb = bnb.blogger:cli']}

setup_kwargs = {
    'name': 'bnb',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Bram Vereertbrugghen',
    'author_email': 'bram@adimian.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
