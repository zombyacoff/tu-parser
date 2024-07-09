from dataclasses import dataclass

from .base import ApplicationException


class ValidatorException(ApplicationException): ...


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
