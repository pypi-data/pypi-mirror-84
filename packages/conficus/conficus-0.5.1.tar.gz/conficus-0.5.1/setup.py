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
    'version': '0.5.1',
    'description': 'python INI configuration library',
    'long_description': "Conficus v0.5.1 \n===================\n\nPython INI Configuration\n^^^^^^^^^^^^^^^^^^^^^^^^\n\n\n|version-badge| |coverage-badge|\n\n``conficus`` is a python ini configuration utility. It reads ini and toml based\nconfiguration files into a python dict. ``conficus`` provides automatic\ncoercing of values (e.g. str -> int), nested sections, easy access and\nsection inheritance.\n\nv0.5.0 drops support for all python versions less that 3.6. The next minor version\nwill also drop it's custom ini support solely for toml format.\n\n\nInstallation\n~~~~~~~~~~~~\n\nInstall the ``ficus`` package with pip.\n\n.. code:: bash\n\n        pip install conficus\n\nQuick Start\n~~~~~~~~~~~\n\nBasic usage:\n\n.. code:: python\n\n    >>> \n    >>> import conficus as ficus\n    >>>\n\nConfigurations can be loaded from a file path string:\n\n.. code:: python\n\n    >>> config = ficus.load('/Users/mgemmill/config.ini', toml=True)\n    >>>\n\nOr from path stored in an environment variable:\n\n.. code:: python\n\n    >>> config = ficus.load('ENV_VAR_CONFIG_PATH')\n    >>>\n\n.. code:: python\n\n    >>> # configuration is just a dictionary:\n    ... \n    >>> print config['app']['debug']\n    True\n    >>>\n    >>> # with ease of access:\n    ... \n    >>> print config['app.debug']\n    True\n\n.. |version-badge| image:: https://img.shields.io/badge/version-v0.5.1-green.svg\n.. |coverage-badge| image:: https://img.shields.io/badge/coverage-100%25-green.svg\n",
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
