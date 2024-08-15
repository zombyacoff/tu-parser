from calendar import monthrange
from datetime import datetime

LEAP_YEAR = 2020


def get_time_now() -> datetime:
    return datetime.now()


def get_days_in_month(month: int) -> int:
    return monthrange(LEAP_YEAR, month)[1]
