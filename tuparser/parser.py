import asyncio
from abc import ABC, abstractmethod
from typing import Generator

import aiohttp
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm

from .constants import LAUNCH_TIME, TELEGRAPH_URL
from .exceptions import InvalidConfigurationError
from .output_file import YamlOutputFile
from .utils import ConsoleColor, get_monthrange, get_time_now
from .validator import validate_config


class TelegraphParser(ABC):
    SEMAPHORE_MAX_LIMIT = 150

    PROGRESS_BAR_FORMAT = (
        "|{bar:50}| {percentage:.2f}% [{n_fmt}/{total_fmt}] ({elapsed} < {remaining} | {rate_fmt}){postfix}"
    )

    def __init__(self, config: dict[str, any]) -> None:
        self.__dict__.update(config)
        self.total_months = LAUNCH_TIME.month if self.published_years == [LAUNCH_TIME.year] else 12

    def _get_total_urls(self) -> int:
        total_days = sum(get_monthrange(month) for month in range(1, self.total_months + 1))
        return len(self.titles) * self.offset * total_days

    def _check_published_year(self, soup: BeautifulSoup) -> bool:
        if not self.published_years:
            return True

        published_year = int(soup.find("meta", property="article:published_time").get("content")[:4])
        return published_year in self.published_years

    def _generate_urls(self) -> Generator[str, None, None]:
        for month in range(1, self.total_months + 1):
            for day in range(1, get_monthrange(month) + 1):
                for offset in range(1, self.offset + 1):
                    for title in self.titles:
                        url = f"{TELEGRAPH_URL}/{title}-{month:02}-{day:02}"
                        yield (url if offset == 1 else f"{url}-{offset}")

    async def _validate_url(self, url: str) -> None:
        async with self.session.get(url) as page:
            if page.status != 200:
                return
            soup = BeautifulSoup(await page.text(), "html.parser")

        if not self._check_published_year(soup):
            return

        await self.parse(url, soup)

    async def _semaphore_process(self, url: str, semaphore: asyncio.Semaphore) -> None:
        async with semaphore:
            await self._validate_url(url)

    async def _url_processing(self) -> None:
        urls_generator = self._generate_urls()
        semaphore = asyncio.Semaphore(self.SEMAPHORE_MAX_LIMIT)

        async with aiohttp.ClientSession() as self.session:
            tasks = [self._semaphore_process(url, semaphore) for url in urls_generator]
            completed_tasks = (
                tqdm(
                    asyncio.as_completed(tasks),
                    total=self._get_total_urls(),
                    bar_format=self.PROGRESS_BAR_FORMAT,
                    unit="URLs",
                    dynamic_ncols=True,
                    leave=False,
                )
                if self.progress_bar
                else asyncio.as_completed(tasks)
            )

            for task in completed_tasks:
                await task

        if self.output_file:
            self.output_file.complete()

    @abstractmethod
    async def parse(self, url: str, soup: BeautifulSoup) -> None:
        pass

    def main(self) -> None:
        if not self.messages:
            asyncio.run(self._url_processing())
            return

        print(
            ConsoleColor.paint_info(
                "Parsing has started...\nDo not turn off the program until the process is completed!\n"
            )
        )

        asyncio.run(self._url_processing())

        elapsed_time = str(get_time_now() - LAUNCH_TIME)[:7]
        print(
            ConsoleColor.paint_success("SUCCESSFULLY COMPLETED"),
            ConsoleColor.paint_info(f"Time elapsed: {elapsed_time}"),
            sep="\n",
        )

        if self.output_file:
            print(ConsoleColor.paint_info(f"Output file path: {self.output_file.file_path}"))


def run_parser(
    parser_class: TelegraphParser,
    *,
    titles: list,
    custom_args: list | None = None,
    messages: bool = True,
    offset: int = 1,
    output_file: YamlOutputFile | None = None,
    progress_bar: bool = True,
    published_years: list[int] | None = None,
) -> None:
    """
    Starts the parser

    Required arguments:
        :param parser_class: (TelegraphParser) the parser class, which must inherit from TelegraphParser
        :param titles: (list) the titles of the telegraph articles. Value must be a list without None

    Optional configuration arguments:
        :param custom_args: (list) arguments passed to the constructor of the parser class
        :param messages: (bool) whether to display the messages or not
        :param offset: (int) the number of articles to parse per day. Value must be an integer and must be between 1 and 250 inclusive
        :param output_file: (YamlOutputFile) the output file configuration. Value must be an instance of the YamlOutputFile class
        :param progress_bar: (bool) whether to display a progress bar or not
        :param published_years: (list[int]) the years when the articles should be parsed.\
        Value must be a list of integers and must be within the specified range [0, LAUNCH_TIME_YEAR]
    """
    try:
        config = validate_config({
            "titles": titles,
            "messages": messages,
            "offset": offset,
            "output_file": output_file,
            "progress_bar": progress_bar,
            "published_years": published_years,
        })
    except InvalidConfigurationError as exception:
        print(exception)
    else:
        parser = parser_class(config) if custom_args is None else parser_class(config, *custom_args)
        parser.main()
