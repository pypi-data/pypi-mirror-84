# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terra_sdk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'terra-sdk',
    'version': '0.0.0',
    'description': 'The Python SDK for Terra',
    'long_description': None,
    'author': 'Terraform Labs, PTE.',
    'author_email': 'engineering@terra.money',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
