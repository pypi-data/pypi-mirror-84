# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dj_admin_urls']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0.0']

setup_kwargs = {
    'name': 'django-admin-urls',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Alex Uzjakov',
    'author_email': 'cyberbudy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
