from dataclasses import dataclass

import aiohttp
from bs4 import BeautifulSoup

from tuparser.config.base import Config
from tuparser.file_operations.file_manager import FileManager
from tuparser.main import run_parser
from tuparser.parser.base import TelegraphParser


@dataclass
class MediaParser(TelegraphParser):
    main_output_folder: str = "parser-output"
    output_folder: str = "media"
    images_folder: str = "images"
    videos_folder: str = "videos"

    async def _process_url(self, url: str, session: aiohttp.ClientSession) -> None:
        soup = await super()._process_url(url, session)
        if soup is None:
            return

        folder_url = url[19:]
        images = self._get_urls(soup.find_all("img"))
        videos = self._get_urls(soup.find_all("video"))

        if images:
            await self._download_media(
                images, self.images_folder, "gif", folder_url, session
            )
        if videos:
            await self._download_media(
                videos, self.videos_folder, "mp4", folder_url, session
            )

    async def _download_media(
        self,
        media: list[str],
        main_folder: str,
        file_extension: str,
        folder: str,
        session: aiohttp.ClientSession,
    ) -> None:
        media_folder_path = FileManager.join_paths(
            self.main_output_folder,
            self.output_folder,
            main_folder,
            folder,
        )
        FileManager.create_folder(media_folder_path)

        for i, value_url in enumerate(media):
            try:
                async with session.get(value_url) as response:
                    media_file_name = f"{i}.{file_extension}"
                    media_file_path = FileManager.join_paths(
                        media_folder_path, media_file_name
                    )
                    FileManager.save_file(media_file_path, await response.read())
            except aiohttp.client_exceptions.ClientConnectorError:
                continue

    def _get_urls(self, media: list[BeautifulSoup]) -> list[str] | list[None]:
        return [
            f"https://telegra.ph{value.get("src")}"
            for value in media
            if not value.get("src").startswith("http")
        ]

    def _get_complete_message(self) -> None:
        super()._get_complete_message()

    async def main(self) -> None:
        await super().main()


if __name__ == "__main__":
    run_parser(config_class=Config, parser_class=MediaParser)
