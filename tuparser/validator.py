from abc import ABC, abstractmethod

from .constants import LAUNCH_TIME
from .output_file import YamlOutputFile


class Validator(ABC):
    __slots__ = ("value",)

    def __get__(self, obj, objtype=None) -> any:
        return self.value

    def __set__(self, obj, value: any) -> any:
        self.validate(value)
        self.value = value

    @abstractmethod
    def validate(self, value: any) -> None: ...


class TitlesValidation(Validator):
    def validate(self, value: list) -> None:
        if not isinstance(value, list) or not value:
            raise ValueError("Titles must be a non-empty list")


class OffsetValidation(Validator):
    MAX_OFFSET = 250

    def validate(self, value: int) -> None:
        if not isinstance(value, int) or not (1 <= value <= self.MAX_OFFSET):
            raise ValueError(f"Offset must be an integer between 1 and {self.MAX_OFFSET}")


class OutputFileValidation(Validator):
    def validate(self, value: YamlOutputFile | None) -> None:
        if value is not None and not isinstance(value, YamlOutputFile):
            raise ValueError("Output file must be an instance of YamlOutputFile or None")


class PublishedYearsValidation(Validator):
    def validate(self, value: list[int] | None) -> None:
        if value is not None and (
            not isinstance(value, list)
            or any(not isinstance(year, int) or not (0 <= year <= LAUNCH_TIME.year) for year in value)
        ):
            raise ValueError(f"Published years must be a list of integers between 0 and {LAUNCH_TIME.year} or None")
