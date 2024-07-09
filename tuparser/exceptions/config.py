from dataclasses import dataclass

from .base import ApplicationException


class ConfigException(ApplicationException): ...


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
