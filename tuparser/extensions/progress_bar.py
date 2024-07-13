FULL_CHAR = "█"
HALF_CHAR = "▒"

RAW_PROGRESS_BAR_LENGTH = 64


class ProgressBar:
    @staticmethod
    def show(current: int, total: int) -> None:
        percent = 100 * current / total
        current_bar_length = round(percent) // 2
        bar = current_bar_length * FULL_CHAR + (50 - current_bar_length) * HALF_CHAR
        print(bar, "[{current}/{total}]", "[{percent:.2f}%]", end="\r")

    @staticmethod
    def get_length(total: int) -> int:
        return RAW_PROGRESS_BAR_LENGTH + len(str(total)) * 2
