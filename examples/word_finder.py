from tuparser import TelegraphParser, run_parser

WORD = "dog"


class WordFinder(TelegraphParser):
    async def parse(self, url, soup):
        website_text = list(soup.stripped_strings)
        for sentence in website_text:
            if WORD in sentence:
                self.output_file.write_data(url)


run_parser(WordFinder, titles=["PLACEHOLDER"], output_file=[{"url": {}}])
