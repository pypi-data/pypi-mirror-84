# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['supertimer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'supertimer',
    'version': '0.1.0',
    'description': 'Contextmanager to print or log execution time of code blocks',
    'long_description': None,
    'author': 'Marius Helf',
    'author_email': 'helfsmarius@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
