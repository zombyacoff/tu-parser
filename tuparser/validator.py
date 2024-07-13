from .constants import LAUNCH_TIME
from .exceptions import ValidatorException

OFFSET_RANGE = (1, 250)
RELEASE_DATES_RANGE = (0, LAUNCH_TIME.year)


def check_range(value: int, value_range: tuple[int, int]) -> bool:
    return value_range[0] <= value <= value_range[1]


def boolean(value: any) -> bool:
    return isinstance(value, bool)


def integer(value: any) -> bool:
    return isinstance(value, int) and check_range(value, OFFSET_RANGE)


def list_int(values: any) -> bool:
    return isinstance(values, list) and all(
        isinstance(value, int) and check_range(value, RELEASE_DATES_RANGE) for value in values
    )


def list_wtn(values: any) -> bool:
    return isinstance(values, list) and all(value is not None for value in values)


def validate(*parser_args: tuple[any]) -> tuple[any]:
    validate_dict = {
        "titles": (
            parser_args[0],
            list_wtn,
            "Invalid titles: {}\nValues must be a list without None",
        ),
        "messages": (
            parser_args[1],
            boolean,
            "Invalid offset: {}\nValue must be an integer and must be between 1 and 250 inclusive",
        ),
        "offset": (
            parser_args[2],
            integer,
            "Invalid progress bar value: {}\nValue must be a boolean",
        ),
        "progress_bar": (
            parser_args[3],
            boolean,
            "Invalid release dates: {}\nValues must be a list of integers and must be within the specified range [0, LAUNCH_TIME_YEAR]",
        ),
        "release_dates": (
            parser_args[4],
            list_int,
            "Invalid messages value: {}\nValue must be a boolean",
        ),
    }
    for params in validate_dict.values():
        value, validate_function, exception_message = params
        if not validate_function(value):
            raise ValidatorException(value, exception_message)

    return parser_args
