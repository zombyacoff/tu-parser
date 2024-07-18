from .constants import TELEGRAPH_MIRROR_URL, TELEGRAPH_URL
from .file_handling import FileManager
from .parser import TelegraphParser, run_parser

__all__ = ["TELEGRAPH_MIRROR_URL", "TELEGRAPH_URL", "FileManager", "TelegraphParser", "run_parser"]

# This information is used in the setup.py file:
__version__ = "0.2.0"
__author__ = "zombyacoff"
__email__ = "zombyacoff@gmail.com"
__git_url__ = "https://github.com/zombyacoff/tu-parser"
