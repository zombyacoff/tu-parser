from dataclasses import dataclass

from aiohttp import ClientSession

from tuparser.config.base import Config
from tuparser.file_operations.output_file import OutputYAMLFile
from tuparser.main import run_parser
from tuparser.parser.base import TelegraphParser
from tuparser.utils import ConsoleColor, compile_regex


class LPParserConfig(Config):
    def _parse_config(self) -> None:
        super()._parse_config()

        self.exceptions = self.config["exceptions"] + ["dmca@telegram.org"]
        self.login_regex = compile_regex(
            self.config["for_advanced_users"]["login_regex"]
        )
        self.password_regex = compile_regex(
            self.config["for_advanced_users"]["password_regex"]
        )


@dataclass
class LPParser(TelegraphParser):
    output_file: OutputYAMLFile

    async def _process_url(self, url: str, session: ClientSession) -> None:
        soup = await super()._process_url(url, session)
        if soup is None:
            return

        website_text = list(soup.stripped_strings)
        output_data = self._extract_credentials(website_text) + (url,)
        if output_data[0] != "":
            self.output_file.write_output(output_data)

    def _extract_credentials(self, website_text: list[str]) -> tuple[str, str]:
        login = password = ""

        for i, current in enumerate(website_text):
            email_match = self.config.login_regex.search(current)
            if email_match is None or email_match.group() in self.config.exceptions:
                continue

            login = email_match.group()
            if ":" in login:
                data = login.split(":")
                login, password = data[0], data[-1]
                return login, password
            for k in range(1, min(4, len(website_text) - i)):
                password_match = self.config.password_regex.search(website_text[i + k])
                if password_match is None:
                    continue
                password = password_match.group()
                break

        return login, password

    def _get_complete_message(self) -> None:
        super()._get_complete_message()
        # Output file path: parser-output\output_file_name.yml
        print(
            ConsoleColor.paint_info(
                f"Output file path: parser-output/{self.output_file.output_file_name}",
            )
        )

    async def main(self) -> None:
        await super().main()
        self.output_file.complete_output()


if __name__ == "__main__":
    output_file = OutputYAMLFile({"login": {}, "password": {}, "url": {}})
    run_parser(
        config_class=LPParserConfig,
        parser_class=LPParser,
        parser_arguments=(output_file,),
    )
