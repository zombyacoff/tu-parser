from dataclasses import dataclass
from enum import Enum
from typing import Callable

from .constants import LAUNCH_TIME
from .exceptions import InvalidConfigurationError


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
    if value is None:
        return True

    if not isinstance(value, dict) or "pattern" not in value:
        return False

    pattern = value.get("pattern")
    optional_keys = {"name", "folder_path"}
    if not (
        isinstance(pattern, dict)
        and pattern
        and all(value == {} for value in pattern.values())
        and all(isinstance(value.get(key), str) for key in optional_keys if key in value)
    ):
        return False

    allowed_keys = {"pattern", "name", "folder_path"}
    return set(value.keys()).issubset(allowed_keys)


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
        output_file,
        """Invalid output file value: {}
The value must be a dictionary with 3 keys:
"pattern" - the pattern on which the output file will be created, the type is dictionary whose values are empty dictionaries,
"name" - the name of the output file, and "folder_path" - the path to the folder where the output file will be created.
The type of the "name" and "folder_path" values is string.""",
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
