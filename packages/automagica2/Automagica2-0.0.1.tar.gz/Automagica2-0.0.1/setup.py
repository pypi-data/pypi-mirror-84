# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['automagica']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'automagica2',
    'version': '0.0.1',
    'description': 'Reserved',
    'long_description': None,
    'author': 'Ossi Rajuvaara',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
