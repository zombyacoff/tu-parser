import re

from tuparser import TelegraphParser, run_parser

EXCEPTIONS = ["dmca@telegram.org"]

LOGIN_REGEX = re.compile(r"\S+@\S+\.\S+")
PASSWORD_REGEX = re.compile(r"\S*\d\S*")


class LPParser(TelegraphParser):
    async def parse(self, url, soup) -> None:
        website_text = list(soup.stripped_strings)
        output_data = self.extract_credentials(website_text)

        if output_data[0] != "":
            self.output_file.write_data(*output_data, url)

    def extract_credentials(self, website_text):
        login = password = ""
        for i, current in enumerate(website_text):
            email_match = LOGIN_REGEX.search(current)
            if email_match is None or email_match.group() in EXCEPTIONS:
                continue
            login = email_match.group()
            if ":" in login:
                data = login.split(":")
                login, password = data[0], data[-1]
                return login, password
            for k in range(1, min(4, len(website_text) - i)):
                password_match = PASSWORD_REGEX.search(website_text[i + k])
                if password_match is None:
                    continue
                password = password_match.group()
                break

        return login, password


run_parser(LPParser, titles=["PLACEHOLDER"], output_file=[{"login": {}, "password": {}, "url": {}}])
