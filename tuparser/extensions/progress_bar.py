from ..constants import LAUNCH_TIME
from ..utils import get_elapsed_time

FULL_CHAR = "█"
HALF_CHAR = "▒"

RAW_PROGRESS_BAR_LENGTH = 75


class ProgressBar:
    def __init__(self, total: int) -> None:
        self.total = total
        self.current = 0

    def update(self) -> None:
        self.current += 1
        percent = self.__calculate_percent()
        bar = self.__generate_bar(percent)
        self.__print_progress(bar, percent)

    def __calculate_percent(self) -> float:
        return 100 * self.current / self.total

    def __generate_bar(self, percent: float) -> str:
        current_bar_length = int(percent // 2)
        return FULL_CHAR * current_bar_length + HALF_CHAR * (50 - current_bar_length)

    def __print_progress(self, bar: str, percent: float) -> None:
        if self.current == 1:
            print()

        print(f"{bar} {percent:.2f}% [{self.current}/{self.total}] [{get_elapsed_time(LAUNCH_TIME)}]", end="\r")

        if self.current == self.total:
            print("\n")

    @property
    def length(self) -> int:
        return RAW_PROGRESS_BAR_LENGTH + len(str(self.total)) * 2
