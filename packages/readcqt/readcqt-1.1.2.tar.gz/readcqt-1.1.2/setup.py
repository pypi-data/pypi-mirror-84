# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['readcqt']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1.4,<2.0.0', 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'readcqt',
    'version': '1.1.2',
    'description': 'Converts specification from .xlsx files into a dataframe.',
    'long_description': None,
    'author': 'Sergey Belousov',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
