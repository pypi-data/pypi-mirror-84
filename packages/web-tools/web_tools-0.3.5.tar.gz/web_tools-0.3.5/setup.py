# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['web_tools', 'web_tools.fastapi', 'web_tools.fastapi.request_log']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-JSONField>=0.9.0,<0.10.0',
 'fastapi>=0.61.1,<0.62.0',
 'gino>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'web-tools',
    'version': '0.3.5',
    'description': '',
    'long_description': None,
    'author': 'rgilfanov',
    'author_email': 'rgilfanov@fix.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
