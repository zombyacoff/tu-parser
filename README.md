# Telegraph Universal Parser
It's a pip module that makes it easy to create parsers for the Telegraph website.

### Installation
```batch
pip install tuparser
```

## Example Usage
Here is a small demonstration of how you can create your parser and parse anything you want.
Let's have a look at simple parser that searches particular word in Telegraph articles:
```py
# First, you need to import the necessary modules from tuparser
# In this case import everything
from tuparser import *

# If you want to customize settings,
# create a new class that inherits from Config
class MyParserConfig(Config):
    def parse_config(self):
        # Initialize parameters 
        # from the default configuration file
        super().parse_config()
        # self.config is a dictionary 
        # containing settings from the configuration file  
        self.word = self.config["word"]

# Next, create a new class that inherits from TelegraphParser
class MyParser(TelegraphParser):
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
    MyParser,                     # Your parser class 
    parser_args=[output_file],    # A list containing the class arguments  
    config_class=MyParserConfig,  # Your config class 
    config_path="myparserconfig", # Path to your config file without extension
)
```

#### Here is an example of the `myparserconfig.yml` configuration file:  
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
word: around
```
This word finder you'll find in [example](example) folder

## Contributing
To contribute, fork the repository, create a new branch for your changes, and submit a pull request.

---

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
