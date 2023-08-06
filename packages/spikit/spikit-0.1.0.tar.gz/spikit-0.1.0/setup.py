# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spikit']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['APPLICATION-NAME = spikit']}

setup_kwargs = {
    'name': 'spikit',
    'version': '0.1.0',
    'description': 'Command line interface for Spikit Cloud Services.',
    'long_description': None,
    'author': 'PETERSON AI INC.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
