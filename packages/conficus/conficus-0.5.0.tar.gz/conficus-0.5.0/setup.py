# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['conficus']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'conficus',
    'version': '0.5.0',
    'description': 'python INI configuration library',
    'long_description': None,
    'author': 'Mark Gemmill',
    'author_email': 'dev@markgemmill.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mgemmill-pypi/conficus',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
