from dataclasses import dataclass

from .base import ApplicationException


@dataclass(frozen=True, eq=False)
class InvalidConfigurationError(ApplicationException):
    error_message: str

    @property
    def message(self) -> str:
        return self.error_message
