# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['botocove']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.12,<2.0.0']

setup_kwargs = {
    'name': 'botocove',
    'version': '0.1.0',
    'description': 'A simple decorator to run functions against all AWS accounts in an organization',
    'long_description': None,
    'author': 'Dave Connell',
    'author_email': '39798556+connelldave@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
