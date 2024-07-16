import asyncio
from abc import ABC, abstractmethod
from typing import Generator

import aiohttp
from bs4 import BeautifulSoup

from .constants import LAUNCH_TIME, TELEGRAPH_URL
from .exceptions import ValidatorException
from .extensions import ProgressBar
from .file_handling import YAMLOutputFile
from .utils import ConsoleColor, get_elapsed_time, get_monthrange
from .validator import validate

HTTP_OK_STATUS = 200
SEMAPHORE_MAX_LIMIT = 150

PARSING_START_MESSAGE = "Parsing has started...\nDo not turn off the program until the process is completed!\n"
SUCCESS_COMPLETE_TITLE = "SUCCESSFULLY COMPLETED"
TIME_ELAPSED_TEXT = "Time elapsed: {}"


class TelegraphParser(ABC):
    def __init__(self, parser_args: dict[str, any]) -> None:
        self.titles = parser_args.get("titles")
        self.messages_enabled = parser_args.get("messages")
        self.offset = parser_args.get("offset")
        self.release_years = parser_args.get("release_years")

        output_file = parser_args.get("output_file")
        self.output_file = YAMLOutputFile(*output_file) if output_file else False

        self.total_months = LAUNCH_TIME.month if self.release_years == [LAUNCH_TIME.year] else 12
        self.total_days = (
            sum(get_monthrange(month) for month in range(1, self.total_months + 1)) if self.total_months != 12 else 366
        )
        self.total_urls = len(self.titles) * self.offset * self.total_days

        self.progress_bar = ProgressBar(self.total_urls) if parser_args.get("progress_bar") else False

    @abstractmethod
    async def parse(self, url: str, soup: BeautifulSoup) -> None: ...

    def __check_release_date(self, soup: BeautifulSoup) -> bool:
        if not self.release_years:
            return True

        time_element = soup.select_one("time")
        release_date = int(time_element.get_text("\n", strip=True)[-4:]) if time_element else LAUNCH_TIME.year
        return release_date in self.release_years

    async def __validate_url(self, url: str) -> None:
        async with self.session.get(url) as page:
            if page.status != HTTP_OK_STATUS:
                return
            soup = BeautifulSoup(await page.text(), "html.parser")

        if not self.__check_release_date(soup):
            return

        await self.parse(url, soup)

    def get_complete_message(self) -> None:
        whitespaces = " " * (self.progress_bar.length - len(SUCCESS_COMPLETE_TITLE)) if self.progress_bar else ""
        print(
            ConsoleColor.paint_success(SUCCESS_COMPLETE_TITLE) + whitespaces,
            ConsoleColor.paint_info(TIME_ELAPSED_TEXT.format(get_elapsed_time(LAUNCH_TIME))),
            sep="\n",
        )

        if self.output_file:
            print(ConsoleColor.paint_info(f"Output file path: {self.output_file.file_path}"))

    def __generate_urls(self) -> Generator[str, None, None]:
        for month in range(1, self.total_months + 1):
            for day in range(1, get_monthrange(month) + 1):
                for offset in range(1, self.offset + 1):
                    for title in self.titles:
                        url = f"{TELEGRAPH_URL}/{title}-{month:02}-{day:02}"
                        yield (f"{url}-{offset}" if offset > 1 else url)

    async def __semaphore_process(self, url: str) -> None:
        semaphore = asyncio.Semaphore(SEMAPHORE_MAX_LIMIT)
        async with semaphore:
            await self.__validate_url(url)

    async def __url_processing(self) -> None:
        urls_generator = self.__generate_urls()

        async with aiohttp.ClientSession() as self.session:
            processes = [self.__semaphore_process(url) for url in urls_generator]
            for process in asyncio.as_completed(processes):
                await process

                if self.progress_bar:
                    self.progress_bar.show()

        if self.output_file:
            self.output_file.complete()

    def main(self) -> None:
        if self.messages_enabled:
            print(ConsoleColor.paint_info(PARSING_START_MESSAGE))

        asyncio.run(self.__url_processing())

        if self.messages_enabled:
            self.get_complete_message()


def run_parser(
    parser_class: TelegraphParser,
    *,
    titles: list[any],
    custom_args: list[any] | None = None,
    messages: bool = True,
    offset: int = 1,
    output_file: list[any] = [],
    progress_bar: bool = True,
    release_years: list[int] = [],
) -> None:
    """Starts the parser

    Required arguments:
    :param parser_class: (TelegraphParser) the parser class, which must inherit from TelegraphParser
    :param titles: (List[any]) the titles of the telegraph articles. Values must be a list without None

    Optional configuration arguments:
    :param custom_args: (List[any]) arguments passed to the constructor of the parser class
    :param messages: (Boolean) whether to display the messages or not
    :param offset: (Integer) the number of articles to parse per day. Value must be an integer and must be between 1 and 250 inclusive

    :param progress_bar: (Boolean) whether to display a progress bar or not
    :param release_years: (List[int]) the years when the articles should be parsed. Values must be a list of integers and must be within the specified range [0, LAUNCH_TIME_YEAR]
    """

    # TODO: добавить :param output_file: в комментарий выше;
    # заменить "PLACEHOLDER" в validate функции на соответствующее сообщение;
    # посмотреть как реализованы комментарии в библиотеке telebot;
    # попробовать заменить кортеж parser_args на словарь

    try:
        parser_args = validate({
            "titles": titles,
            "messages": messages,
            "offset": offset,
            "output_file": output_file,
            "progress_bar": progress_bar,
            "release_years": release_years,
        })
    except ValidatorException as exception:
        exception.get_error_message(exception)
    else:
        parser = parser_class(parser_args) if custom_args is None else parser_class(parser_args, *custom_args)
        parser.main()
