from .constants import LAUNCH_TIME
from .exceptions import (
    ConfigNotFoundError,
    InvalidConfigError,
    InvalidOffsetValueError,
    InvalidReleaseDateError,
    InvalidTitleError,
)
from .file_handling import FileManager
from .utils import get_monthrange


class ConfigAPI:
    @staticmethod
    def get_offset(offset: any) -> int:
        # if offset is disabled in the config
        if offset is False:
            return 1

        # at least one offset value is not an integer
        # or the value is not between 2 and 250
        if not (isinstance(offset, int) and 2 <= offset <= 250):
            raise InvalidOffsetValueError(value=offset)

        return offset

    @staticmethod
    def get_years(release_date: any) -> list[int] | None:
        # if release_date is disabled in the config
        if release_date is False:
            return None

        # release_date is not a list
        # at least one year is not an integer
        # or is not between 0 and 'CURRENT YEAR'
        if not (
            isinstance(release_date, list)
            and all(
                isinstance(year, int) and 0 <= year <= LAUNCH_TIME.year
                for year in release_date
            )
        ):
            raise InvalidReleaseDateError(years=release_date)

        return release_date

    @staticmethod
    def get_titles(titles: any) -> list[str]:
        # titles is not a list
        # or at least one title is None
        if not isinstance(titles, list) or any(
            title is None for title in titles
        ):
            raise InvalidTitleError(titles=titles)

        return titles


class Config:
    def __init__(self, config_file_path: str) -> None:
        self.config_file_path = config_file_path
        self.load_config()
        try:
            self.parse_config()
        except (KeyError, TypeError) as error:
            raise InvalidConfigError(error)
        self.calculate_totals()

    def load_config(self) -> None:
        try:
            self.config = FileManager.load_yaml(self.config_file_path)
        except FileNotFoundError:
            raise ConfigNotFoundError(path=self.config_file_path)

    def parse_config(self) -> None:
        self.offset = ConfigAPI.get_offset(self.config["offset"])
        self.release_date = ConfigAPI.get_years(self.config["release_date"])
        self.titles = ConfigAPI.get_titles(self.config["titles"])
        self.progress_bar = self.config["progress_bar"]

    def calculate_totals(self) -> None:
        self.total_months = (
            LAUNCH_TIME.month
            if self.release_date == [LAUNCH_TIME.year]
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
        self.total_urls = len(self.titles) * self.offset * self.total_days
