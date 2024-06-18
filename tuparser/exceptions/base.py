from abc import ABC, abstractmethod


class ApplicationException(ABC, Exception):
    @staticmethod
    @abstractmethod
    def get_error_message(exception: "ApplicationException") -> None: ...

    @property
    @abstractmethod
    def message(self) -> str: ...
