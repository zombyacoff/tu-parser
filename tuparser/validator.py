from dataclasses import dataclass
from enum import Enum
from typing import Callable

from .constants import LAUNCH_TIME
from .exceptions import InvalidConfigurationError
from .output_file import YamlOutputFile


class Ranges(Enum):
    offset = (1, 250)
    published_years = (0, LAUNCH_TIME.year)


def check_range(value: int, value_range: tuple[int, int]) -> bool:
    return value_range[0] <= value <= value_range[1]


def titles(values: any) -> bool:
    return isinstance(values, list) and all(value is not None for value in values)


def boolean(value: any) -> bool:
    return isinstance(value, bool)


def offset(value: any) -> bool:
    return isinstance(value, int) and check_range(value, Ranges.offset.value)


def output_file(value: any) -> bool:
    return value is None or isinstance(value, YamlOutputFile)


def published_years(values: any) -> bool:
    return values is None or (
        isinstance(values, list)
        and all(isinstance(value, int) and check_range(value, Ranges.published_years.value) for value in values)
    )


def ensure_valide_data(*, value: any, condition: Callable, exception_message: str) -> None:
    if not condition(value):
        raise InvalidConfigurationError(exception_message.format(value))


@dataclass
class ValidationRules:
    condition: Callable
    exception_message: str


validation_rules = {
    "titles": ValidationRules(titles, "Invalid titles: {}\nValues must be a list without None."),
    "messages": ValidationRules(boolean, "Invalid messages value: {}\nValue must be a boolean."),
    "offset": ValidationRules(
        offset, "Invalid offset: {}\nValue must be an integer and must be between 1 and 250 inclusive."
    ),
    "output_file": ValidationRules(
        output_file, "Invalid output file value: {}\nValue must be an instance of the YamlOutputFile class."
    ),
    "progress_bar": ValidationRules(boolean, "Invalid progress bar value: {}\nValue must be a boolean."),
    "published_years": ValidationRules(
        published_years,
        "Invalid release dates: {}\nValues must be a list of integers and must be within the specified range [0, LAUNCH_TIME_YEAR].",
    ),
}


def validate(config: dict[str, any]) -> dict[str, any]:
    for param, rules in validation_rules.items():
        ensure_valide_data(
            value=config.get(param), condition=rules.condition, exception_message=rules.exception_message
        )

    return config
