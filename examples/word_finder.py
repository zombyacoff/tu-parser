from dataclasses import dataclass

from tuparser import TelegraphParser, YAMLOutputFile, run_parser

WORD = "animal"


@dataclass
class WordFinder(TelegraphParser):
    output_file: YAMLOutputFile

    async def parse(self, url, soup):
        website_text = list(soup.stripped_strings)
        for sentence in website_text:
            if self.word in sentence:
                self.output_file.write_data(url)


output_file = YAMLOutputFile({"url": {}})
run_parser(
    WordFinder,
    parser_args=[output_file],
    titles=["cat", "dog"],
)
