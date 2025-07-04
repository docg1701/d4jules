import unittest
from urllib.parse import urlparse # For potential direct use in tests if needed for assertions

# Assuming src is in PYTHONPATH or tests are run from project root
from src.core.crawler import Crawler

class TestCrawler(unittest.TestCase):

    def test_initialization_empty(self):
        crawler = Crawler()
        self.assertEqual(crawler.base_url, "")
        self.assertEqual(crawler.get_queue_size(), 0)
        self.assertEqual(crawler.get_visited_count(), 0)
        self.assertIsNone(crawler.max_pages)
        self.assertIsNone(crawler.max_depth)

    def test_initialization_with_base_url(self):
        base = "https://example.com"
        crawler = Crawler(base_url=base)
        self.assertEqual(crawler.base_url, base)
        self.assertEqual(crawler.get_queue_size(), 1)
        self.assertEqual(crawler.get_visited_count(), 0)
        # _normalize_url makes "https://example.com" -> "https://example.com/"
        self.assertIn("https://example.com/", crawler._queue_set)

    def test_normalize_url(self):
        crawler = Crawler()
        # Test cases for _normalize_url
        # Note: _normalize_url is a private method, so we test its effects via public methods
        # or by calling it directly for focused testing if we make it notionally public for tests.
        # For now, testing via add_url and inspecting internal state or get_next_url.

        test_cases = {
            "http://example.com": "http://example.com/",
            "https://example.com/path": "https://example.com/path",
            "https://Example.com/Path": "https://example.com/Path", # Scheme/netloc lowercased
            "https://example.com/path#fragment": "https://example.com/path",
            "https://example.com/path/": "https://example.com/path", # Trailing slash removed
            "https://example.com/": "https://example.com/", # Root trailing slash kept
            "example.com": "https://example.com/", # Scheme added
            "example.com/path": "https://example.com/path",
            "ftp://example.com": "", # Invalid scheme
            "": "", # Empty URL
            "   ": "", # Whitespace URL
            "http://": "", # Invalid (no netloc)
            "http:///path": "", # Invalid
            # Current _normalize_url does not simplify /./ or /../ path segments
            "http://example.com/a/./b/../c": "http://example.com/a/./b/../c",
        }
        for original, expected in test_cases.items():
            # Direct call for easier testing of this specific method's logic
            self.assertEqual(crawler._normalize_url(original), expected, f"Failed for: {original}")

    def test_add_url_and_get_next_url(self):
        crawler = Crawler()
        url1 = "https://example.com/page1"
        url2 = "https://example.com/page2"
        normalized_url1 = "https://example.com/page1"
        normalized_url2 = "https://example.com/page2"

        crawler.add_url(url1)
        self.assertEqual(crawler.get_queue_size(), 1)
        self.assertIn(normalized_url1, crawler._queue_set)

        crawler.add_url(url2)
        self.assertEqual(crawler.get_queue_size(), 2)
        self.assertIn(normalized_url2, crawler._queue_set)

        # Test FIFO
        self.assertEqual(crawler.get_next_url(), normalized_url1)
        self.assertEqual(crawler.get_queue_size(), 1)
        self.assertEqual(crawler.get_visited_count(), 1)
        self.assertIn(normalized_url1, crawler.visited_urls)
        self.assertNotIn(normalized_url1, crawler._queue_set)

        self.assertEqual(crawler.get_next_url(), normalized_url2)
        self.assertEqual(crawler.get_queue_size(), 0)
        self.assertEqual(crawler.get_visited_count(), 2)
        self.assertIn(normalized_url2, crawler.visited_urls)
        self.assertNotIn(normalized_url2, crawler._queue_set)

        self.assertIsNone(crawler.get_next_url()) # Empty queue

    def test_add_url_duplicates_and_visited(self):
        crawler = Crawler()
        url1 = "https://example.com/page1"
        normalized_url1 = "https://example.com/page1"

        crawler.add_url(url1)
        self.assertEqual(crawler.get_queue_size(), 1)

        # Add same URL (should be ignored as it's in _queue_set)
        crawler.add_url(url1)
        self.assertEqual(crawler.get_queue_size(), 1)

        # Add same URL but with different casing/fragment (should normalize and be ignored)
        crawler.add_url("https://Example.com/page1#frag")
        self.assertEqual(crawler.get_queue_size(), 1)

        # Mark as visited
        crawler.mark_as_visited(url1)
        self.assertEqual(crawler.get_visited_count(), 1)
        self.assertIn(normalized_url1, crawler.visited_urls)

        # Try adding again after visited (should be ignored)
        crawler.add_url(url1)
        self.assertEqual(crawler.get_queue_size(), 1) # Still 1 from original add, if not yet popped

        # Pop it, then try adding a visited URL
        retrieved_url = crawler.get_next_url()
        self.assertEqual(retrieved_url, normalized_url1)
        self.assertEqual(crawler.get_queue_size(), 0)
        self.assertIn(normalized_url1, crawler.visited_urls) # Visited set by get_next_url

        crawler.add_url(url1) # Should not be added as it's in visited_urls
        self.assertEqual(crawler.get_queue_size(), 0)


    def test_add_invalid_urls(self):
        crawler = Crawler()
        crawler.add_url(None) # type: ignore
        crawler.add_url("")
        crawler.add_url("  ")
        crawler.add_url("ftp://invalid.com")
        self.assertEqual(crawler.get_queue_size(), 0)

    def test_add_urls_list(self):
        crawler = Crawler()
        urls = [
            "https://example.com/p1",
            "https://example.com/p2",
            "https://example.com/p1", # duplicate
            "ftp://bad.com", # invalid
            "https://example.com/P2#frag" # duplicate via normalization
        ]
        crawler.add_urls(urls)
        # Expected: "https://example.com/p1", "https://example.com/p2", "https://example.com/P2"
        self.assertEqual(crawler.get_queue_size(), 3)
        self.assertIn("https://example.com/p1", crawler._queue_set)
        self.assertIn("https://example.com/p2", crawler._queue_set)
        self.assertIn("https://example.com/P2", crawler._queue_set) # Path casing is preserved

    def test_mark_as_visited(self):
        crawler = Crawler()
        url = "https://example.com/path"
        normalized_url = "https://example.com/path"
        crawler.mark_as_visited(url)
        self.assertIn(normalized_url, crawler.visited_urls)
        self.assertEqual(crawler.get_visited_count(), 1)

        # Mark again
        crawler.mark_as_visited(url + "#frag")
        self.assertEqual(crawler.get_visited_count(), 1) # Count should not increase

    def test_state_methods(self):
        crawler = Crawler()
        self.assertFalse(crawler.has_next_url())
        self.assertEqual(crawler.get_queue_size(), 0)
        self.assertEqual(crawler.get_visited_count(), 0)

        crawler.add_url("https://example.com/one")
        self.assertTrue(crawler.has_next_url())
        self.assertEqual(crawler.get_queue_size(), 1)
        self.assertEqual(crawler.get_visited_count(), 0)

        crawler.get_next_url()
        self.assertFalse(crawler.has_next_url())
        self.assertEqual(crawler.get_queue_size(), 0)
        self.assertEqual(crawler.get_visited_count(), 1)

    def test_can_crawl_url_domain_scoping(self):
        base = "https://docs.example.com/product/"
        crawler = Crawler(base_url=base) # Base URL is normalized to "https://docs.example.com/product"

        # Test cases for can_crawl_url
        # Normalization of base_url by Crawler's add_url:
        # "https://docs.example.com/product/" becomes "https://docs.example.com/product"
        # But _normalize_url for can_crawl_url will normalize the base again.
        # The effective base netloc is "docs.example.com"

        self.assertTrue(crawler.can_crawl_url("https://docs.example.com/product/page1"))
        self.assertTrue(crawler.can_crawl_url("https://docs.example.com/other"))
        self.assertTrue(crawler.can_crawl_url("http://docs.example.com/another")) # Scheme difference ok if netloc matches

        self.assertFalse(crawler.can_crawl_url("https://api.example.com/data")) # Different subdomain
        self.assertFalse(crawler.can_crawl_url("https://example.com/product")) # Parent domain
        self.assertFalse(crawler.can_crawl_url("https://another.domain.com")) # Different domain
        self.assertFalse(crawler.can_crawl_url("ftp://docs.example.com")) # Invalid scheme for comparison
        self.assertFalse(crawler.can_crawl_url("")) # Invalid URL

        # Test with no base_url (should always be true for valid URLs)
        crawler_no_base = Crawler()
        self.assertTrue(crawler_no_base.can_crawl_url("https://any.valid.url.com/path"))
        self.assertFalse(crawler_no_base.can_crawl_url("ftp://invalid.scheme.com")) # Still respects valid URL structure
        self.assertFalse(crawler_no_base.can_crawl_url(""))

if __name__ == '__main__':
    unittest.main()
