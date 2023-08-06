# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lobotomy', 'lobotomy._cli', 'lobotomy._clients', 'lobotomy._services']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'boto3>=1.16.0,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['lobotomy = lobotomy:run_cli']}

setup_kwargs = {
    'name': 'lobotomy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Scott Ernst',
    'author_email': 'swernst@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
