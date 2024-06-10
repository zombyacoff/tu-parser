from .constants import LAUNCH_TIME
from .exceptions.config import (
    InvalidOffsetValueError,
    InvalidReleaseDateError,
    InvalidTitleError,
)


class ConfigValidator:
    @staticmethod
    def offset(offset_bool, value: any) -> int:
        if not offset_bool:
            return 1

        if not (isinstance(value, int) and 2 <= value <= 250):
            raise InvalidOffsetValueError(offset_value=value)

        return value

    @staticmethod
    def release_date(release_date_bool, years: list[any]) -> list[int] | None:
        if not release_date_bool:
            return None

        for year in years:
            if not (isinstance(year, int) and 0 <= year <= LAUNCH_TIME.year):
                raise InvalidReleaseDateError(year=year)

        return years

    @staticmethod
    def titles(titles: list[any]) -> list[str]:
        for title in titles:
            if not isinstance(title, str):
                raise InvalidTitleError(title=title)

        return titles
