from dataclasses import dataclass

from .base import BaseException


@dataclass(frozen=True, eq=False)
class InvalidSettingsError(BaseException):
    error_message: str

    @property
    def message(self) -> str:
        return self.error_message
