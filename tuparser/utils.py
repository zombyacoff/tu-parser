from calendar import monthrange
from datetime import datetime


def get_time_now() -> datetime:
    return datetime.now()


def get_days_in_month(month: int) -> int:
    return monthrange(2020, month)[1]
