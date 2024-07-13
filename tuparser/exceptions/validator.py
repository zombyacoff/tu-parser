from dataclasses import dataclass

from .base import BaseException


@dataclass(frozen=True, eq=False)
class ValidatorException(BaseException):
    value: str
    error_message: str

    @property
    def message(self) -> str:
        return self.error_message.format(self.value)
