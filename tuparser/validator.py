from dataclasses import dataclass
from typing import Callable

from .constants import LAUNCH_TIME
from .exceptions import InvalidSettingsError

OFFSET_RANGE = (1, 250)
PUBLISHED_YEARS_RANGE = (0, LAUNCH_TIME.year)


def check_range(value: int, value_range: tuple[int, int]) -> bool:
    return value_range[0] <= value <= value_range[1]


def titles(values: any) -> bool:
    return isinstance(values, list) and all(value is not None for value in values)


def boolean(value: any) -> bool:
    return isinstance(value, bool)


def offset(value: any) -> bool:
    return isinstance(value, int) and check_range(value, OFFSET_RANGE)


def output_file(values: any) -> bool:
    def optional_is_string(index: int) -> bool:
        return isinstance(values[index], str) if len(values) >= index + 1 else True

    return values is None or (
        isinstance(values, list)
        and 1 <= len(values) <= 3
        and isinstance(values[0], dict)
        and all(value == {} for value in values[0].values())
        and optional_is_string(1)
        and optional_is_string(2)
    )


def published_years(values: any) -> bool:
    return values is None or (
        isinstance(values, list)
        and all(isinstance(value, int) and check_range(value, PUBLISHED_YEARS_RANGE) for value in values)
    )


def ensure_valide_data(*, value: any, validate_function: Callable, exception_message: str) -> None:
    if not validate_function(value):
        raise InvalidSettingsError(exception_message.format(value))


@dataclass
class ValidationRules:
    validation_function: Callable
    exception_message: str


validation_rules = {
    "titles": ValidationRules(titles, "Invalid titles: {}\nValues must be a list without None"),
    "messages": ValidationRules(boolean, "Invalid messages value: {}\nValue must be a boolean"),
    "offset": ValidationRules(
        offset, "Invalid offset: {}\nValue must be an integer and must be between 1 and 250 inclusive"
    ),
    "output_file": ValidationRules(output_file, "Invalid output file value: {}\nTODO"),
    "progress_bar": ValidationRules(boolean, "Invalid progress bar value: {}\nValue must be a boolean"),
    "published_years": ValidationRules(
        published_years,
        "Invalid release dates: {}\nValues must be a list of integers and must be within the specified range [0, LAUNCH_TIME_YEAR]",
    ),
}


def validate(settings: dict[str, any]) -> dict[str, any]:
    for setting, rules in validation_rules.items():
        ensure_valide_data(
            value=settings.get(setting),
            validate_function=rules.validation_function,
            exception_message=rules.exception_message,
        )

    return settings
