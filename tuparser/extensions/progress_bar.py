from ..constants import LAUNCH_TIME
from ..utils import get_elapsed_time

FULL_CHAR = "█"
HALF_CHAR = "▒"

RAW_PROGRESS_BAR_LENGTH = 75


class ProgressBar:
    def __init__(self, total: int) -> None:
        self.current = 1
        self.total = total

    def show(self) -> None:
        percent = 100 * self.current / self.total
        current_bar_length = round(percent) // 2
        bar = current_bar_length * FULL_CHAR + (50 - current_bar_length) * HALF_CHAR

        print(bar, f"{percent:.2f}%", f"[{self.current}/{self.total}]", f"[{get_elapsed_time(LAUNCH_TIME)}]", end="\r")

        self.current += 1

    @property
    def length(self) -> int:
        return RAW_PROGRESS_BAR_LENGTH + len(str(self.total)) * 2
