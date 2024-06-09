import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generator

import aiohttp
from bs4 import BeautifulSoup

from ..config.base import Config
from ..constants import LAUNCH_TIME
from ..exceptions.config import InvalidWebsiteURLError
from ..extensions.progress_bar import ProgressBar
from ..utils import ConsoleColor, get_monthrange, get_time_now
from .constants import (
    PARSING_START_MESSAGE,
    SEMAPHORE_MAX_LIMIT,
    SUCCESS_COMPLETE_TITLE,
    TIME_ELAPSED_TEXT,
)


@dataclass
class TelegraphParser(ABC):
    config: Config

    def __post_init__(self) -> None:
        self.bar_counter = 0

    @abstractmethod
    async def _process_url(
        self, url: str, session: aiohttp.ClientSession
    ) -> BeautifulSoup | None:
        """Processing the URL —
        checking for validity, release date,
        and returning a BeautifulSoup object"""
        try:
            async with session.get(url) as page:
                if page.status != 200:
                    return None
                soup = BeautifulSoup(await page.text(), "html.parser")
        except aiohttp.InvalidURL:
            raise InvalidWebsiteURLError(url=url) from None

        if not self._check_release_date(soup):
            return None

        return soup

    def _get_progress_bar(self) -> None:
        """Print the progress bar"""
        ProgressBar.show(self.bar_counter, self.config.total_urls)
        self.bar_counter += 1

    def _check_release_date(self, soup: BeautifulSoup) -> bool:
        """Check if the release date is valid"""
        if not self.config.release_date_bool:
            return True

        time_element = soup.select_one("time")
        release_date = (
            int(time_element.get_text("\n", strip=True)[-4:])
            if time_element
            else LAUNCH_TIME.year
        )
        return release_date in self.config.release_date

    @abstractmethod
    def _get_complete_message(self) -> None:
        """
        Abstract method for printing the completion message

        SUCCESSFULLY COMPLETED
        Time elapsed: 0:00:01.012345
        """
        elapsed_time = get_time_now() - LAUNCH_TIME
        print(
            ConsoleColor.paint_success(SUCCESS_COMPLETE_TITLE)
            + " "
            * (
                ProgressBar.get_length(self.config.total_urls)
                - len(SUCCESS_COMPLETE_TITLE)
            ),
            ConsoleColor.paint_info(TIME_ELAPSED_TEXT.format(time=elapsed_time)),
            sep="\n",
        )

    def _generate_urls(self) -> Generator[str, None, None]:
        for month in range(1, self.config.total_months + 1):
            for day in range(1, get_monthrange(month) + 1):
                for offset in range(1, self.config.offset_value + 1):
                    for title in self.config.titles:
                        yield (
                            f"https://telegra.ph/{title}-{month:02}-{day:02}-{offset}"
                            if offset > 1
                            else f"https://telegra.ph/{title}-{month:02}-{day:02}"
                        )

    async def _semaphore_process(
        self, url: str, semaphore: asyncio.Semaphore, session: aiohttp.ClientSession
    ) -> None:
        async with semaphore:
            await self._process_url(url, session)

    @abstractmethod
    async def main(self) -> None:
        semaphore = asyncio.Semaphore(SEMAPHORE_MAX_LIMIT)
        async with aiohttp.ClientSession() as session:
            urls_generator = self._generate_urls()
            processes = [
                self._semaphore_process(url, semaphore, session)
                for url in urls_generator
            ]
            print(ConsoleColor.paint_info(PARSING_START_MESSAGE))
            # await asyncio.gather(*processes)
            for process in asyncio.as_completed(processes):
                self._get_progress_bar()
                await process

        self._get_complete_message()
