import aiohttp
from bs4 import BeautifulSoup

from tuparser.config import Config
from tuparser.file_operations.file_manager import FileManager
from tuparser.parser import TelegraphParser, run_parser


class MediaParser(TelegraphParser):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.main_output_folder = "parser-output"
        self.output_folder = "media"
        self.images_folder = "images"
        self.videos_folder = "videos"

    async def process_url(
        self, url: str, session: aiohttp.ClientSession
    ) -> None:
        soup = await super().process_url(url, session)
        # return if url is not valid
        if soup is None:
            return

        folder_url = url[19:]
        images = self.get_urls(soup.find_all("img"))
        videos = self.get_urls(soup.find_all("video"))

        if images:
            await self.download_media(
                images, self.images_folder, "gif", folder_url, session
            )
        if videos:
            await self.download_media(
                videos, self.videos_folder, "mp4", folder_url, session
            )

    async def download_media(
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
                    FileManager.save_file(
                        media_file_path, await response.read()
                    )
            except aiohttp.client_exceptions.ClientConnectorError:
                continue

    def get_urls(self, media: list[BeautifulSoup]) -> list[str] | list[None]:
        return [
            f"https://telegra.ph{value.get("src")}"
            for value in media
            if not value.get("src").startswith("http")
        ]


if __name__ == "__main__":
    run_parser(config_class=Config, parser_class=MediaParser)
