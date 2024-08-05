from .utils import ConsoleColor


class TUParserException(Exception):
    def __init__(self, title: str, message: str):
        self.title = title
        self.message = message

    def __str__(self):
        return f"{ConsoleColor.paint_error(self.title)}\n{ConsoleColor.paint_info(self.message)}"


class InvalidConfigurationError(TUParserException):
    def __init__(self, error_message: str):
        super().__init__(title="INVALID TELEGRAPH PARSER CONFIGURATION", message=error_message)
