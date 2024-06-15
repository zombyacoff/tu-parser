from .constants import LAUNCH_TIME
from .exceptions import ConfigNotFoundError, InvalidConfigError
from .file_handling import FileManager
from .utils import get_monthrange
from .validator import validate

__all__ = ["Config"]

INVALID_OFFSET_MESSAGE = "Invalid offset value: {value}\n(value must be an integer greater than 2 and less than 250)"
INVALID_YEARS_MESSAGE = "Invalid years in release date: {value}"
INVALID_TITLES_MESSAGE = "Invalid titles: {value}"
INVALID_PROGRESS_BAR_MESSAGE = "Invalid progress bar value: {value}\n(value must be a boolean)"


class Config:

    def __init__(self, config_file_path: str) -> None:
        self.config_file_path = config_file_path
        self.__load_config()
        try:
            self.parse_config()
        except (KeyError, TypeError) as error:
            raise InvalidConfigError(error)
        self.__calculate_totals()

    def __load_config(self) -> None:
        self.config = FileManager.load_yaml(self.config_file_path)
        if self.config is None:
            raise ConfigNotFoundError(path=self.config_file_path)

    def parse_config(self) -> None:
        """Parses the configuration YAML file
        
        Your own config-parser should be structured as follows:
            self.{NAME} = self.config[{CONFIGURATION_PARAMETER_NAME}]
            
        Example:
            self.offset = self.config["offset"]
            
        NOTE: if you want to validate the parameter value, use the validate() function
        """
        self.offset = validate(
            self.config["offset"],
            "integer",
            default_value=1,
            value_range=(2, 250),
            exception_message=INVALID_OFFSET_MESSAGE,
        )
        self.release_date = validate(
            self.config["release_date"],
            "integer_list",
            value_range=(0, LAUNCH_TIME.year),
            exception_message=INVALID_YEARS_MESSAGE,
        )
        self.titles = validate(
            self.config["titles"],
            "any_list_wn",
            exception_message=INVALID_TITLES_MESSAGE,
        )
        self.progress_bar = validate(
            self.config["progress_bar"],
            "boolean",
            exception_message=INVALID_PROGRESS_BAR_MESSAGE,
        )

    def __calculate_totals(self) -> None:
        self.total_months = (LAUNCH_TIME.month if self.release_date
                             == [LAUNCH_TIME.year] else 12)
        self.total_days = (sum(
            get_monthrange(month)
            for month in range(1, self.total_months +
                               1)) if self.total_months != 12 else 366)
        self.total_urls = len(self.titles) * self.offset * self.total_days
