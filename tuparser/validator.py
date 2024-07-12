from typing import Callable

from .constants import LAUNCH_TIME
from .exceptions import (
    InvalidOffsetValueError,
    InvalidProgressBarValueError,
    InvalidReleaseDatesValuesError,
    InvalidTitlesValuesError,
    ValidatorException,
)

OFFSET_RANGE = (1, 250)
RELEASE_DATES_RANGE = (0, LAUNCH_TIME.year)


def check_range(value: int, value_range: tuple[int, int]) -> bool:
    return value_range[0] <= value <= value_range[1]


def titles(values: any) -> bool:
    return isinstance(values, list) and all(value is not None for value in values)


def offset(value: any) -> bool:
    return isinstance(value, int) and check_range(value, OFFSET_RANGE)


def progress_bar(value: any) -> bool:
    return isinstance(value, bool)


def release_dates(values: any) -> bool:
    return isinstance(values, list) and all(
        isinstance(value, int) and check_range(value, RELEASE_DATES_RANGE) for value in values
    )


def validate_raise(
    value: any, validate_func: Callable, validate_exception: ValidatorException
) -> bool:
    if not validate_func(value):
        raise validate_exception(value)


def validate(*parser_args: tuple[any]) -> tuple[any]:
    titles, offset, progress_bar, release_dates = parser_args

    validate_raise(titles, titles, InvalidTitlesValuesError)
    validate_raise(offset, offset, InvalidOffsetValueError)
    validate_raise(progress_bar, progress_bar, InvalidProgressBarValueError)
    validate_raise(release_dates, release_dates, InvalidReleaseDatesValuesError)

    return parser_args
