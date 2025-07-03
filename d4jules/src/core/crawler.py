#!/usr/bin/env python3
# d4jules/src/core/crawler.py

import collections
from urllib.parse import urlparse, urlunparse, urldefrag

class Crawler:
    def __init__(self, base_url: str = "", config: dict = None, max_pages: int = None, max_depth: int = None):
        self.base_url = base_url
        self.config = config if config is not None else {}
        self.max_pages = max_pages
        self.max_depth = max_depth

        self.to_visit_queue = collections.deque()
        self.visited_urls = set()
        self._queue_set = set()

        if base_url:
             self.add_url(base_url)

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

    def add_url(self, url: str):
        normalized_url = self._normalize_url(url)
        if not normalized_url:
            return

        if normalized_url not in self.visited_urls and normalized_url not in self._queue_set:
            self.to_visit_queue.append(normalized_url)
            self._queue_set.add(normalized_url)

    def add_urls(self, urls: list[str]):
        for url in urls:
            self.add_url(url)

    def get_next_url(self) -> str | None:
        if not self.to_visit_queue:
            return None

        url = self.to_visit_queue.popleft()
        self._queue_set.remove(url)
        self.mark_as_visited(url)
        return url

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
        if not self.base_url:
            return True

        normalized_url_to_check = self._normalize_url(url)
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
                print(f"Reached max_pages limit of {self.max_pages}. Stopping crawl.")
                break

            current_url = self.get_next_url()
            if not current_url:
                break

            if not self.can_crawl_url(current_url):
                print(f"Skipping URL (outside base domain or invalid): {current_url}")
                continue

            print(f"Crawling ({pages_crawled + 1}): {current_url}")
            pages_crawled += 1
            print(f"Queue size: {self.get_queue_size()}, Visited: {self.get_visited_count()}")

        print(f"Crawling finished. Total pages visited: {self.get_visited_count()}")
