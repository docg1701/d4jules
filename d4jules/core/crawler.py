import requests
from collections import deque
from typing import Optional, Set, Tuple, List, Dict, Any
from urllib.parse import urlparse, urljoin # urljoin was missing in plan text but implied

# Placeholder for analyzer module/function (from task-D09)
# Actual import path might be different based on task-D09's implementation
# from ..core import analyzer # Assuming it's in d4jules.core.analyzer
# For now, let's define a mock so the file is syntactically valid
class MockAnalyzer:
    def analyze_url_for_selectors(self, url: str, config: Dict[str, Any]) -> Optional[Tuple[Optional[str], Optional[str], Optional[str]]]:
        print(f"MockAnalyzer: Analyzing {url} for selectors (E2E Test Mode).")
        # For E2E testing (task-T02), provide fixed selectors for "test-site.com"
        if "test-site.com" in url:
            content_selector = "div#content"
            nav_selector = "nav#nav_menu"
            next_page_selector = "a.next_button"
            print(f"  MockAnalyzer: Returning selectors for test-site: C='{content_selector}', N='{nav_selector}', NP='{next_page_selector}'")
            return (content_selector, nav_selector, next_page_selector)

        # Fallback for other URLs or if the actual analyzer from D09 is different
        print(f"  MockAnalyzer: No predefined selectors for {url}. Returning None.")
        return (None, None, None)

analyzer = MockAnalyzer() # This will be used by Crawler unless D09 provides a real one and updates the import

from d4jules.core.parser import parse_html_content
from d4jules.core.writer import save_content_as_markdown

class Crawler:
    def __init__(self, base_url: str, config: Dict[str, Any],
                 max_pages: Optional[int] = None,
                 max_depth: Optional[int] = None):
        self.base_url = base_url
        self.config = config # Expected to contain API keys or other settings for analyzer
        self.max_pages = max_pages
        self.max_depth = max_depth

        self.url_queue: deque[Tuple[str, int]] = deque()
        self.visited_urls: Set[str] = set()
        self.pages_processed_count: int = 0

        parsed_base_url = urlparse(self.base_url)
        self.base_domain = parsed_base_url.netloc

        # Placeholder for logging
        print(f"Crawler initialized for base URL: {self.base_url}")
        print(f"Base domain set to: {self.base_domain}")
        if self.max_pages:
            print(f"Max pages to crawl: {self.max_pages}")
        if self.max_depth:
            print(f"Max depth to crawl: {self.max_depth}")

    def _is_same_domain(self, url: str) -> bool:
        try:
            parsed_url = urlparse(url)
            return parsed_url.netloc == self.base_domain
        except Exception:
            return False

    def _normalize_url(self, url: str) -> str:
        """ Basic normalization: remove fragment and ensure consistent scheme if possible. """
        parsed = urlparse(url)
        # Rebuild without fragment, ensure scheme and netloc are present
        # This is a simple version; more robust normalization might be needed
        scheme = parsed.scheme if parsed.scheme else urlparse(self.base_url).scheme
        netloc = parsed.netloc if parsed.netloc else self.base_domain # Fallback to base_domain if netloc is missing

        # If URL is relative, urljoin should handle it correctly with base_url
        # If it's absolute, this ensures it's well-formed.
        # For this crawler, we often get absolute URLs from parser already.
        # The main goal here is to strip fragments for visited checks.
        return urlparse(urljoin(self.base_url, url))._replace(fragment="").geturl()


    def add_url_to_queue(self, url: str, depth: int):
        normalized_url = self._normalize_url(url)

        if normalized_url in self.visited_urls:
            # print(f"URL already visited: {normalized_url}")
            return

        # Check if already in queue (simple check, might not be perfectly efficient for large queues)
        # A more robust way would be a separate set for "in_queue" status
        for item_url, _ in self.url_queue:
            if self._normalize_url(item_url) == normalized_url:
                # print(f"URL already in queue: {normalized_url}")
                return

        if not self._is_same_domain(normalized_url):
            # print(f"Skipping external URL: {normalized_url}")
            return

        if self.max_depth is not None and depth > self.max_depth:
            print(f"Skipping URL due to max depth: {normalized_url} (depth {depth})")
            return

        self.url_queue.append((normalized_url, depth))
        # print(f"Added to queue: {normalized_url} (depth {depth})")

    def start_crawling(self):
        print(f"Starting crawl for {self.base_url}...")
        self.add_url_to_queue(self.base_url, 0)

        while self.url_queue:
            if self.max_pages is not None and self.pages_processed_count >= self.max_pages:
                print(f"Max pages limit ({self.max_pages}) reached. Stopping crawl.")
                break

            current_url, current_depth = self.url_queue.popleft()
            normalized_current_url = self._normalize_url(current_url) # Should be normalized already if from queue

            if normalized_current_url in self.visited_urls:
                # print(f"Re-checking visited, skipping: {normalized_current_url}")
                continue

            print(f"Processing: {normalized_current_url} (Depth: {current_depth}, Processed: {self.pages_processed_count}/{self.max_pages if self.max_pages else 'unlimited'})")

            self.visited_urls.add(normalized_current_url)
            self.pages_processed_count += 1

            try:
                # Step 1: Get selectors using Analyzer
                # print(f"  [Crawler] Analyzing URL for selectors: {normalized_current_url}")
                selectors = analyzer.analyze_url_for_selectors(normalized_current_url, self.config)

                if not selectors or not selectors[0]: # Assuming content_selector (selectors[0]) is mandatory
                    print(f"  [Crawler] Failed to get selectors or no content selector for {normalized_current_url}. Skipping.")
                    continue

                content_selector, nav_selector, next_page_selector = selectors
                # print(f"  [Crawler] Selectors obtained: C='{content_selector}', N='{nav_selector}', NP='{next_page_selector}'")

                # Step 2: Download HTML
                # print(f"  [Crawler] Downloading HTML for: {normalized_current_url}")
                try:
                    headers = {'User-Agent': 'Mozilla/5.0 (compatible; JulesCrawler/0.1)'}
                    response = requests.get(normalized_current_url, timeout=10, headers=headers)
                    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                    html_doc = response.text
                except requests.RequestException as e:
                    print(f"  [Crawler] Error downloading {normalized_current_url}: {e}. Skipping.")
                    continue

                # print(f"  [Crawler] HTML downloaded successfully.")

                # Step 3: Parse HTML content
                # print(f"  [Crawler] Parsing HTML content...")
                main_content_html, new_links = parse_html_content(
                    html_doc, normalized_current_url, content_selector, nav_selector, next_page_selector
                )

                if main_content_html:
                    # print(f"  [Crawler] Main content extracted. Saving to Markdown...")
                    # Step 4: Save content as Markdown
                    saved_filepath = save_content_as_markdown(normalized_current_url, main_content_html)
                    if saved_filepath:
                        print(f"  [Crawler] Content saved to: {saved_filepath}")
                    else:
                        print(f"  [Crawler] Failed to save content for {normalized_current_url}.")
                else:
                    print(f"  [Crawler] No main content found by parser for {normalized_current_url}.")

                # Step 5: Add new links to queue
                # print(f"  [Crawler] Adding {len(new_links)} new links to queue...")
                for link_url in new_links:
                    self.add_url_to_queue(link_url, current_depth + 1)

            except Exception as e:
                print(f"  [Crawler] Unhandled error processing {normalized_current_url}: {e}. Skipping.")
                # Optionally, re-add to queue with retry count, or move to a failed queue
                continue

        print("Crawling finished.")

if __name__ == '__main__':
    # Example Usage (for testing purposes, will be driven by scraper_cli.py)
    print("Running Crawler example...")
    # Mock config, replace with actual config loading
    sample_config = {
        "gemini": {"api_key": "YOUR_API_KEY"}, # Example, structure depends on D07
        "limits": {"max_pages": 5, "max_depth": 2}
    }

    # Ensure mock analyzer returns something for this test
    def mock_analyze_for_example(url, config):
        if "example.com" in url or "example.org" in url : # or "example.net" in url:
            return ("body", "nav", "a.next") # Simplified selectors
        return (None, None, None)
    analyzer.analyze_url_for_selectors = mock_analyze_for_example


    # Create dummy HTML files for local testing
    Path("temp_html_files").mkdir(exist_ok=True)
    with open("temp_html_files/example_com_page1.html", "w") as f:
        f.write("<html><head><title>Page 1</title></head><body><div id='main_content'>Page 1 content</div><nav><a href='page2.html'>Next Page (Page 2)</a> <a href='http://example.org/otherpage'>Other Domain</a></nav></body></html>")
    with open("temp_html_files/example_com_page2.html", "w") as f:
        f.write("<html><head><title>Page 2</title></head><body><div id='main_content'>Page 2 content. No more links.</div><nav></nav></body></html>")
    with open("temp_html_files/example_org_otherpage.html", "w") as f:
        f.write("<html><head><title>Other Page</title></head><body><div id='main_content'>Other domain content.</div></body></html>")


    original_requests_get = requests.get
    def mock_requests_get(url, timeout, headers):
        print(f"    Mocking requests.get for: {url}")
        parsed_url = urlparse(url)
        # Simplified local file mapping
        if parsed_url.netloc == "example.com":
            filename = "temp_html_files/example_com_" + Path(parsed_url.path).name
            if Path(filename).exists():
                mock_response = requests.Response()
                mock_response.status_code = 200
                with open(filename, "r") as f_html:
                    mock_response._content = f_html.read().encode('utf-8')
                return mock_response
        elif parsed_url.netloc == "example.org": # For testing same-domain logic
             filename = "temp_html_files/example_org_" + Path(parsed_url.path).name
             if Path(filename).exists():
                mock_response = requests.Response()
                mock_response.status_code = 200
                with open(filename, "r") as f_html:
                    mock_response._content = f_html.read().encode('utf-8')
                return mock_response

        # Fallback for unmocked URLs or if file not found
        mock_response = requests.Response()
        mock_response.status_code = 404
        mock_response._content = b"<html><body>Mock Not Found</body></html>"
        return mock_response

    requests.get = mock_requests_get

    # Test the crawler
    # Note: The output directory d4jules/output/ will be created if it doesn't exist.
    # Clean it up manually after test if needed.

    crawler = Crawler(
        base_url="http://example.com/page1.html",
        config=sample_config,
        max_pages=sample_config.get("limits", {}).get("max_pages"),
        max_depth=sample_config.get("limits", {}).get("max_depth")
    )
    crawler.start_crawling()

    # Restore original requests.get
    requests.get = original_requests_get
    # Clean up dummy files
    # shutil.rmtree("temp_html_files")
    # shutil.rmtree("d4jules/output") # Be careful with this one

    print("Crawler example finished.")
