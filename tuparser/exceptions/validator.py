from dataclasses import dataclass

from .base import ApplicationException


class ValidatorException(ApplicationException): ...


@dataclass(frozen=True, eq=False)
class InvalidTitlesValuesError(ValidatorException):
    values: str

    @property
    def message(self) -> str:
        return f"Invalid titles: {self.values}"


@dataclass(frozen=True, eq=False)
class InvalidOffsetValueError(ValidatorException):
    value: str

    @property
    def message(self) -> str:
        return f"Invalid offset: {self.value}"


@dataclass(frozen=True, eq=False)
class InvalidProgressBarValueError(ValidatorException):
    value: str

    @property
    def message(self) -> str:
        return f"Invalid progress bar value: {self.value}\n(value must be a boolean)"


@dataclass(frozen=True, eq=False)
class InvalidReleaseDatesValuesError(ValidatorException):
    values: str

    @property
    def message(self) -> str:
        return f"Invalid release dates: {self.values}"
