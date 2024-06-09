from dataclasses import dataclass

from ..utils import ConsoleColor
from .base import ParserException
from .messages import (
    CONFIG_FILE_ERROR_MESSAGE,
    CONFIG_NOT_FOUND_TEXT,
    INVALID_OFFSET_TEXT,
    INVALID_RELEASE_DATE_TEXT,
    INVALID_WEBSITES_TEXT,
)


@dataclass(frozen=True, eq=False)
class ConfigNotFoundError(ParserException):
    @property
    def message(self) -> str:
        return ConsoleColor.paint_info(CONFIG_NOT_FOUND_TEXT)


@dataclass(frozen=True, eq=False)
class InvalidConfigError(ParserException):
    """General exception for configuration file errors"""

    error_message: str

    @property
    def message(self) -> str:
        return ConsoleColor.paint_info(
            CONFIG_FILE_ERROR_MESSAGE.format(error=self.error_message)
        )


@dataclass(frozen=True, eq=False)
class InvalidOffsetValueError(ParserException):
    offset_value: any

    @property
    def message(self) -> str:
        return ConsoleColor.paint_info(
            INVALID_OFFSET_TEXT.format(offset_value=self.offset_value)
        )


@dataclass(frozen=True, eq=False)
class InvalidReleaseDateError(ParserException):
    release_date: any

    @property
    def message(self) -> str:
        return ConsoleColor.paint_info(
            INVALID_RELEASE_DATE_TEXT.format(release_date=self.release_date)
        )


@dataclass(frozen=True, eq=False)
class InvalidWebsiteURLError(ParserException):
    url: str

    @property
    def message(self) -> str:
        return ConsoleColor.paint_info(INVALID_WEBSITES_TEXT.format(url=self.url))
