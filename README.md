# Telegraph Universal Parser
**Telegraph Universal Parser (tu-parser)** is a flexible Python module designed for creating custom parsers for the Telegraph website. It offers easily configurable and extendable functionality to scrape and analyze article content. This module can be useful for developers looking to automate the extraction of data from Telegraph articles.

### Installation
```batch
pip install tuparser
```

## Example Usage
Here is a small demonstration of how you can create your parser and parse anything you want.
Let's have a look at simple parser that searches particular word in Telegraph articles:
```py
# First, you need to import the necessary modules from tuparser
from tuparser import (
    TelegraphParserConfig,
    TelegraphParser,
    YAMLOutputFile,
    run_parser,
)

# If you want to customize settings,
# create a new class that inherits from Config
class WordFinderConfig(TelegraphParserConfig):
    def parse_config(self):
        # Initialize parameters 
        # from the default configuration file
        super().parse_config()
        # self.config is a dictionary 
        # containing settings from the configuration file  
        self.word = self.config.get("word")

# Next, create a new class that inherits from TelegraphParser
class WordFinder(TelegraphParser):
    # Add additional arguments to the main constructor
    # 'output_file' is an instance of the YAMLOutputFile class
    # which simplifies the creation of the output file  
    def __init__(self, config, output_file):
        super().__init__(config)
        self.output_file = output_file
    
    # The parse() function is always required in your code
    # It is the entry point for your parser logic
    async def parse(self, url, soup):
        # 'website_text' is a list containing 
        # all the text from the Telegraph article 
        website_text = list(soup.stripped_strings)
        for sentence in website_text:
            if self.config.word in sentence:
                # Write the URL to the output dictionary
                self.output_file.write_data(url)

# Create an instance of YAMLOutputFile
# You must provide a dictionary with the initial structure
output_file = YAMLOutputFile({"url": {}})
# Run the parser with the specified configuration
run_parser(
    WordFinder,                       # Your parser class 
    parser_args=[output_file],        # A list containing the class arguments  
    config_class=WordFinderConfig,    # Your config class 
    config_path="word_finder_config", # Path to your config file without extension
)
```

#### Here is an example of the `word_finder_config.yml` configuration file:  
```yaml
# Specifies how many articles the parser will examine per day.
# Provide an integer between 2 and 250.
# Set to false to disable this feature.
offset: false

# A list of years in which the articles were written.
# If you only want articles from specific years, list them here.
# Set to false to disable this filter.
release_date: false

# Boolean value to turn the progress bar on or off.
# Set to true to show the progress bar, false to hide it.
progress_bar: true

# Titles of the articles to search for.
# Add as many titles as you want; the parser will look for articles with these titles.
titles:
- dog
- cat

# The word to search for within the articles' text, as declared in MyParserConfig.
# The parser will look for this word in each article.
word: animal
```
This word finder you'll find in [example](example) folder.

You can also take a look at the [basic configuration file](config.yml), which should be present in every project. Of course, you are free to change its name and path, specifying it as an argument to the `run_parser` function, as well as add new parameters to the config, as shown above.

And finally, **you can explore other examples of how to use this module — [LP Parser](https://github.com/zombyacoff/telegraph-lp-parser), [Media Parser](https://github.com/Fru1tApple/telegraph-media-parser), and [Links Parser](https://github.com/lazerofmagma/links-parser).**

## Contributing
To contribute, fork the repository, create a new branch for your changes, and submit a pull request.

---

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
