from abc import ABC, abstractmethod


class ApplicationException(ABC, Exception):

    @staticmethod
    @abstractmethod
    def get_error_message(exception: "ApplicationException") -> str:
        """Print the error message for the exception in console"""

    @property
    @abstractmethod
    def message(self) -> str:
        """Error message for exception"""
