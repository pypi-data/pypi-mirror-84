Conficus v0.5.1 
===================

Python INI Configuration
^^^^^^^^^^^^^^^^^^^^^^^^


|version-badge| |coverage-badge|

``conficus`` is a python ini configuration utility. It reads ini and toml based
configuration files into a python dict. ``conficus`` provides automatic
coercing of values (e.g. str -> int), nested sections, easy access and
section inheritance.

v0.5.0 drops support for all python versions less that 3.6. The next minor version
will also drop it's custom ini support solely for toml format.


Installation
~~~~~~~~~~~~

Install the ``ficus`` package with pip.

.. code:: bash

        pip install conficus

Quick Start
~~~~~~~~~~~

Basic usage:

.. code:: python

    >>> 
    >>> import conficus as ficus
    >>>

Configurations can be loaded from a file path string:

.. code:: python

    >>> config = ficus.load('/Users/mgemmill/config.ini', toml=True)
    >>>

Or from path stored in an environment variable:

.. code:: python

    >>> config = ficus.load('ENV_VAR_CONFIG_PATH')
    >>>

.. code:: python

    >>> # configuration is just a dictionary:
    ... 
    >>> print config['app']['debug']
    True
    >>>
    >>> # with ease of access:
    ... 
    >>> print config['app.debug']
    True

.. |version-badge| image:: https://img.shields.io/badge/version-v0.5.1-green.svg
.. |coverage-badge| image:: https://img.shields.io/badge/coverage-100%25-green.svg
