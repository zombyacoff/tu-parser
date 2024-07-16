import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, Generator, List, Optional

import aiohttp
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm

from .constants import LAUNCH_TIME, TELEGRAPH_URL
from .exceptions import InvalidSettingsError
from .file_handling import YAMLOutputFile
from .utils import ConsoleColor, get_elapsed_time, get_monthrange
from .validator import validate

HTTP_OK_STATUS = 200
SEMAPHORE_MAX_LIMIT = 150

PROGRESS_BAR_FORMAT = "{bar} {percentage:.2f}% [{n_fmt}/{total_fmt}] [{elapsed} < {remaining} : {rate_fmt} {postfix}]"

PARSING_START_MESSAGE = "Parsing has started...\nDo not turn off the program until the process is completed!"
SUCCESS_COMPLETE_TITLE = "SUCCESSFULLY COMPLETED"
TIME_ELAPSED_TEXT = "Time elapsed: {}"


class TelegraphParser(ABC):
    def __init__(self, settings: Dict[str, Any]) -> None:
        self.titles = settings.get("titles")
        self.messages_enabled = settings.get("messages")
        self.offset = settings.get("offset")
        self.published_years = settings.get("published_years")
        self.progress_bar = settings.get("progress_bar")

        output_file = settings.get("output_file")
        self.output_file = YAMLOutputFile(*output_file) if output_file else False

        self.total_months = LAUNCH_TIME.month if self.published_years == [LAUNCH_TIME.year] else 12

    def __get_total_urls(self) -> int:
        total_days = (
            sum(get_monthrange(month) for month in range(1, self.total_months + 1)) if self.total_months != 12 else 366
        )
        return len(self.titles) * self.offset * total_days

    @abstractmethod
    async def parse(self, url: str, soup: BeautifulSoup) -> None: ...

    def __check_release_date(self, soup: BeautifulSoup) -> bool:
        if not self.published_years:
            return True

        published_year = soup.find("meta", property="article:published_time").get("content")[:4]
        return published_year in self.published_years

    async def __validate_url(self, url: str) -> None:
        async with self.session.get(url) as page:
            if page.status != HTTP_OK_STATUS:
                return
            soup = BeautifulSoup(await page.text(), "html.parser")

        if not self.__check_release_date(soup):
            return

        await self.parse(url, soup)

    def __generate_urls(self) -> Generator[str, None, None]:
        for month in range(1, self.total_months + 1):
            for day in range(1, get_monthrange(month) + 1):
                for offset in range(1, self.offset + 1):
                    for title in self.titles:
                        url = f"{TELEGRAPH_URL}/{title}-{month:02}-{day:02}"
                        yield (f"{url}-{offset}" if offset > 1 else url)

    async def __semaphore_process(self, url: str, semaphore: asyncio.Semaphore) -> None:
        async with semaphore:
            await self.__validate_url(url)

    async def __url_processing(self) -> None:
        urls_generator = self.__generate_urls()
        semaphore = asyncio.Semaphore(SEMAPHORE_MAX_LIMIT)

        async with aiohttp.ClientSession() as self.session:
            tasks = [self.__semaphore_process(url, semaphore) for url in urls_generator]
            tasks_iter = asyncio.as_completed(tasks)
            if self.progress_bar:
                tasks_iter = tqdm(
                    tasks_iter,
                    bar_format=PROGRESS_BAR_FORMAT,
                    total=self.__get_total_urls(),
                    leave=False,
                    dynamic_ncols=True,
                )

            for task in tasks_iter:
                await task

        if self.output_file:
            self.output_file.complete()

    def main(self) -> None:
        if self.messages_enabled:
            print(ConsoleColor.paint_info(PARSING_START_MESSAGE))

        asyncio.run(self.__url_processing())

        if self.messages_enabled:
            print(
                ConsoleColor.paint_success(SUCCESS_COMPLETE_TITLE),
                ConsoleColor.paint_info(TIME_ELAPSED_TEXT.format(get_elapsed_time(LAUNCH_TIME))),
                sep="\n",
            )

            if self.output_file:
                print(ConsoleColor.paint_info(f"Output file path: {self.output_file.file_path}"))


def run_parser(
    parser_class: TelegraphParser,
    *,
    titles: List[Any],
    custom_args: Optional[List[Any]] = None,
    messages: bool = True,
    offset: int = 1,
    output_file: Optional[List[Any]] = None,
    progress_bar: bool = True,
    published_years: Optional[List[Any]] = None,
) -> None:
    """Starts the parser

    Required arguments:
    :param parser_class: (TelegraphParser) the parser class, which must inherit from TelegraphParser
    :param titles: (List[Any]) the titles of the telegraph articles. Values must be a list without None

    Optional configuration arguments:
    :param custom_args: (List[Any]) arguments passed to the constructor of the parser class
    :param messages: (bool) whether to display the messages or not
    :param offset: (Integer) the number of articles to parse per day. Value must be an integer and must be between 1 and 250 inclusive
    :param output_file: (List[Any]) the output file configuration
    :param progress_bar: (bool) whether to display a progress bar or not
    :param published_years: (List[int]) the years when the articles should be parsed. Values must be a list of integers and must be within the specified range [0, LAUNCH_TIME_YEAR]
    """

    try:
        settings = validate({
            "titles": titles,
            "messages": messages,
            "offset": offset,
            "output_file": output_file,
            "progress_bar": progress_bar,
            "published_years": published_years,
        })
    except InvalidSettingsError as exception:
        exception.get_error_message(exception)
    else:
        parser = parser_class(settings) if custom_args is None else parser_class(settings, *custom_args)
        parser.main()
