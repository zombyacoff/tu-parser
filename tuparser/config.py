from .constants import LAUNCH_TIME
from .exceptions.config import ConfigNotFoundError, InvalidConfigError
from .file_operations.file_manager import FileManager
from .utils import get_monthrange
from .validator import ConfigValidator


class Config:
    def __init__(self, config_file_name: str = "config.yml") -> None:
        self.config_file_name = config_file_name
        self.load_config()
        try:
            self.parse_config()
        except (KeyError, TypeError) as e:
            raise InvalidConfigError(e) from None
        self.calculate_totals()

    def load_config(self) -> None:
        try:
            self.config = FileManager.load_yaml(self.config_file_name)
        except FileNotFoundError:
            raise ConfigNotFoundError from None

    def parse_config(self) -> None:
        self.offset_bool = self.config["offset"]["offset"]
        self.offset_value = ConfigValidator.offset(
            self.offset_bool, self.config["offset"]["value"]
        )
        self.release_date_bool = self.config["release_date"]["release_date"]
        self.release_date = ConfigValidator.release_date(
            self.release_date_bool, self.config["release_date"]["years"]
        )
        self.titles = ConfigValidator.titles(self.config["titles"])
        self.progress_bar_bool = self.config["progress_bar"]

    def calculate_totals(self) -> None:
        self.total_months = (
            LAUNCH_TIME.month
            if self.release_date_bool
            and self.release_date == [LAUNCH_TIME.year]
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
