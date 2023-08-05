# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strawberry_django']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.2,<4.0.0', 'strawberry-graphql>=0.39.1,<0.40.0']

setup_kwargs = {
    'name': 'strawberry-graphql-django',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Lauri Hintsala',
    'author_email': 'lauri.hintsala@verkkopaja.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
