from dataclasses import dataclass

from ..utils import ConsoleColor
from .base import ApplicationException


class ValidatorException(ApplicationException):
    """General exception for validation errors"""

    @staticmethod
    def get_error_message(exception: "ValidatorException") -> None:
        print(
            ConsoleColor.paint_error("VALIDATION ERROR"),
            ConsoleColor.paint_info(exception.message),
            sep="\n",
        )


@dataclass(frozen=True, eq=False)
class InvalidValidationTypeError(ValidatorException):
    validation_type: str

    @property
    def message(self) -> str:
        return f"Invalid validation type: {self.validation_type}"


@dataclass(frozen=True, eq=False)
class InvalidValidationValueError(ValidatorException):
    value: str
    error_message: str

    @property
    def message(self) -> str:
        return self.error_message.format(value=self.value)
