from abc import ABC, abstractmethod


class ApplicationException(ABC, Exception):
    # method get_error_message
    # should be present in every GENERAL exception
    @staticmethod
    @abstractmethod
    def get_error_message(exception: "ApplicationException") -> str:
        """Get the error message for the exception"""

    # method message
    # should be present in every exception
    @property
    @abstractmethod
    def message(self) -> str:
        """Error message for exception"""
