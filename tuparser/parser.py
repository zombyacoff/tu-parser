import asyncio
from abc import ABC, abstractmethod
from typing import Generator

import aiohttp
from bs4 import BeautifulSoup

from .constants import LAUNCH_TIME, TELEGRAPH_URL
from .exceptions import ApplicationException
from .extensions import ProgressBar
from .file_handling import YAMLOutputFile
from .utils import ConsoleColor, call_counter, get_monthrange, get_time_now
from .validator import validate

HTTP_OK_STATUS = 200
SEMAPHORE_MAX_LIMIT = 150

PARSING_START_MESSAGE = """Parsing has started...
Do not turn off the program until the process is completed!\n"""
SUCCESS_COMPLETE_TITLE = "SUCCESSFULLY COMPLETED"
TIME_ELAPSED_TEXT = "Time elapsed: {time}"


class TelegraphParser(ABC):
    def __init__(self, required_args: tuple[any]) -> None:
        self.titles, self.offset, self.progress_bar, self.release_dates = required_args

        self.total_months = LAUNCH_TIME.month if self.release_dates == [LAUNCH_TIME.year] else 12
        self.total_days = (
            sum(get_monthrange(month) for month in range(1, self.total_months + 1))
            if self.total_months != 12
            else 366
        )
        self.total_urls = len(self.titles) * self.offset * self.total_days

    async def __process_url(self, url: str) -> None:
        async with self.session.get(url) as page:
            if page.status != HTTP_OK_STATUS:
                return
            soup = BeautifulSoup(await page.text(), "html.parser")

        if not self.__check_release_date(soup):
            return

        await self.parse(url, soup)

    @abstractmethod
    async def parse(self, url: str, soup: BeautifulSoup) -> None: ...

    @call_counter
    def __get_progress_bar(self) -> None:
        if not self.progress_bar:
            return
        ProgressBar.show(self.__get_progress_bar.calls, self.total_urls)

    def __check_release_date(self, soup: BeautifulSoup) -> bool:
        if self.release_dates is None:
            return True

        time_element = soup.select_one("time")
        release_date = (
            int(time_element.get_text("\n", strip=True)[-4:]) if time_element else LAUNCH_TIME.year
        )
        return release_date in self.release_dates

    def get_complete_message(self) -> None:
        elapsed_time = get_time_now() - LAUNCH_TIME
        print(
            ConsoleColor.paint_success(SUCCESS_COMPLETE_TITLE)
            + " " * (ProgressBar.get_length(self.total_urls) - len(SUCCESS_COMPLETE_TITLE)),
            ConsoleColor.paint_info(TIME_ELAPSED_TEXT.format(time=elapsed_time)),
            sep="\n",
        )

    def __generate_urls(self) -> Generator[str, None, None]:
        for month in range(1, self.total_months + 1):
            for day in range(1, get_monthrange(month) + 1):
                for offset in range(1, self.offset + 1):
                    for title in self.titles:
                        url = f"{TELEGRAPH_URL}/{title}-{month:02}-{day:02}"
                        yield (f"{url}-{offset}" if offset > 1 else url)

    async def __semaphore_process(
        self,
        url: str,
        semaphore: asyncio.Semaphore,
    ) -> None:
        async with semaphore:
            await self.__process_url(url)

    async def main(self) -> None:
        print(ConsoleColor.paint_info(PARSING_START_MESSAGE))

        semaphore = asyncio.Semaphore(SEMAPHORE_MAX_LIMIT)
        urls_generator = self.__generate_urls()
        async with aiohttp.ClientSession() as self.session:
            processes = [self.__semaphore_process(url, semaphore) for url in urls_generator]
            for process in asyncio.as_completed(processes):
                await process
                self.__get_progress_bar()

        self.get_complete_message()

        # complete 'output file' if child class
        # has an attribute whose type is YAMLOutputFile
        for _, attr_value in vars(self).items():
            if isinstance(attr_value, YAMLOutputFile):
                attr_value.complete()
                print(
                    ConsoleColor.paint_info(
                        f"Output file path: {self.output_file.file_path}",
                    )
                )
                break


def run_parser(
    parser_class: TelegraphParser,
    *,
    titles: list[any],
    offset: int = 1,
    progress_bar: bool = True,
    release_dates: tuple[int] | None = None,
    parser_args: list[any] | None = None,
) -> None:
    """Starts the parser

    Required arguments:
    :param parser_class: (TelegraphParser) the parser class, which must inherit from TelegraphParser

    Optional configuration arguments:
    :param titles: (List[any]) the titles of the telegraph articles. Values must be a list without None
    :param parser_args: (List[any]) arguments passed to the constructor of the parser class.
    :param offset: (Integer) the number of articles to parse per day. Value must be an integer and must be between 1 and 250 inclusive
    :param progress_bar: (Boolean) whether to display a progress bar or not. Value must be a boolean
    :param release_dates: (Tuple[int]) the years when the articles should be parsed. Values must be a list of integers and must be within the specified range [0, LAUNCH_TIME_YEAR]
    """
    try:
        required_args = validate(titles, offset, progress_bar, release_dates)
        parser = (
            parser_class(required_args)
            if parser_args is None
            else parser_class(required_args, *parser_args)
        )
        asyncio.run(parser.main())
    except ApplicationException as exception:
        exception.get_error_message(exception)
