from abc import ABC, abstractmethod

from ..utils import ConsoleColor, uppercamelcase_split


class BaseException(ABC, Exception):
    @staticmethod
    def get_error_message(exception: "BaseException") -> None:
        print(
            ConsoleColor.paint_error(uppercamelcase_split(exception.__class__.__name__).upper()),
            ConsoleColor.paint_info(exception.message),
            sep="\n",
        )

    @property
    @abstractmethod
    def message(self) -> str: ...
