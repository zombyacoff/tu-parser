from abc import ABC, abstractmethod

from ..utils import ConsoleColor


class ApplicationException(ABC, Exception):
    @staticmethod
    def get_error_message(exception: "ApplicationException") -> None:
        print(
            ConsoleColor.paint_error(exception.__class__.__name__),
            ConsoleColor.paint_info(exception.message),
            sep="\n",
        )

    @property
    @abstractmethod
    def message(self) -> str: ...
