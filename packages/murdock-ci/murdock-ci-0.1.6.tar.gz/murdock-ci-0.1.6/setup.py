# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['murdock_ci']

package_data = \
{'': ['*']}

install_requires = \
['agithub>=2.2.2,<3.0.0', 'tornado>=6.0.4,<7.0.0']

entry_points = \
{'console_scripts': ['murdock = murdock_ci:main']}

setup_kwargs = {
    'name': 'murdock-ci',
    'version': '0.1.6',
    'description': 'A simple gihub CI server',
    'long_description': None,
    'author': 'Kaspar Schleiser',
    'author_email': 'kaspar@schleiser.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
