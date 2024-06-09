import asyncio

from .config.base import Config
from .exceptions.base import ParserException
from .exceptions.config import (
    ConfigNotFoundError,
    InvalidConfigError,
    InvalidOffsetValueError,
    InvalidReleaseDateError,
    InvalidWebsiteURLError,
)
from .parser.base import TelegraphParser


def run_parser(
    config_class: Config,
    parser_class: TelegraphParser,
    parser_arguments: tuple[any] | None = None,
) -> None:
    try:
        config = config_class()
        parser = (
            parser_class(config)
            if parser_arguments is None
            else parser_class(config, *parser_arguments)
        )
    except (
        ConfigNotFoundError,
        InvalidConfigError,
        InvalidWebsiteURLError,
        InvalidReleaseDateError,
        InvalidOffsetValueError,
    ) as exception:
        ParserException.get_error_message(exception)
    else:
        asyncio.run(parser.main())
