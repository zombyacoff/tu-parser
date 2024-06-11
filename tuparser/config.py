from .constants import LAUNCH_TIME
from .exceptions.config import (
    ConfigNotFoundError,
    InvalidConfigError,
    InvalidOffsetValueError,
    InvalidReleaseDateError,
    InvalidTitleError,
)
from .file_operations.file_manager import FileManager
from .utils import get_monthrange


class ConfigValidator:
    @staticmethod
    def offset(offset, value: any) -> int:
        if not offset:
            return 1

        if not (isinstance(value, int) and 2 <= value <= 250):
            raise InvalidOffsetValueError(value=value)

        return value

    @staticmethod
    def years(release_date, years: any) -> list[int] | None:
        if not release_date:
            return None

        if not (
            isinstance(years, list)  # years is not a list
            and all(
                isinstance(year, int) and 0 <= year <= LAUNCH_TIME.year
                for year in years
            )  # all years are integer and in range 0-250
        ):
            raise InvalidReleaseDateError(years=years)

        return years

    @staticmethod
    def titles(titles: any) -> list[str]:
        if not isinstance(titles, list) or any(
            title is None for title in titles
        ):  # titles is not a list and at least one title is None
            raise InvalidTitleError(titles=titles)

        return titles


class Config:
    def __init__(self, config_file_path: str) -> None:
        self.config_file_path = config_file_path
        self.load_config()
        try:
            self.parse_config()
        except (KeyError, TypeError) as e:
            raise InvalidConfigError(e)
        self.calculate_totals()

    def load_config(self) -> None:
        try:
            self.config = FileManager.load_yaml(self.config_file_path)
        except FileNotFoundError:
            raise ConfigNotFoundError(path=self.config_file_path)

    def parse_config(self) -> None:
        self.offset = self.config["offset"]["offset"]
        self.offset_value = ConfigValidator.offset(
            self.offset, self.config["offset"]["value"]
        )
        self.release_date = self.config["release_date"]["release_date"]
        self.years = ConfigValidator.years(
            self.release_date, self.config["release_date"]["years"]
        )
        self.titles = ConfigValidator.titles(self.config["titles"])
        self.progress_bar = self.config["progress_bar"]

    def calculate_totals(self) -> None:
        self.total_months = (
            LAUNCH_TIME.month
            if self.release_date and self.years == [LAUNCH_TIME.year]
            else 12
        )
        self.total_days = (
            sum(
                get_monthrange(month)
                for month in range(1, self.total_months + 1)
            )
            if self.total_months != 12
            else 366
        )
        self.total_urls = (
            len(self.titles) * self.offset_value * self.total_days
        )
