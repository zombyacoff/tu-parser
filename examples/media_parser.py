from os import makedirs, path

from aiohttp.client_exceptions import ClientConnectorError

from tuparser import TELEGRAPH_URL, TelegraphParser, run_parser


class MediaParser(TelegraphParser):
    async def parse(self, url, soup):
        self.article = url.split("/")[-1]
        images = self.get_urls(soup.find_all("img"))
        videos = self.get_urls(soup.find_all("video"))

        if images:
            await self.download_media(images, "images", "gif")
        if videos:
            await self.download_media(videos, "videos", "mp4")

    async def download_media(self, media, media_category, file_extension):
        media_folder_path = path.join("output", "media", media_category, self.article)
        makedirs(media_folder_path, exist_ok=True)

        for i, url in enumerate(media):
            try:
                async with self.session.get(url) as response:
                    media_file_name = f"{i + 1}.{file_extension}"
                    media_file_path = path.join(media_folder_path, media_file_name)
                    with open(media_file_path, "wb") as file:
                        file.write(await response.read())
            except ClientConnectorError:
                ...

    def get_urls(self, media):
        return [TELEGRAPH_URL + value.get("src") for value in media if not value.get("src").startswith("http")]


run_parser(MediaParser, titles=["PLACEHOLDER"])
