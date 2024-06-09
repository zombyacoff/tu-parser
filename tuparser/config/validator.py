from ..constants import LAUNCH_TIME
from ..exceptions.config import InvalidOffsetValueError, InvalidReleaseDateError


class ConfigValidator:
    @staticmethod
    def offset(offset_bool, value: any) -> int:
        if not offset_bool:
            return 1

        if not (isinstance(value, int) and 2 <= value <= 250):
            raise InvalidOffsetValueError(offset_value=value)

        return value

    @staticmethod
    def release_date(release_date_bool, values: list[any]) -> list[int] | None:
        if not release_date_bool:
            return None

        for value in values:
            if not (isinstance(value, int) and 0 <= value <= LAUNCH_TIME.year):
                raise InvalidReleaseDateError(release_date=value)

        return values
