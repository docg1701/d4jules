# This file makes d4jules.src.core a subpackage
# It should only export symbols defined within this specific subpackage (d4jules/src/core).
# Core logic modules like analyzer, crawler, parser, writer are in d4jules/core/.
from .config_loader import load_config, ConfigError
from .crawler import Crawler
from .parser import parse_html_content
from .writer import save_content_as_markdown

# Ensure that LangChainDeprecationWarning is handled or acknowledged if it persists from this level.
# For now, focusing on structure.

__all__ = [
    "load_config", "ConfigError",
    "Crawler",
    "parse_html_content",
    "save_content_as_markdown"
]
