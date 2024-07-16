import re
from calendar import monthrange
from datetime import datetime, timedelta

from termcolor import colored


def get_time_now() -> datetime:
    return datetime.now()


def get_formatted_time(time: timedelta) -> str:
    hours, remainder = divmod(time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"


def get_monthrange(month: int) -> int:
    return monthrange(2020, month)[1]


def uppercamelcase_split(sentence: str) -> str:
    return " ".join(re.findall(r"[A-Z][a-z]*", sentence))


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
