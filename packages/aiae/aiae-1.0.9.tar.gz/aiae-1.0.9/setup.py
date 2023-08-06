# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiae']

package_data = \
{'': ['*']}

install_requires = \
['aihelper>=0.2.11,<0.3.0',
 'matplotlib>=3.2.2,<4.0.0',
 'oyaml>=0.9,<0.10',
 'pandas>=1.0.4,<2.0.0',
 'scipy>=1.5.3,<2.0.0',
 'seaborn>=0.11.0,<0.12.0',
 'xlsxwriter>=1.2.9,<2.0.0']

setup_kwargs = {
    'name': 'aiae',
    'version': '1.0.9',
    'description': '',
    'long_description': None,
    'author': 'mjaquier',
    'author_email': 'mjaquier@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
