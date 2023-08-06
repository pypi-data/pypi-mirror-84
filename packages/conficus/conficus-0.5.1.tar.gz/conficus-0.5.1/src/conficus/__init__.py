# -*- coding: utf-8 -*-
from os import environ
from os import path
from pathlib import Path
from . import coerce
from . import parse
from . import toml
from .inherit import inherit as _inherit
from .readonly import ReadOnlyDict


def read_config(config_input):
    """
    read_config assumes `config_input` is one of the following in this
    order:

        1. a file path string.
        2. an environment variable name.
        3. a raw config string.

    """

    def _readlines(pth):
        with open(pth, "r") as fh_:
            return fh_.read()

    if isinstance(config_input, Path):
        return config_input.read_text().split("\n")

    if path.exists(config_input):
        config_input = _readlines(config_input)

    elif config_input in environ and path.exists(environ[config_input]):
        config_input = _readlines(environ[config_input])

    return config_input.split("\n")


def load(config_path, **kwargs):
    """
    keyword arguments:

        inheritance=False
        readonly=True
        use_pathlib=False
        use_decimal=False
        coercers=None

    """

    use_pathlib = kwargs.get("use_pathlib", False) or kwargs.get("pathlib", False)
    use_decimal = kwargs.get("use_decimal", False) or kwargs.get("decimal", False)
    use_toml = kwargs.get("use_toml", False) or kwargs.get("toml", False)
    coercers = kwargs.get("coercers")

    _parse = parse.parse
    _coerce = coerce.coerce

    if use_toml is True:
        _parse = toml.parse
        _coerce = toml.coerce

    config = _parse(read_config(config_path))
    config = _coerce(
        config, pathlib=use_pathlib, decimal=use_decimal, coercers=coercers
    )

    if kwargs.get("inheritance", False) is True:
        config = _inherit(config)

    if kwargs.get("readonly", True) is True:
        config = ReadOnlyDict(config)

    return config
