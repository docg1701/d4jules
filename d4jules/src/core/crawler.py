import collections
from urllib.parse import urlparse, urlunparse

class Crawler:
    """
    Manages the queue of URLs to visit and keeps track of visited URLs
    to prevent re-crawling and loops.
    """

    def __init__(self):
        self.to_visit_queue = collections.deque()
        self.visited_urls = set()
        # Using a set for queue_set for efficient "in queue" checks
        self._queue_set = set()

    def _normalize_url(self, url: str) -> str:
        """
        Normalizes a URL by:
        - Ensuring http or https scheme.
        - Removing fragments (#...).
        - Removing trailing slashes from the path.
        - Lowercasing scheme and netloc.
        """
        if not url:
            return ""

        parsed = urlparse(url)

        # Ensure scheme, default to https if missing and looks like a domain
        scheme = parsed.scheme.lower()
        if not scheme and parsed.netloc:
            scheme = "https"
        elif scheme not in ["http", "https"]:
             # If scheme is something else (e.g. 'ftp', 'mailto'), it's not a web URL we want
            return ""


        netloc = parsed.netloc.lower()
        path = parsed.path

        # Remove trailing slash from path if path is not just "/"
        if path != '/' and path.endswith('/'):
            path = path[:-1]

        # Reconstruct URL without fragment and with normalized parts
        # Params and query are kept as is
        normalized_url = urlunparse((scheme, netloc, path, parsed.params, parsed.query, ''))
        return normalized_url

    def add_url(self, url: str):
        """
        Adds a URL to the visit queue if it's valid, not already visited,
        and not already in the queue.
        Performs normalization before adding.
        """
        if not url or not isinstance(url, str):
            return

        normalized_url = self._normalize_url(url)

        if not normalized_url: # If normalization results in empty (e.g. invalid scheme)
            return

        if normalized_url not in self.visited_urls and normalized_url not in self._queue_set:
            self.to_visit_queue.append(normalized_url)
            self._queue_set.add(normalized_url)
            # print(f"Added to queue: {normalized_url}") # For debugging

    def add_urls(self, urls: list[str]):
        """
        Adds a list of URLs to the visit queue.
        """
        if not urls:
            return
        for url in urls:
            self.add_url(url)

    def get_next_url(self) -> str | None:
        """
        Retrieves and removes the next URL from the queue.
        Returns None if the queue is empty.
        Also marks the URL as visited when retrieved.
        """
        if not self.to_visit_queue:
            return None

        next_url = self.to_visit_queue.popleft()
        self._queue_set.remove(next_url) # Remove from queue tracking set
        self.mark_as_visited(next_url) # Mark as visited when it's taken to be processed
        return next_url

    def mark_as_visited(self, url: str):
        """
        Marks a given URL as visited. Normalizes before adding.
        """
        if not url or not isinstance(url, str):
            return
        normalized_url = self._normalize_url(url)
        if normalized_url:
            self.visited_urls.add(normalized_url)
            # print(f"Marked as visited: {normalized_url}") # For debugging

    def has_next_url(self) -> bool:
        """
        Checks if there are more URLs in the queue.
        """
        return bool(self.to_visit_queue)

    def get_queue_size(self) -> int:
        """Returns the current size of the to_visit_queue."""
        return len(self.to_visit_queue)

    def get_visited_count(self) -> int:
        """Returns the current count of visited URLs."""
        return len(self.visited_urls)

if __name__ == '__main__':
    # Basic demonstration of the Crawler class
    crawler = Crawler()

    print("Initial state:")
    print(f"Queue: {crawler.to_visit_queue}, Visited: {crawler.visited_urls}")
    print(f"Has next: {crawler.has_next_url()}, Queue size: {crawler.get_queue_size()}, Visited count: {crawler.get_visited_count()}")

    urls_to_add = [
        "http://example.com/page1",
        "https://example.com/page1/", # Should normalize to the same as above
        "http://example.com/page2#section1", # Fragment should be removed
        "HTTPS://EXAMPLE.COM/PAGE3", # Scheme and netloc to be lowercased
        None, # Invalid
        "", # Invalid
        "ftp://example.com/file", # Invalid scheme
        "example.com/page4" # Should be normalized to https://example.com/page4
    ]

    print(f"\nAdding URLs: {urls_to_add}")
    crawler.add_urls(urls_to_add)
    print(f"Queue after adding: {list(crawler.to_visit_queue)}") # Show as list for clarity
    print(f"Internal queue set: {crawler._queue_set}")
    print(f"Visited: {crawler.visited_urls}")
    print(f"Has next: {crawler.has_next_url()}, Queue size: {crawler.get_queue_size()}, Visited count: {crawler.get_visited_count()}")

    print("\nProcessing URLs:")
    while crawler.has_next_url():
        url = crawler.get_next_url()
        print(f"Processing: {url}")
        # In a real scenario, this is where fetching and parsing would happen
        # Then new links found would be added back using crawler.add_urls([...])
        if url == "https://example.com/page1":
            print("  (Simulating finding new links on page1)")
            crawler.add_urls(["http://example.com/page1/subpageA", "https://example.com/page2"]) # page2 already visited/queued

    print("\nFinal state:")
    print(f"Queue: {list(crawler.to_visit_queue)}")
    print(f"Visited: {crawler.visited_urls}")
    print(f"Has next: {crawler.has_next_url()}, Queue size: {crawler.get_queue_size()}, Visited count: {crawler.get_visited_count()}")

    print("\nTesting adding already visited URL:")
    crawler.add_url("http://example.com/page1") # Already visited
    print(f"Queue size after trying to re-add visited: {crawler.get_queue_size()}")

    print("\nTesting _normalize_url directly:")
    print(f"'http://Domain.Com/Path/?query=Yes#frag' -> '{crawler._normalize_url('http://Domain.Com/Path/?query=Yes#frag')}'")
    print(f"'no-scheme.com/path' -> '{crawler._normalize_url('no-scheme.com/path')}'")
    print(f"'mailto:user@example.com' -> '{crawler._normalize_url('mailto:user@example.com')}' (should be empty)")
```
