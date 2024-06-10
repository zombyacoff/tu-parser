from abc import ABC, abstractmethod

from ..utils import ConsoleColor
from .messages import ERROR_TITLE


class ApplicationException(ABC, Exception):
    @staticmethod
    def get_error_message(exception: "ApplicationException") -> str:
        print(
            ConsoleColor.paint_error(ERROR_TITLE),
            ConsoleColor.paint_info(exception.message),
            sep="\n",
        )

    @property
    @abstractmethod
    def message(self) -> str: ...
