from .config import TelegraphParserConfig
from .constants import TELEGRAPH_MIRROR_URL, TELEGRAPH_URL
from .file_handling import FileManager, YAMLOutputFile
from .parser import TelegraphParser, run_parser
from .validator import validate

__all__ = [
    "TelegraphParserConfig",
    "TELEGRAPH_MIRROR_URL",
    "TELEGRAPH_URL",
    "FileManager",
    "YAMLOutputFile",
    "TelegraphParser",
    "run_parser",
    "validate",
]

# This information is used in the setup.py file:
__version__ = "0.1.5.5"
__author__ = "zombyacoff"
__email__ = "zombyacoff@gmail.com"
__git_url__ = "https://github.com/zombyacoff/tu-parser"
