from tuparser import TelegraphParser, TelegraphParserConfig, YAMLOutputFile, run_parser


class WordFinderConfig(TelegraphParserConfig):
    def parse_config(self):
        super().parse_config()
        self.word = self.config.get("word")


class WordFinder(TelegraphParser):
    def __init__(self, config, output_file):
        super().__init__(config)
        self.output_file = output_file

    async def parse(self, url, soup):
        website_text = list(soup.stripped_strings)
        for sentence in website_text:
            if self.config.word in sentence:
                self.output_file.write_data(url)


output_file = YAMLOutputFile({"url": {}})
run_parser(
    WordFinder,
    parser_args=[output_file],
    config_class=WordFinderConfig,
    config_path="word_finder_config",
)
