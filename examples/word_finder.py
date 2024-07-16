from tuparser import TelegraphParser, YAMLOutputFile, run_parser

WORD = "dog"


class WordFinder(TelegraphParser):
    def __init__(self, parser_args, output_file):
        super().__init__(parser_args)
        self.output_file = output_file

    async def parse(self, url, soup):
        website_text = list(soup.stripped_strings)
        for sentence in website_text:
            if WORD in sentence:
                self.output_file.write_data(url)


output_file = YAMLOutputFile({"url": {}})
run_parser(WordFinder, titles=["PLACEHOLDER"], custom_args=[output_file])
