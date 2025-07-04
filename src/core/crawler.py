#!/usr/bin/env python3
# d4jules/src/core/crawler.py

import collections
import requests # For downloading HTML content before parsing
import logging # Added for logging
from urllib.parse import urlparse, urlunparse, urldefrag
from typing import Callable, Dict, Any, Optional, Tuple, List

# Import exceptions and types from other modules for error handling and type hints
from .analyzer import HtmlSelectors, AnalyzerError, NetworkError, LLMAnalysisError

logger = logging.getLogger(__name__)

class Crawler:
    def __init__(self,
                 base_url: str = "",
                 max_pages: Optional[int] = None,
                 max_depth: Optional[int] = None,
                 analyzer_func: Callable[[str, Dict[str, Any]], HtmlSelectors] = None,
                 parser_func: Callable[[str, str, str, Optional[str], Optional[str]], Tuple[Optional[str], List[str]]] = None,
                 writer_func: Callable[[str, Optional[str], str], Optional[str]] = None,
                 analyzer_config: Dict[str, Any] = None,
                 output_dir: str = "output"):
        self.base_url = base_url
        self.max_pages = max_pages
        self.max_depth = max_depth # Will be used in task-R02

        # Injected dependencies
        self.analyzer_func = analyzer_func
        self.parser_func = parser_func
        self.writer_func = writer_func
        self.analyzer_config = analyzer_config if analyzer_config is not None else {}
        self.output_dir = output_dir

        self.to_visit_queue = collections.deque()
        self.visited_urls = set()
        self._queue_set = set() # To quickly check if a URL is already in to_visit_queue

        if not self.analyzer_func or not self.parser_func or not self.writer_func:
            raise ValueError("analyzer_func, parser_func, and writer_func must be provided.")

        if base_url:
             self.add_url(base_url, depth=0) # Add initial URL with depth 0

    def _normalize_url(self, url: str) -> str:
        if not url:
            return ""
        url = url.strip()
        url_no_frag, _ = urldefrag(url)

        try:
            temp_url_for_parse = url_no_frag
            # Heuristic: if no scheme, and ( (has dot and slash) OR (first path part has dot) )
            # then it's likely a domain that needs a scheme.
            if '://' not in url_no_frag and \
               ((url_no_frag.count('.') > 0 and '/' in url_no_frag) or \
                (url_no_frag.split('/')[0].count('.') > 0)):
                temp_url_for_parse = f"https://{url_no_frag}"

            parsed = urlparse(temp_url_for_parse)

            scheme = parsed.scheme.lower()
            netloc = parsed.netloc.lower()
            path = parsed.path
            params = parsed.params
            query = parsed.query

            if not netloc: # After attempting to parse, if netloc is still empty, invalid.
                return ""

            if scheme not in ["http", "https"]: # Must be http or https.
                return ""

            # Normalize path: remove trailing slash unless it's the root path itself
            if path.endswith('/') and len(path) > 1:
                path = path[:-1]
            elif not path and netloc: # if path is empty and there's a domain, ensure it's "/"
                path = '/'

            return urlunparse((scheme, netloc, path, params, query, ''))
        except ValueError: # Catch any parsing errors
            return ""

    def add_url(self, url: str, depth: int):
        normalized_url = self._normalize_url(url)
        if not normalized_url:
            return

        if self.max_depth is not None and depth > self.max_depth:
            print(f"DEBUG: URL {normalized_url} at depth {depth} exceeds max_depth {self.max_depth}. Not adding.")
            return

        if normalized_url not in self.visited_urls and normalized_url not in self._queue_set:
            self.to_visit_queue.append((normalized_url, depth))
            self._queue_set.add(normalized_url)
            # print(f"DEBUG: Added to queue: {normalized_url} at depth {depth}")
        # else:
            # print(f"DEBUG: URL {normalized_url} already visited or in queue. Not adding.")


    def add_urls(self, urls: list[str], current_depth: int):
        new_link_depth = current_depth + 1
        if self.max_depth is not None and new_link_depth > self.max_depth:
            print(f"DEBUG: Not adding new links from depth {current_depth} because new depth {new_link_depth} would exceed max_depth {self.max_depth}")
            return

        for url in urls:
            self.add_url(url, new_link_depth)

    def get_next_url(self) -> Tuple[Optional[str], Optional[int]]:
        if not self.to_visit_queue:
            return None, None

        url, depth = self.to_visit_queue.popleft()
        self._queue_set.remove(url) # Remove from set used to check if already in queue
        # Note: mark_as_visited will be called after successful processing or definite skip in start_crawling
        # For now, let's assume get_next_url implies it will be "visited" in some sense (attempted)
        # but actual addition to self.visited_urls might be better after processing attempt.
        # However, the current structure of start_crawling calls get_next_url then processes.
        # If it fails processing, it's still "visited" in the sense of being popped.
        # Let's keep mark_as_visited here for now as it aligns with current logic.
        self.mark_as_visited(url) # Mark as visited when taken from queue
        return url, depth

    def mark_as_visited(self, url: str):
        normalized_url = self._normalize_url(url)
        if normalized_url:
            self.visited_urls.add(normalized_url)

    def has_next_url(self) -> bool:
        return bool(self.to_visit_queue)

    def get_queue_size(self) -> int:
        return len(self.to_visit_queue)

    def get_visited_count(self) -> int:
        return len(self.visited_urls)

    def can_crawl_url(self, url: str) -> bool:
        normalized_url_to_check = self._normalize_url(url)
        if not normalized_url_to_check: # If URL is fundamentally invalid (e.g. bad scheme, unparseable)
            return False

        if not self.base_url: # No domain scoping if base_url isn't set, but URL must be valid
            return True

        normalized_base_url = self._normalize_url(self.base_url)

        if not normalized_url_to_check or not normalized_base_url:
            return False

        parsed_url_to_check = urlparse(normalized_url_to_check)
        parsed_base_url = urlparse(normalized_base_url)

        return parsed_url_to_check.netloc == parsed_base_url.netloc

    def start_crawling(self):
        print(f"Starting crawl for base URL: {self.base_url}")
        pages_crawled = 0

        while self.has_next_url():
            if self.max_pages is not None and pages_crawled >= self.max_pages:
                print(f"INFO: Reached max_pages limit of {self.max_pages}. Stopping crawl.")
                break

            current_url, current_depth = self.get_next_url()

            if not current_url: # Queue is empty
                break

            # Redundant check if add_url correctly filters by depth, but good for safety
            if self.max_depth is not None and current_depth > self.max_depth:
                print(f"DEBUG: Skipping {current_url} at depth {current_depth} (exceeds max_depth {self.max_depth}) - this should ideally not happen if add_url filters correctly.")
                continue

            if not self.can_crawl_url(current_url):
                print(f"INFO: Skipping URL (outside base domain or invalid): {current_url}")
                continue

            print(f"INFO: Processing ({pages_crawled + 1}/{self.max_pages if self.max_pages else 'unlimited'}): {current_url} at depth {current_depth}")

            # --- 1. Analyze URL for selectors ---
            try:
                if not self.analyzer_func or self.analyzer_config is None:
                    print(f"ERROR: Analyzer function or config not set for URL {current_url}. Skipping.")
                    continue
                selectors = self.analyzer_func(current_url, self.analyzer_config)
                print(f"DEBUG: Selectors for {current_url}: Content='{selectors.content_selector}', Nav='{selectors.navigation_selector}', Next='{selectors.next_page_selector}'")
            except (AnalyzerError, NetworkError, LLMAnalysisError) as e:
                print(f"ERROR: Analyzer phase failed for {current_url}: {e}")
                continue
            except Exception as e:
                print(f"ERROR: Unexpected error during analysis of {current_url}: {e}")
                continue

            # --- 2. Fetch HTML content for parser ---
            html_content_for_parser: Optional[str] = None
            try:
                response = requests.get(current_url, timeout=30)
                response.raise_for_status()
                html_content_for_parser = response.text
            except requests.exceptions.RequestException as e:
                print(f"ERROR: Failed to fetch HTML for parsing {current_url}: {e}")
                continue

            if html_content_for_parser is None: # Should be caught by raise_for_status or RequestException
                print(f"ERROR: HTML content is None after fetching for {current_url}. Skipping.")
                continue

            # --- 3. Parse HTML for content and links ---
            parsed_content_html: Optional[str] = None
            extracted_links: List[str] = []
            try:
                if not self.parser_func:
                    print(f"ERROR: Parser function not set for URL {current_url}. Skipping.")
                    continue
                parsed_content_html, extracted_links = self.parser_func(
                    html_content_for_parser,
                    current_url,
                    selectors.content_selector,
                    selectors.navigation_selector,
                    selectors.next_page_selector
                )
                print(f"DEBUG: Parsed {current_url}. Found {len(extracted_links)} links. Content HTML length: {len(parsed_content_html) if parsed_content_html else 0}")
            except Exception as e:
                print(f"ERROR: Parsing failed for {current_url}: {e}")
                continue

            # --- 4. Write content to Markdown ---
            try:
                if not self.writer_func:
                    print(f"ERROR: Writer function not set for URL {current_url}. Skipping save.")
                elif parsed_content_html is not None:
                    saved_filepath = self.writer_func(
                        current_url,
                        parsed_content_html,
                        self.output_dir
                    )
                    if saved_filepath:
                        print(f"INFO: Content from {current_url} saved to {saved_filepath}")
                    else:
                        print(f"WARN: Failed to save content for {current_url} (writer returned None).")
                else:
                    print(f"INFO: No content extracted from {current_url} to save.")
            except Exception as e:
                print(f"ERROR: Writing content failed for {current_url}: {e}")

            # --- 5. Add new valid links to queue ---
            # Only add links if current_depth is less than max_depth (or max_depth is None)
            # This check is now primarily handled by add_urls and add_url.
            if extracted_links:
                print(f"DEBUG: Adding {len(extracted_links)} new links from {current_url} (depth {current_depth}) to queue.")
                self.add_urls(extracted_links, current_depth)

            pages_crawled += 1
            print(f"INFO: Finished processing {current_url}. Queue size: {self.get_queue_size()}, Visited: {self.get_visited_count()}")
            print("-" * 30)


        print(f"Crawling finished. Total pages processed: {pages_crawled}, Total URLs visited: {self.get_visited_count()}")
