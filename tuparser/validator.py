from .exceptions import InvalidValidationTypeError, InvalidValidationValueError


def check_condition(condition: bool, value: any, exception_message: str) -> None:
    if not condition:
        raise InvalidValidationValueError(value, exception_message)


def check_range(value: int, value_range: tuple[int, int] | None) -> bool:
    # Checks that the integer value is within the range
    # if value_range is specified
    return value_range is None or value_range[0] <= value <= value_range[1]


def boolean(value: any, exception_message: str) -> bool:
    # Checks if the value is of type bool
    check_condition(isinstance(value, bool), value, exception_message)

    return value


def integer(value: int, exception_message: str, value_range: tuple[int, int] | None) -> int:
    # Checks if the value is of type int,
    # and if the range of acceptable values is specified,
    # verifies that the value is within the range
    check_condition(
        isinstance(value, int) and check_range(value, value_range),
        value,
        exception_message,
    )

    return value


def integer_list(
    values: any, exception_message: str, value_range: tuple[int, int] | None
) -> list[int]:
    # Checks if the value is of type list,
    # and ensures that all values in the list are of type int.
    # If the range of acceptable values is specified,
    # verifies that each value in the list is within the range
    check_condition(
        isinstance(values, list)
        and all(isinstance(value, int) and check_range(value, value_range) for value in values),
        values,
        exception_message,
    )

    return values


def any_list_wn(values: any, exception_message: str) -> list[any]:
    # Checks if the value is of type list,
    # and ensures that none of the values in the list are None
    check_condition(
        isinstance(values, list) and all(value is not None for value in values),
        values,
        exception_message,
    )

    return values


def validate(
    value: any,
    validation_type: str,
    *,
    default_value: any = None,
    value_range: tuple[int, int] | None = None,
    exception_message: str = "Invalid value: {value}",
) -> any:
    """Validates the value according to the specified validation type

    Required arguments:
    :param value: (Any) the value to be validated
    :param validation_type: (String) the type of validation
        "boolean": checks if the value is of type bool
        "integer": checks if the value is of type int, and if the range of
        acceptable values is specified, verifies that the value is within the range
        "integer_list": checks if the value is of type list, and ensures that
        all values in the list are of type int. If the range of acceptable
        values is specified, verifies that each value in the list is within the range
        "any_list_wn": checks if the value is of type list, and ensures that
        none of the values in the list are None

    Optional configuration arguments:
    :param default_value: (Any) the default value. The function returns this value if it is False,
    but only if the validation type != "boolean"
    :param value_range: (Tuple[int, int]) the range of acceptable values.
    Can be set if the validation type = "integer"/"integer_list"
    :param exception_message: (String) the error message if the value fails validation.
    Default value: "Invalid value: {value}"

    :return: the default value, in the case described above.
    If the validation is successful, returns the value that was initially
    passed to the function.
    """
    if validation_type != "boolean" and value is False:
        return default_value

    match validation_type:
        case "boolean":
            return boolean(value, exception_message)

        case "integer":
            return integer(value, exception_message, value_range)

        case "integer_list":
            return integer_list(value, exception_message, value_range)

        case "any_list_wn":
            return any_list_wn(value, exception_message)

        case _:
            raise InvalidValidationTypeError(validation_type=validation_type)
