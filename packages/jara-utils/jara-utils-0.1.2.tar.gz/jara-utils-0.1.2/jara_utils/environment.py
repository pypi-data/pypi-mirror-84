import os

from typing import Optional, List

from jara_utils.exceptions import EnvironmentVariableNotFound
from jara_utils.normalization.boolean import str_2_bool
from jara_utils.normalization.integer import parse_int


def get_str(name: str, invalid=None, required: bool = False) -> Optional[str]:
    if name not in os.environ and required:
        raise EnvironmentVariableNotFound(name)
    return str(os.environ.get(name, '')) or invalid


def get_int(name: str, invalid=None, required: bool = False) -> Optional[int]:
    if name not in os.environ and required:
        raise EnvironmentVariableNotFound(name)
    return parse_int(os.environ.get(name)) or invalid


def get_bool(name: str, invalid=None, required: bool = False) -> Optional[bool]:
    if name not in os.environ and required:
        raise EnvironmentVariableNotFound(name)
    value = str_2_bool(os.environ.get(name))
    return value if value is not None else invalid


def get_list(name: str, separator: str = ',', invalid=None, required: bool = False) -> List[str]:
    if name not in os.environ and required:
        raise EnvironmentVariableNotFound(name)

    if invalid is None:
        invalid = list()

    value = os.environ.get(name)
    return value.split(separator) if value else invalid
