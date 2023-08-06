# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atlantisbot_api',
 'atlantisbot_api.api',
 'atlantisbot_api.management.commands',
 'atlantisbot_api.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<3.0',
 'djangorestframework==3.10.3',
 'requests-oauthlib==1.3.0',
 'requests==2.22']

setup_kwargs = {
    'name': 'atlantisbot-api',
    'version': '0.1.0',
    'description': 'Django App to interface with the AtlantisBot API',
    'long_description': None,
    'author': 'John Victor',
    'author_email': 'johnvfs@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
