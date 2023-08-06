# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['currency']

package_data = \
{'': ['*']}

install_requires = \
['dtb.mapped-collection>=1.0.3,<2.0.0', 'pydantic>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'dtb.currency',
    'version': '1.0.1',
    'description': 'Simple currency package',
    'long_description': None,
    'author': 'Dima Doroshev',
    'author_email': 'dima@doroshev.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
