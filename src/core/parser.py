from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Tuple, List, Optional

def parse_html_content(
    html_doc: str,
    base_url: str,
    content_selector: str,
    nav_selector: Optional[str],
    next_page_selector: Optional[str]
) -> Tuple[Optional[str], List[str]]:
    """
    Parses HTML content to extract the main content block and relevant links.

    Args:
        html_doc: The HTML document string.
        base_url: The base URL of the HTML document, used for resolving relative links.
        content_selector: CSS selector for the main content block.
        nav_selector: CSS selector for navigation links container. Links are extracted from <a> tags within this.
        next_page_selector: CSS selector for the 'next page' link.

    Returns:
        A tuple containing:
            - The HTML string of the main content block (or None if not found).
            - A list of unique absolute URLs found (navigation + next page).
    """
    try:
        soup = BeautifulSoup(html_doc, 'lxml')
    except Exception:  # Fallback if lxml is not available or fails
        soup = BeautifulSoup(html_doc, 'html.parser')

    content_html: Optional[str] = None
    if content_selector:
        content_element = soup.select_one(content_selector)
        if content_element:
            content_html = str(content_element)

    extracted_urls: set[str] = set()

    # Extract navigation links
    if nav_selector:
        nav_container = soup.select_one(nav_selector)
        if nav_container:
            for link_tag in nav_container.select("a[href]"):
                href = link_tag.get('href')
                if href:
                    absolute_url = urljoin(base_url, href)
                    extracted_urls.add(absolute_url)

    # Extract next page link
    if next_page_selector:
        next_page_link_tag = soup.select_one(next_page_selector + "[href]")
        if next_page_link_tag: # Check if the selector itself is an 'a' tag or contains one
            href = next_page_link_tag.get('href')
            if href:
                absolute_url = urljoin(base_url, href)
                extracted_urls.add(absolute_url)
        else: # If the selector points to a container, try to find 'a' inside it
            next_page_container = soup.select_one(next_page_selector)
            if next_page_container:
                link_tag_inside = next_page_container.select_one("a[href]")
                if link_tag_inside:
                    href = link_tag_inside.get('href')
                    if href:
                        absolute_url = urljoin(base_url, href)
                        extracted_urls.add(absolute_url)


    return content_html, sorted(list(extracted_urls))
