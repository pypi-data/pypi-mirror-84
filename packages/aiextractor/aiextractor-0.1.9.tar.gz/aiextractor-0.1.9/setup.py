# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiextractor']

package_data = \
{'': ['*']}

install_requires = \
['aihelper>=0.2.8,<0.3.0', 'pandas>=1.1.2,<2.0.0', 'pytest-cov>=2.10.1,<3.0.0']

setup_kwargs = {
    'name': 'aiextractor',
    'version': '0.1.9',
    'description': '',
    'long_description': None,
    'author': 'mjaquier',
    'author_email': 'mjaquier@mjaquier.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
