# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spikit']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.10,<2.0.0', 'keyring>=21.4.0,<22.0.0', 'warrant>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['spikit = spikit.cli:main']}

setup_kwargs = {
    'name': 'spikit',
    'version': '0.1.5',
    'description': 'Command line interface for Spikit Cloud Services.',
    'long_description': None,
    'author': 'PETERSON AI INC.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
