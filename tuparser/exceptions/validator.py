from dataclasses import dataclass

from .base import ApplicationException


class ValidatorException(ApplicationException): ...


@dataclass(frozen=True, eq=False)
class InvalidTitlesValuesError(ValidatorException):
    values: str

    @property
    def message(self) -> str:
        return f"Invalid titles: {self.values}\nValues must be a list without None"


@dataclass(frozen=True, eq=False)
class InvalidOffsetValueError(ValidatorException):
    value: str

    @property
    def message(self) -> str:
        return f"Invalid offset: {self.value}\nValue must be an integer and must be between 1 and 250 inclusive"


@dataclass(frozen=True, eq=False)
class InvalidProgressBarValueError(ValidatorException):
    value: str

    @property
    def message(self) -> str:
        return f"Invalid progress bar value: {self.value}\nValue must be a boolean"


@dataclass(frozen=True, eq=False)
class InvalidReleaseDatesValuesError(ValidatorException):
    values: str

    @property
    def message(self) -> str:
        return f"Invalid release dates: {self.values}\nValues must be a list of integers and must be within the specified range [0, LAUNCH_TIME_YEAR]"
