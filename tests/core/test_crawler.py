import unittest
import collections # For direct comparison if needed, though Crawler uses it internally
from d4jules.src.core.crawler import Crawler # Assuming direct import works

class TestCrawler(unittest.TestCase):

    def setUp(self):
        """Common setup for test methods."""
        self.base_url = "http://example.com"
        # Provide a minimal config; specific tests can override or use a more detailed one
        self.sample_config = {
            "gemini": {"api_key": "TEST_API_KEY"},
            "output": {"markdown_dir": "test_output/markdown"},
            "crawler_limits": {"max_pages": 10, "max_depth": 3}
        }
        self.crawler = Crawler(base_url=self.base_url, config=self.sample_config)

    def test_initialization(self):
        self.assertEqual(self.crawler.get_queue_size(), 1) # base_url is added
        self.assertEqual(self.crawler.get_visited_count(), 0)
        self.assertTrue(self.crawler.has_next_url())
        # Test _queue_set initialization
        self.assertIn(self.crawler._normalize_url(self.base_url), self.crawler._queue_set)

    def test_normalize_url(self):
        # Test cases: (input_url, expected_normalized_url)
        test_cases = [
            ("http://Example.com/Path/", "http://example.com/Path"),
            ("https://example.com/path?query=1#fragment", "https://example.com/path?query=1"),
            ("http://example.com", "http://example.com/"), # Expect trailing slash for root
            ("https://example.com/", "https://example.com/"), # Expect trailing slash for root
            ("example.com/test", "https://example.com/test"), # Default to https
            ("ftp://example.com/file", ""), # Unsupported scheme
            # urllib.parse does not normalize /./ or /../ from paths by default
            ("http://example.com/path/./../other", "http://example.com/path/./../other"),
            ("", ""),
            (None, ""),
            ("http://localhost:8000", "http://localhost:8000/"), # Expect trailing slash for root
            ("HTTPS://EXAMPLE.COM/UPPER", "https://example.com/UPPER")
        ]
        for input_url, expected in test_cases:
            with self.subTest(input_url=input_url):
                self.assertEqual(self.crawler._normalize_url(input_url), expected)

    def test_add_url_new_and_valid(self):
        self.crawler.to_visit_queue.clear() # Start fresh for this test
        self.crawler._queue_set.clear()

        url = "http://example.com/page1"
        normalized_url = self.crawler._normalize_url(url)

        self.crawler.add_url(url)
        self.assertEqual(self.crawler.get_queue_size(), 1)
        self.assertIn(normalized_url, self.crawler.to_visit_queue)
        self.assertIn(normalized_url, self.crawler._queue_set)

    def test_add_url_already_visited(self):
        url = "http://example.com/visited_page"
        normalized_url = self.crawler._normalize_url(url)

        self.crawler.mark_as_visited(url) # Mark as visited
        self.assertEqual(self.crawler.get_visited_count(), 1) # base_url + this one

        # Clear queue to ensure it's not added
        self.crawler.to_visit_queue.clear()
        self.crawler._queue_set.clear()

        self.crawler.add_url(url)
        self.assertEqual(self.crawler.get_queue_size(), 0, "URL already visited should not be added to queue")

    def test_add_url_already_in_queue(self):
        self.crawler.to_visit_queue.clear()
        self.crawler._queue_set.clear()

        url = "http://example.com/in_queue_page"
        self.crawler.add_url(url) # Add once
        self.assertEqual(self.crawler.get_queue_size(), 1)

        self.crawler.add_url(url) # Add again
        self.assertEqual(self.crawler.get_queue_size(), 1, "URL already in queue should not be added again")

    def test_add_url_invalid_and_empty(self):
        initial_size = self.crawler.get_queue_size()
        invalid_urls = ["ftp://example.com", "", None, "just_text"]
        for url in invalid_urls:
            self.crawler.add_url(url)
        self.assertEqual(self.crawler.get_queue_size(), initial_size, "Invalid or empty URLs should not be added")

    def test_add_urls_list(self):
        self.crawler.to_visit_queue.clear()
        self.crawler._queue_set.clear()
        self.crawler.visited_urls.clear()

        urls_to_add = [
            "http://example.com/listpage1",
            "http://example.com/listpage2",
            "http://example.com/listpage1" # duplicate in list
        ]
        self.crawler.add_urls(urls_to_add)
        self.assertEqual(self.crawler.get_queue_size(), 2) # Only unique, valid URLs
        self.assertIn(self.crawler._normalize_url("http://example.com/listpage1"), self.crawler._queue_set)
        self.assertIn(self.crawler._normalize_url("http://example.com/listpage2"), self.crawler._queue_set)

    def test_get_next_url_fifo_and_visit_marking(self):
        self.crawler.to_visit_queue.clear()
        self.crawler._queue_set.clear()
        self.crawler.visited_urls.clear()

        url1 = "http://example.com/fifo1"
        url2 = "http://example.com/fifo2"
        norm_url1 = self.crawler._normalize_url(url1)
        norm_url2 = self.crawler._normalize_url(url2)

        self.crawler.add_url(url1)
        self.crawler.add_url(url2)

        self.assertEqual(self.crawler.get_queue_size(), 2)

        next_url = self.crawler.get_next_url()
        self.assertEqual(next_url, norm_url1)
        self.assertIn(norm_url1, self.crawler.visited_urls)
        self.assertNotIn(norm_url1, self.crawler._queue_set) # Removed from queue_set
        self.assertEqual(self.crawler.get_queue_size(), 1)
        self.assertEqual(self.crawler.get_visited_count(), 1)

        next_url_2 = self.crawler.get_next_url()
        self.assertEqual(next_url_2, norm_url2)
        self.assertIn(norm_url2, self.crawler.visited_urls)
        self.assertNotIn(norm_url2, self.crawler._queue_set)
        self.assertEqual(self.crawler.get_queue_size(), 0)
        self.assertEqual(self.crawler.get_visited_count(), 2)

        self.assertIsNone(self.crawler.get_next_url(), "Should return None when queue is empty")

    def test_mark_as_visited(self):
        url = "http://example.com/marked_page"
        normalized_url = self.crawler._normalize_url(url)

        self.crawler.mark_as_visited(url)
        self.assertIn(normalized_url, self.crawler.visited_urls)

    def test_has_next_url(self):
        self.crawler.to_visit_queue.clear()
        self.crawler._queue_set.clear()
        self.assertFalse(self.crawler.has_next_url())

        self.crawler.add_url("http://example.com/another")
        self.assertTrue(self.crawler.has_next_url())

        self.crawler.get_next_url()
        self.assertFalse(self.crawler.has_next_url())

    def test_status_methods_get_counts(self):
        self.crawler.to_visit_queue.clear()
        self.crawler._queue_set.clear()
        self.crawler.visited_urls.clear()

        self.assertEqual(self.crawler.get_queue_size(), 0)
        self.assertEqual(self.crawler.get_visited_count(), 0)

        self.crawler.add_url("http://example.com/count_test1")
        self.crawler.add_url("http://example.com/count_test2")
        self.assertEqual(self.crawler.get_queue_size(), 2)

        self.crawler.get_next_url()
        self.assertEqual(self.crawler.get_queue_size(), 1)
        self.assertEqual(self.crawler.get_visited_count(), 1)

    def test_can_crawl_url_same_domain(self):
        crawler_strict = Crawler(base_url="http://example.com/docs/main", config=self.sample_config)
        self.assertTrue(crawler_strict.can_crawl_url("http://example.com/docs/page1"))
        self.assertTrue(crawler_strict.can_crawl_url("http://example.com/other_path"))
        self.assertFalse(crawler_strict.can_crawl_url("http://anotherdomain.com"))
        self.assertFalse(crawler_strict.can_crawl_url("https://sub.example.com")) # subdomain is different netloc

    def test_can_crawl_url_no_base_url_set(self):
        crawler_no_base = Crawler(config=self.sample_config) # No base_url
        self.assertTrue(crawler_no_base.can_crawl_url("http://anydomain.com/page")) # Should allow any if no base

    def test_normalize_url_path_edge_cases(self):
        # urllib.parse does not collapse multiple slashes in path segments
        self.assertEqual(self.crawler._normalize_url("http://example.com//path//to///page"), "http://example.com//path//to///page")
        # Normalizing a path that is just "." or ".." relative to a domain
        # often results in the domain itself or the path as is, depending on interpretation.
        # Current _normalize_url with path.endswith('/') removal:
        self.assertEqual(self.crawler._normalize_url("http://example.com/."), "http://example.com/.")
        self.assertEqual(self.crawler._normalize_url("http://example.com/.."), "http://example.com/..")

    def test_add_url_with_different_case_netloc(self):
        self.crawler.to_visit_queue.clear()
        self.crawler._queue_set.clear()
        self.crawler.visited_urls.clear()

        url_lower = "http://example.com/path"
        url_upper_netloc = "http://EXAMPLE.COM/path"
        self.crawler.add_url(url_lower)
        self.assertEqual(self.crawler.get_queue_size(), 1)
        # Adding the same URL with different netloc case should be treated as duplicate due to normalization
        self.crawler.add_url(url_upper_netloc)
        self.assertEqual(self.crawler.get_queue_size(), 1)
        self.assertIn(self.crawler._normalize_url(url_lower), self.crawler._queue_set)


if __name__ == '__main__':
    unittest.main()
