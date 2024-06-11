import asyncio
from abc import ABC, abstractmethod
from typing import Generator

import aiohttp
from bs4 import BeautifulSoup

from .config import Config
from .constants import (
    LAUNCH_TIME,
    PARSING_START_MESSAGE,
    SEMAPHORE_MAX_LIMIT,
    SUCCESS_COMPLETE_TITLE,
    TELEGRAPH_URL,
    TIME_ELAPSED_TEXT,
)
from .exceptions.config import (
    ConfigNotFoundError,
    InvalidConfigError,
    InvalidOffsetValueError,
    InvalidReleaseDateError,
    InvalidTitleError,
)
from .extensions.progress_bar import ProgressBar
from .utils import ConsoleColor, get_monthrange, get_time_now


class TelegraphParser(ABC):
    def __init__(self, config: Config) -> None:
        self.config = config
        self.bar_counter = 0

    async def process_url(self, url: str) -> None:
        async with self.session.get(url) as page:
            if page.status != 200:
                return None
            soup = BeautifulSoup(await page.text(), "html.parser")

        if not self.__check_release_date(soup):
            return None

        # print(f"Processing {url}")
        await self.parse(url, soup)

    @abstractmethod
    async def parse(self, url: str, soup: BeautifulSoup) -> None: ...

    def __get_progress_bar(self) -> None:
        if not self.config.progress_bar:
            return
        ProgressBar.show(self.bar_counter, self.config.total_urls)
        self.bar_counter += 1

    def __check_release_date(self, soup: BeautifulSoup) -> bool:
        if not self.config.release_date:
            return True

        time_element = soup.select_one("time")
        release_date = (
            int(time_element.get_text("\n", strip=True)[-4:])
            if time_element
            else LAUNCH_TIME.year
        )
        return release_date in self.config.years

    def get_complete_message(self) -> None:
        elapsed_time = get_time_now() - LAUNCH_TIME
        print(
            ConsoleColor.paint_success(SUCCESS_COMPLETE_TITLE)
            + " "
            * (
                ProgressBar.get_length(self.config.total_urls)
                - len(SUCCESS_COMPLETE_TITLE)
            ),
            ConsoleColor.paint_info(
                TIME_ELAPSED_TEXT.format(time=elapsed_time)
            ),
            sep="\n",
        )

    def __generate_urls(self) -> Generator[str, None, None]:
        for month in range(1, self.config.total_months + 1):
            for day in range(1, get_monthrange(month) + 1):
                for offset in range(1, self.config.offset_value + 1):
                    for title in self.config.titles:
                        yield (
                            f"{TELEGRAPH_URL}/{title}-{month:02}-{day:02}-{offset}"
                            if offset > 1
                            else f"{TELEGRAPH_URL}/{title}-{month:02}-{day:02}"
                        )

    async def __semaphore_process(
        self,
        url: str,
        semaphore: asyncio.Semaphore,
    ) -> None:
        async with semaphore:
            await self.process_url(url)

    async def main(self) -> None:
        print(ConsoleColor.paint_info(PARSING_START_MESSAGE))

        semaphore = asyncio.Semaphore(SEMAPHORE_MAX_LIMIT)
        urls_generator = self.__generate_urls()
        async with aiohttp.ClientSession() as self.session:
            processes = [
                self.__semaphore_process(url, semaphore)
                for url in urls_generator
            ]
            for process in asyncio.as_completed(processes):
                self.__get_progress_bar()
                await process

        self.get_complete_message()


def run_parser(
    config_class: Config,
    parser_class: TelegraphParser,
    parser_args: tuple[any] | None = None,
    config_path: str = "config.yml",
) -> None:
    try:
        # init classes
        config = config_class(config_path)
        parser = (
            parser_class(config)
            if parser_args is None
            else parser_class(config, *parser_args)
        )
        # start parsing
        asyncio.run(parser.main())
    except (
        # config exceptions
        ConfigNotFoundError,
        InvalidConfigError,
        InvalidReleaseDateError,
        InvalidOffsetValueError,
        InvalidTitleError,
    ) as exception:
        exception.get_error_message(exception)
