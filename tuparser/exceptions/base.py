from ..utils import ConsoleColor
from .messages import ERROR_TITLE


class ParserException(Exception):
    """Base class for all application exceptions"""

    @staticmethod
    def get_error_message(exception: "ParserException") -> str:
        print(
            ConsoleColor.paint_error(ERROR_TITLE),
            exception.message,
            sep="\n",
        )
