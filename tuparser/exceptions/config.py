from dataclasses import dataclass

from ..utils import ConsoleColor
from .base import ApplicationException
from .messages import ERROR_TITLE, FILE_NOT_FOUND_MESSAGE


class ConfigException(ApplicationException):
    """General exception for configuration file errors"""

    @staticmethod
    def get_error_message(exception: "ConfigException") -> str:
        print(
            ConsoleColor.paint_error(
                ERROR_TITLE.format(title="CONFIGURATION FILE")),
            ConsoleColor.paint_info(exception.message),
            sep="\n",
        )


@dataclass(frozen=True, eq=False)
class ConfigNotFoundError(ConfigException):
    path: str

    @property
    def message(self) -> str:
        return FILE_NOT_FOUND_MESSAGE.format(path=self.path)


@dataclass(frozen=True, eq=False)
class InvalidConfigError(ConfigException):
    error_message: str

    @property
    def message(self) -> str:
        return self.error_message
