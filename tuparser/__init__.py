from .config import TelegraphParserConfig
from .constants import LAUNCH_TIME, TELEGRAPH_URL, TELEGRAPH_URL_MIRROR
from .file_handling import FileManager, YAMLOutputFile
from .parser import TelegraphParser, run_parser
from .utils import ConsoleColor, call_counter, get_monthrange, get_time_now
from .validator import validate

__all__ = [
    "TelegraphParserConfig",
    "LAUNCH_TIME",
    "TELEGRAPH_URL",
    "TELEGRAPH_URL_MIRROR",
    "FileManager",
    "YAMLOutputFile",
    "TelegraphParser",
    "run_parser",
    "ConsoleColor",
    "get_monthrange",
    "get_time_now",
    "call_counter",
    "validate",
]

# This information is used in the setup.py file:
__version__ = "0.1.5.4"
__author__ = "zombyacoff"
__email__ = "zombyacoff@gmail.com"
__git_url__ = "https://github.com/zombyacoff/tu-parser"
