from abc import ABC, abstractmethod


class ApplicationException(ABC, Exception):

    @staticmethod
    @abstractmethod
    def get_error_message(exception: "ApplicationException") -> str:
        ...

    @property
    @abstractmethod
    def message(self) -> str:
        ...
