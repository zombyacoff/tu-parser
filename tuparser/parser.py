import asyncio
from abc import ABC, abstractmethod
from typing import Generator

import aiohttp
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm

from .constants import LAUNCH_TIME, TELEGRAPH_URL
from .utils import get_days_in_month, get_time_now
from .validator import OffsetValidation, PublishedYearsValidation, TitlesValidation


class TelegraphParser(ABC):
    SEMAPHORE_MAX_LIMIT = 150
    PROGRESS_BAR_FORMAT = (
        "|{bar:50}| {percentage:.2f}% [{n_fmt}/{total_fmt}] ({elapsed} < {remaining} | {rate_fmt}){postfix}"
    )

    titles = TitlesValidation()
    offset = OffsetValidation()
    published_years = PublishedYearsValidation()

    def _get_total_urls(self) -> int:
        total_days = sum(get_days_in_month(month) for month in range(1, self.total_months + 1))
        return len(self.titles) * self.offset * total_days

    def _check_published_year(self, soup: BeautifulSoup) -> bool:
        if not self.published_years:
            return True

        published_year = int(soup.find("meta", property="article:published_time").get("content")[:4])
        return published_year in self.published_years

    def _generate_urls(self) -> Generator[str, None, None]:
        for month in range(1, self.total_months + 1):
            for day in range(1, get_days_in_month(month) + 1):
                for offset in range(1, self.offset + 1):
                    for title in self.titles:
                        url = f"{TELEGRAPH_URL}/{title}-{month:02}-{day:02}"
                        yield url if offset == 1 else f"{url}-{offset}"

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

    @abstractmethod
    async def parse(self, url: str, soup: BeautifulSoup) -> None: ...

    def run(
        self,
        *,
        titles: list,
        messages: bool = True,
        offset: int = 1,
        progress_bar: bool = True,
        published_years: list[int] | None = None,
    ) -> None:
        self.titles = titles
        self.offset = offset
        self.progress_bar = progress_bar
        self.published_years = published_years

        self.total_months = LAUNCH_TIME.month if self.published_years == [LAUNCH_TIME.year] else 12

        if not messages:
            asyncio.run(self._url_processing())
            return

        print("Parsing has started...\nDo not turn off the program until the process is completed!")

        asyncio.run(self._url_processing())

        elapsed_time = str(get_time_now() - LAUNCH_TIME)[:7]
        print(f"Successfully completed! ({elapsed_time})")
