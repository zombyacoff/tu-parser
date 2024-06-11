from dataclasses import dataclass

from .base import ApplicationException
from .messages import (
    CONFIG_FILE_ERROR_MESSAGE,
    CONFIG_NOT_FOUND_MESSAGE,
    INVALID_OFFSET_MESSAGE,
    INVALID_TITLES_MESSAGE,
    INVALID_YEARS_MESSAGE,
)


@dataclass(frozen=True, eq=False)
class ConfigNotFoundError(ApplicationException):
    path: str

    @property
    def message(self) -> str:
        return CONFIG_NOT_FOUND_MESSAGE.format(path=self.path)


@dataclass(frozen=True, eq=False)
class InvalidConfigError(ApplicationException):
    """General exception for configuration file errors"""

    error_message: str

    @property
    def message(self) -> str:
        return CONFIG_FILE_ERROR_MESSAGE.format(error=self.error_message)


@dataclass(frozen=True, eq=False)
class InvalidOffsetValueError(ApplicationException):
    value: any

    @property
    def message(self) -> str:
        return INVALID_OFFSET_MESSAGE.format(value=self.value)


@dataclass(frozen=True, eq=False)
class InvalidReleaseDateError(ApplicationException):
    years: any

    @property
    def message(self) -> str:
        return INVALID_YEARS_MESSAGE.format(years=self.years)


@dataclass(frozen=True, eq=False)
class InvalidTitleError(ApplicationException):
    titles: any

    @property
    def message(self) -> str:
        return INVALID_TITLES_MESSAGE.format(titles=self.titles)
