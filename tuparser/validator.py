from abc import ABC, abstractmethod

from .constants import LAUNCH_TIME


class Validator(ABC):
    __slots__ = ("value",)

    def __get__(self, obj, objtype=None) -> any:
        return self.value

    def __set__(self, obj, value: any) -> None:
        self.validate(value)
        self.value = value

    @abstractmethod
    def validate(self, value: any) -> None: ...


class TitlesValidation(Validator):
    def validate(self, value: list) -> None:
        if not isinstance(value, list) or not value:
            raise ValueError("Titles must be a non-empty list")


class OffsetValidation(Validator):
    def validate(self, value: int) -> None:
        if not isinstance(value, int) or not (1 <= value <= 250):
            raise ValueError("Offset must be an integer between 1 and 250")


class PublishedYearsValidation(Validator):
    def validate(self, value: list[int] | None) -> None:
        if value is not None and (
            not isinstance(value, list)
            or any(not isinstance(year, int) or not (0 <= year <= LAUNCH_TIME.year) for year in value)
        ):
            raise ValueError(f"Published years must be a list of integers between 0 and {LAUNCH_TIME.year}")
