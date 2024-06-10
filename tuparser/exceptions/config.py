from dataclasses import dataclass

from .base import ApplicationException
from .messages import (
    CONFIG_FILE_ERROR_MESSAGE,
    CONFIG_NOT_FOUND_MESSAGE,
    INVALID_OFFSET_MESSAGE,
    INVALID_TITLES_MESSAGE,
    INVALID_WEBSITES_MESSAGE,
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
        return INVALID_OFFSET_MESSAGE.format(offset_value=self.value)


@dataclass(frozen=True, eq=False)
class InvalidReleaseDateError(ApplicationException):
    year: any

    @property
    def message(self) -> str:
        return INVALID_YEARS_MESSAGE.format(year=self.release_date)


@dataclass(frozen=True, eq=False)
class InvalidTitleError(ApplicationException):
    title: any

    @property
    def message(self) -> str:
        return INVALID_TITLES_MESSAGE.format(title=self.title)


@dataclass(frozen=True, eq=False)
class InvalidWebsiteURLError(ApplicationException):
    url: str

    @property
    def message(self) -> str:
        return INVALID_WEBSITES_MESSAGE.format(url=self.url)
