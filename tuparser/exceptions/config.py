from dataclasses import dataclass

from ..utils import ConsoleColor
from .base import ApplicationException
from .messages import (
    CONFIG_ERROR_TITLE,
    CONFIG_NOT_FOUND_MESSAGE,
    INVALID_OFFSET_MESSAGE,
    INVALID_PROGRESS_BAR_MESSAGE,
    INVALID_TITLES_MESSAGE,
    INVALID_YEARS_MESSAGE,
)


class ConfigException(ApplicationException):
    """General exception for configuration file errors"""

    @staticmethod
    def get_error_message(exception: "ConfigException") -> str:
        print(
            ConsoleColor.paint_error(CONFIG_ERROR_TITLE),
            ConsoleColor.paint_info(exception.message),
            sep="\n",
        )


@dataclass(frozen=True, eq=False)
class ConfigNotFoundError(ConfigException):
    path: str

    @property
    def message(self) -> str:
        return CONFIG_NOT_FOUND_MESSAGE.format(path=self.path)


@dataclass(frozen=True, eq=False)
class InvalidConfigError(ConfigException):
    error_message: str

    @property
    def message(self) -> str:
        return self.error_message


@dataclass(frozen=True, eq=False)
class InvalidOffsetValueError(ConfigException):
    value: any

    @property
    def message(self) -> str:
        return INVALID_OFFSET_MESSAGE.format(value=self.value)


@dataclass(frozen=True, eq=False)
class InvalidReleaseDateError(ConfigException):
    years: any

    @property
    def message(self) -> str:
        return INVALID_YEARS_MESSAGE.format(years=self.years)


@dataclass(frozen=True, eq=False)
class InvalidTitleError(ConfigException):
    titles: any

    @property
    def message(self) -> str:
        return INVALID_TITLES_MESSAGE.format(titles=self.titles)


@dataclass(frozen=True, eq=False)
class InvalidProgressBarError(ConfigException):
    value: any

    @property
    def message(self) -> str:
        return INVALID_PROGRESS_BAR_MESSAGE.format(value=self.value)
