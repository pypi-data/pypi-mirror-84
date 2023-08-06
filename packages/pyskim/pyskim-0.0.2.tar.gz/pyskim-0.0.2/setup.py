# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyskim']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'ipython>=7.19.0,<8.0.0',
 'numpy>=1.16,<2.0',
 'pandas>=1.1,<2.0',
 'scipy>=1.5,<2.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['pyskim = pyskim:main']}

setup_kwargs = {
    'name': 'pyskim',
    'version': '0.0.2',
    'description': 'Quickly create summary statistics for a given dataframe.',
    'long_description': None,
    'author': 'kpj',
    'author_email': 'kpjkpjkpjkpjkpjkpj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
