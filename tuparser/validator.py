from typing import Callable

from .constants import LAUNCH_TIME
from .exceptions import ValidatorException

OFFSET_RANGE = (1, 250)
RELEASE_YEARS_RANGE = (0, LAUNCH_TIME.year)


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

    return values == [] or (
        isinstance(values, list)
        and len(values) <= 3
        and isinstance(values[0], dict)
        and all(value == {} for value in values[0].values())
        and optional_is_string(1)
        and optional_is_string(2)
    )


def release_years(values: any) -> bool:
    return values == [] or (
        isinstance(values, list)
        and all(isinstance(value, int) and check_range(value, RELEASE_YEARS_RANGE) for value in values)
    )


def ensure_valide_data(*, value: any, validate_func: Callable, exception_message: str) -> None:
    if not validate_func(value):
        raise ValidatorException(value, exception_message)


def validate(parser_args: dict[str, any]) -> dict[str, any]:
    ensure_valide_data(
        value=parser_args.get("titles"),
        validate_func=titles,
        exception_message="Invalid titles: {}\nValues must be a list without None",
    )
    ensure_valide_data(
        value=parser_args.get("messages"),
        validate_func=boolean,
        exception_message="Invalid messages value: {}\nValue must be a boolean",
    )
    ensure_valide_data(
        value=parser_args.get("offset"),
        validate_func=offset,
        exception_message="Invalid offset: {}\nValue must be an integer and must be between 1 and 250 inclusive",
    )
    ensure_valide_data(
        value=parser_args.get("output_file"),
        validate_func=output_file,
        exception_message="Invalid output file value: {}\nTODO",
    )
    ensure_valide_data(
        value=parser_args.get("progress_bar"),
        validate_func=boolean,
        exception_message="Invalid progress bar value: {}\nValue must be a boolean",
    )
    ensure_valide_data(
        value=parser_args.get("release_years"),
        validate_func=release_years,
        exception_message="Invalid release dates: {}\nValues must be a list of integers and must be within the specified range [0, LAUNCH_TIME_YEAR]",
    )

    return parser_args
