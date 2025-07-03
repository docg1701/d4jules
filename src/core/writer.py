import html2text
import re
from urllib.parse import urlparse
from pathlib import Path
from typing import Optional

def _generate_filename_from_url(page_url: str) -> str:
    """
    Generates a filesystem-safe filename from a URL.
    Example: http://example.com/foo/bar.html?query=1 -> example_com_foo_bar_html.md
    """
    parsed_url = urlparse(page_url)

    # Start with netloc, replacing dots with underscores
    filename = parsed_url.netloc.replace('.', '_')

    # Add path components
    path_parts = [part for part in parsed_url.path.split('/') if part]
    if path_parts:
        filename += "_" + "_".join(path_parts)

    # Clean the filename: replace non-alphanumeric (excluding underscore, hyphen, dot) with underscore
    filename = re.sub(r'[^\w._-]+', '_', filename)

    # Remove leading/trailing underscores that might result from replacements
    filename = filename.strip('_')

    # Ensure it's not empty after cleaning (e.g. if URL was just "http:///")
    if not filename or filename == "_":
        filename = "index"

    # Add .md extension if not present (e.g. if original path ended with .md)
    if not filename.endswith('.md'):
        filename += ".md"

    # Sanity check for very long filenames (optional, simple truncation for now)
    # A more robust solution might involve hashing, but this is a basic guard.
    MAX_FILENAME_LENGTH = 100 # Reasonble limit
    if len(filename) > MAX_FILENAME_LENGTH:
        name_part, ext_part = Path(filename).stem, Path(filename).suffix
        name_part = name_part[:MAX_FILENAME_LENGTH - len(ext_part) -1] # -1 for a potential underscore
        filename = f"{name_part}{ext_part}"

    return filename

def save_content_as_markdown(
    page_url: str,
    html_content: Optional[str],
    output_dir: str = "output"
) -> Optional[str]:
    """
    Converts HTML content to Markdown and saves it to a file.

    Args:
        page_url: The original URL of the page (used for filename generation).
        html_content: The HTML content string to convert. If None, nothing is saved.
        output_dir: The directory where the Markdown file will be saved.

    Returns:
        The full path to the saved Markdown file if successful, None otherwise.
    """
    if html_content is None:
        return None

    h = html2text.HTML2Text()
    # Configurations based on research (task-R04 and html2text_research.md)
    h.body_width = 0  # No automatic line wrapping
    h.images_as_html = True  # Preserve image tags as HTML
    h.protect_links = True  # Wrap long links with <>
    h.skip_internal_links = False # Keep internal links (e.g., #anchors)
    h.inline_links = True # Use [text](url) format
    h.single_line_break = False # Use two newlines after block elements for better paragraph separation
    h.ignore_emphasis = False # Keep emphasis
    h.bypass_tables = False # Try to convert tables to Markdown

    try:
        markdown_content = h.handle(html_content)
    except Exception as e:
        # Log error during html2text conversion if a logger was available
        print(f"Error converting HTML to Markdown for URL {page_url}: {e}")
        return None

    filename = _generate_filename_from_url(page_url)
    output_path = Path(output_dir)

    try:
        output_path.mkdir(parents=True, exist_ok=True)
        file_path = output_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        return str(file_path)
    except IOError as e:
        # Log error during file writing if a logger was available
        print(f"Error writing Markdown file for URL {page_url} to {file_path}: {e}")
        return None
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred while saving Markdown for {page_url}: {e}")
        return None
