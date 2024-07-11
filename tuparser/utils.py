import re
from calendar import monthrange
from datetime import datetime
from typing import Callable

from termcolor import colored


def get_time_now() -> datetime:
    return datetime.now()


def get_monthrange(month: int) -> int:
    return monthrange(2020, month)[1]


def uppercamelcase_split(sentence: str) -> str:
    return " ".join(re.findall(r"[A-Z][a-z]*", sentence))


def call_counter(func: Callable) -> Callable:
    """Decorator that counts the number of times a function is called"""

    def wrapper(*args, **kwargs) -> int:
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


class ConsoleColor:
    @staticmethod
    def paint_success(text: str) -> str:
        return colored(text, "green", attrs=["bold"])

    @staticmethod
    def paint_error(text: str) -> str:
        return colored(text, "red", attrs=["bold"])

    @staticmethod
    def paint_info(text: str) -> str:
        return colored(text, "yellow")
