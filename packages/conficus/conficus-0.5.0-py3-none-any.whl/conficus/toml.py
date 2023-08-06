from decimal import Decimal
import tomlkit
from .coerce import coerce_unx_path
from .coerce import coerce_win_path
from .coerce import handle_custom_coercers
from .parse import matcher
from .structs import ConfigDict
from .structs import DoubleLinkedDict

coerce_str_to_decimal = (matcher(r"^(?P<value>\d+\.\d+)$"), Decimal)


def parse(config):
    return ConfigDict(tomlkit.parse("\n".join(config)))


def coerce(config, **kwargs):  # pragma pylint: disable=redefined-builtin

    coercers = DoubleLinkedDict()

    if kwargs.get("pathlib", False) is True:
        coercers.append("win_path", coerce_win_path)
        coercers.append("unix_path", coerce_unx_path)

    if kwargs.get("decimal", False) is True:
        coercers.append("decimal", coerce_str_to_decimal)

    # # add any custom coercers
    for name, custom_coercer in handle_custom_coercers(kwargs.get("coercers")):
        if name in coercers:
            coercers.replace(name, custom_coercer)
        else:
            coercers.prepend(name, custom_coercer)

    for section, key, value in config.walk():
        for coercer in coercers:
            m, converter = coercer.content
            if m(value):
                new_value = converter(value)
                section[key] = new_value
                break

    return config
