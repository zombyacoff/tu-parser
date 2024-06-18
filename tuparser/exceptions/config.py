from dataclasses import dataclass

from ..utils import ConsoleColor
from .base import ApplicationException


class ConfigException(ApplicationException):
    """General exception for configuration file errors"""

    @staticmethod
    def get_error_message(exception: "ConfigException") -> None:
        print(
            ConsoleColor.paint_error("CONFIGURATION FILE ERROR"),
            ConsoleColor.paint_info(exception.message),
            sep="\n",
        )


@dataclass(frozen=True, eq=False)
class ConfigNotFoundError(ConfigException):
    path: str

    @property
    def message(self) -> str:
        return f"The {self.path} YAML configuration file is missing"


@dataclass(frozen=True, eq=False)
class InvalidConfigError(ConfigException):
    error_message: str

    @property
    def message(self) -> str:
        return self.error_message
