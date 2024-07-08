from calendar import monthrange
from datetime import datetime
from typing import Callable

from termcolor import colored


def get_time_now() -> datetime:
    return datetime.now()


def get_monthrange(month: int) -> int:
    """Returns the number of days in a given month"""
    return monthrange(2020, month)[1]


def call_counter(func: Callable) -> Callable:
    """Decorator that counts the number of times a function is called

    Usage:
        {FUNCTION_NAME}.calls

    Example:
        @call_counter
        def example_func():
            print(example_func.calls)

        example_func()  # 1
        example_func()  # 2
    """

    def wrapper(*args, **kwargs) -> int:
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


class ConsoleColor:
    @staticmethod
    def paint_success(text: str) -> str:
        """Paints the given text in bold green"""
        return colored(text, "green", attrs=["bold"])

    @staticmethod
    def paint_error(text: str) -> str:
        """Paints the given text in bold red"""
        return colored(text, "red", attrs=["bold"])

    @staticmethod
    def paint_info(text: str) -> str:
        """Paints the given text in yellow"""
        return colored(text, "yellow")
