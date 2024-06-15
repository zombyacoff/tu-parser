import asyncio
from abc import ABC, abstractmethod
from typing import Generator

import aiohttp
from bs4 import BeautifulSoup

from .config import Config
from .constants import LAUNCH_TIME, TELEGRAPH_URL
from .exceptions import ApplicationException
from .extensions import ProgressBar
from .file_handling import YAMLOutputFile
from .utils import ConsoleColor, call_counter, get_monthrange, get_time_now

__all__ = ["TelegraphParser", "run_parser"]

SEMAPHORE_MAX_LIMIT = 150
PARSING_START_MESSAGE = """Parsing has started...
Do not turn off the program until the process is completed!\n"""
SUCCESS_COMPLETE_TITLE = "SUCCESSFULLY COMPLETED"
TIME_ELAPSED_TEXT = "Time elapsed: {time}"


class TelegraphParser(ABC):

    def __init__(self, config: Config) -> None:
        self.config = config

    async def __process_url(self, url: str) -> None:
        async with self.session.get(url) as page:
            if page.status != 200:
                return
            soup = BeautifulSoup(await page.text(), "html.parser")

        if not self.__check_release_date(soup):
            return

        await self.parse(url, soup)

    @abstractmethod
    async def parse(self, url: str, soup: BeautifulSoup) -> None:
        ...

    @call_counter
    def __get_progress_bar(self) -> None:
        if not self.config.progress_bar:
            return
        ProgressBar.show(self.__get_progress_bar.calls, self.config.total_urls)

    def __check_release_date(self, soup: BeautifulSoup) -> bool:
        if self.config.release_date is None:
            return True

        time_element = soup.select_one("time")
        release_date = (int(time_element.get_text("\n", strip=True)[-4:])
                        if time_element else LAUNCH_TIME.year)
        return release_date in self.config.release_date

    def get_complete_message(self) -> None:
        elapsed_time = get_time_now() - LAUNCH_TIME
        print(
            ConsoleColor.paint_success(SUCCESS_COMPLETE_TITLE) + " " *
            (ProgressBar.get_length(self.config.total_urls) -
             len(SUCCESS_COMPLETE_TITLE)),
            ConsoleColor.paint_info(
                TIME_ELAPSED_TEXT.format(time=elapsed_time)),
            sep="\n",
        )

    def __generate_urls(self) -> Generator[str, None, None]:
        for month in range(1, self.config.total_months + 1):
            for day in range(1, get_monthrange(month) + 1):
                for offset in range(1, self.config.offset + 1):
                    for title in self.config.titles:
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
            processes = [
                self.__semaphore_process(url, semaphore)
                for url in urls_generator
            ]
            for process in asyncio.as_completed(processes):
                self.__get_progress_bar()
                await process

        self.get_complete_message()

        # complete 'output file' if child class
        # has an attribute whose type is YAMLOutputFile
        for _, attr_value in vars(self).items():
            if isinstance(attr_value, YAMLOutputFile):
                attr_value.complete()
                break


def run_parser(parser_class: TelegraphParser,
               *,
               config_class: Config = Config,
               parser_args: list[any] | None = None,
               config_path: str = "config") -> None:
    """Starts the parser
    
    Required arguments:
    :param parser_class: (TelegraphParser) the parser class, 
    which must inherit from TelegraphParser
    
    Optional configuration arguments:
    :param config_class: (Config) custom configuration class, 
    which must inherit from Config. Default value: Config class
    :param parser_args: (List) arguments passed to the constructor of the parser class
    :param config_path: (String) path to the configuration file. Default value: 'config'
    """
    try:
        config = config_class(config_path)
        parser = (parser_class(config) if parser_args is None else
                  parser_class(config, *parser_args))
        asyncio.run(parser.main())
    except ApplicationException as exception:
        exception.get_error_message(exception)
