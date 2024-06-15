from dataclasses import dataclass

from ..utils import ConsoleColor
from .base import ApplicationException
from .messages import ERROR_TITLE, INVALID_VALIDATION_TYPE_MESSAGE


class ValidatorException(ApplicationException):
    """General exception for validation errors"""

    @staticmethod
    def get_error_message(exception: "ValidatorException") -> str:
        print(
            ConsoleColor.paint_error(ERROR_TITLE.format(title="VALIDATION")),
            ConsoleColor.paint_info(exception.message),
            sep="\n",
        )


@dataclass(frozen=True, eq=False)
class InvalidValidationTypeError(ValidatorException):
    validation_type: str

    @property
    def message(self) -> str:
        return INVALID_VALIDATION_TYPE_MESSAGE.format(
            type=self.validation_type)


@dataclass(frozen=True, eq=False)
class InvalidValueError(ValidatorException):
    value: str
    error_message: str

    @property
    def message(self) -> str:
        return self.error_message.format(value=self.value)
