from dataclasses import dataclass
from enum import Enum
from typing import Callable

from .constants import LAUNCH_TIME
from .exceptions import InvalidConfigurationError
from .output_file import YamlOutputFile


class Ranges(Enum):
    offset = (1, 250)
    published_years = (0, LAUNCH_TIME.year)


def is_within_range(value: int, value_range: tuple[int, int]) -> bool:
    return value_range[0] <= value <= value_range[1]


def titles(values: any) -> bool:
    return isinstance(values, list) and all(value is not None for value in values)


def boolean(value: any) -> bool:
    return isinstance(value, bool)


def offset(value: any) -> bool:
    return isinstance(value, int) and is_within_range(value, Ranges.offset.value)


def output_file(value: any) -> bool:
    return value is None or isinstance(value, YamlOutputFile)


def published_years(values: any) -> bool:
    return values is None or (
        isinstance(values, list)
        and all(isinstance(value, int) and is_within_range(value, Ranges.published_years.value) for value in values)
    )


def ensure_valid_data(value: any, condition: Callable, exception_message: str) -> None:
    if not condition(value):
        raise InvalidConfigurationError(exception_message.format(value))


@dataclass
class ValidationRule:
    condition: Callable
    exception_message: str


validation_rules = {
    "titles": ValidationRule(titles, "Invalid titles: {}\nValues must be a list without None."),
    "messages": ValidationRule(boolean, "Invalid messages value: {}\nValue must be a boolean."),
    "offset": ValidationRule(
        offset, "Invalid offset: {}\nValue must be an integer and must be between 1 and 250 inclusive."
    ),
    "output_file": ValidationRule(
        output_file, "Invalid output file value: {}\nValue must be an instance of the YamlOutputFile class."
    ),
    "progress_bar": ValidationRule(boolean, "Invalid progress bar value: {}\nValue must be a boolean."),
    "published_years": ValidationRule(
        published_years,
        "Invalid release dates: {}\nValues must be a list of integers and must be within the specified range [0, LAUNCH_TIME_YEAR].",
    ),
}


def validate_config(config: dict[str, any]) -> dict[str, any]:
    for param, rules in validation_rules.items():
        ensure_valid_data(config.get(param), rules.condition, rules.exception_message)

    return config
