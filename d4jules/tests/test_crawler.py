import unittest
from unittest.mock import patch, MagicMock, call
from collections import deque
from pathlib import Path
import tempfile
import shutil
import requests # Import for requests.exceptions.RequestException

# Temporarily adjust path to import Crawler, assuming tests are run from project root
import sys
# sys.path.insert(0, str(Path(__file__).resolve().parent.parent)) # Adjust if d4jules is not directly in PYTHONPATH

from d4jules.core.crawler import Crawler

# Mock config that load_config would provide
MOCK_CONFIG_DEFAULT = {
    "gemini": {"api_key": "TEST_API_KEY"},
    "crawler_limits": {"max_pages": "5", "max_depth": "2"}, # Values are strings as from configparser
    "output": {"directory": "d4jules/output"} # Assuming writer uses this, though Crawler passes it.
}

# A more specific mock config for some tests
MOCK_CONFIG_NO_LIMITS = {
    "gemini": {"api_key": "TEST_API_KEY"},
    "crawler_limits": {},
    "output": {"directory": "d4jules/output"}
}


class TestCrawler(unittest.TestCase):

    def setUp(self):
        self.test_output_dir = Path(tempfile.mkdtemp())
        # Ensure a clean state for each test by resetting where modules are patched
        # Path to the modules as they would be imported by crawler.py
        self.analyzer_patch_path = 'd4jules.core.crawler.analyzer' # Mocking the 'analyzer' instance used in crawler.py
        self.requests_patch_path = 'd4jules.core.crawler.requests.get'
        self.parser_patch_path = 'd4jules.core.crawler.parse_html_content'
        self.writer_patch_path = 'd4jules.core.crawler.save_content_as_markdown'

        # Start all patchers
        self.patcher_analyzer = patch(self.analyzer_patch_path)
        self.patcher_requests = patch(self.requests_patch_path)
        self.patcher_parser = patch(self.parser_patch_path)
        self.patcher_writer = patch(self.writer_patch_path)

        self.mock_analyzer = self.patcher_analyzer.start()
        self.mock_requests_get = self.patcher_requests.start()
        self.mock_parser = self.patcher_parser.start()
        self.mock_writer = self.patcher_writer.start()

        # Default mock behaviors
        self.mock_analyzer.analyze_url_for_selectors.return_value = ("#content", "nav", ".next")
        mock_response = MagicMock()
        mock_response.text = "<html><body>Mock HTML</body></html>"
        mock_response.status_code = 200
        self.mock_requests_get.return_value = mock_response
        self.mock_parser.return_value = ("<p>Content</p>", ["http://example.com/link2"])
        self.mock_writer.return_value = str(self.test_output_dir / "mock_saved_file.md")


    def tearDown(self):
        shutil.rmtree(self.test_output_dir)
        # Stop all patchers
        self.patcher_analyzer.stop()
        self.patcher_requests.stop()
        self.patcher_parser.stop()
        self.patcher_writer.stop()

    def _get_config_for_crawler(self, custom_config_dict=None):
        # Helper to simulate configparser object from dict
        from configparser import ConfigParser
        config = ConfigParser()
        config.read_dict(custom_config_dict if custom_config_dict else MOCK_CONFIG_DEFAULT)
        return config

    def test_initialization(self):
        crawler = Crawler("http://example.com", self._get_config_for_crawler(), max_pages=10, max_depth=3)
        self.assertEqual(crawler.base_url, "http://example.com")
        self.assertEqual(crawler.base_domain, "example.com")
        self.assertEqual(crawler.max_pages, 10)
        self.assertEqual(crawler.max_depth, 3)
        self.assertEqual(len(crawler.url_queue), 0) # Queue populated by start_crawling
        self.assertEqual(len(crawler.visited_urls), 0)

    def test_is_same_domain(self):
        crawler = Crawler("http://example.com", self._get_config_for_crawler())
        self.assertTrue(crawler._is_same_domain("http://example.com/page1"))
        self.assertTrue(crawler._is_same_domain("https://example.com/page2")) # Scheme difference is ok for netloc
        self.assertFalse(crawler._is_same_domain("http://sub.example.com/page3")) # Subdomain is different netloc
        self.assertFalse(crawler._is_same_domain("http://otherexample.com/page4"))
        self.assertTrue(crawler._is_same_domain("http://example.com")) # Root

    def test_add_url_to_queue(self):
        crawler = Crawler("http://example.com", self._get_config_for_crawler(MOCK_CONFIG_NO_LIMITS))
        crawler.add_url_to_queue("http://example.com/page1", 0)
        self.assertEqual(len(crawler.url_queue), 1)
        # Add same URL (should be normalized and ignored if already effectively in queue or visited)
        # For this test, queue is empty initially, so it's fine
        crawler.add_url_to_queue("http://example.com/page1#frag", 0)
        # Simple queue check doesn't prevent adding if not visited. Let's assume start_crawling handles visited.
        # The current add_url_to_queue check for "already in queue" is basic.
        # This test will pass because the mock queue is simple.
        # A better test would mock the queue or test _normalize_url separately.
        # For now, let's check distinct normalized URLs
        crawler.add_url_to_queue("http://example.com/page2", 0)
        self.assertEqual(len(crawler.url_queue), 2)
        crawler.add_url_to_queue("http://otherexample.com/page3", 0) # Different domain
        self.assertEqual(len(crawler.url_queue), 2) # Should not add

    def test_max_depth_respected_in_add_url(self):
        crawler = Crawler("http://example.com", self._get_config_for_crawler(), max_depth=1)
        crawler.add_url_to_queue("http://example.com/depth0", 0)
        crawler.add_url_to_queue("http://example.com/depth1", 1)
        crawler.add_url_to_queue("http://example.com/depth2_too_deep", 2)
        self.assertIn(("http://example.com/depth0", 0), crawler.url_queue)
        self.assertIn(("http://example.com/depth1", 1), crawler.url_queue)
        self.assertNotIn(("http://example.com/depth2_too_deep", 2), crawler.url_queue)


    def test_start_crawling_single_page(self):
        crawler = Crawler("http://example.com/page1", self._get_config_for_crawler(), max_pages=1)
        # Mock parser to return no new links to stop after one page
        self.mock_parser.return_value = ("<p>Content page 1</p>", [])

        crawler.start_crawling()

        self.mock_analyzer.analyze_url_for_selectors.assert_called_once_with("http://example.com/page1", crawler.config)
        self.mock_requests_get.assert_called_once_with("http://example.com/page1", timeout=10, headers=unittest.mock.ANY)
        self.mock_parser.assert_called_once_with("<html><body>Mock HTML</body></html>", "http://example.com/page1", "#content", "nav", ".next")
        self.mock_writer.assert_called_once_with("http://example.com/page1", "<p>Content page 1</p>")
        self.assertEqual(crawler.pages_processed_count, 1)
        self.assertIn("http://example.com/page1", crawler.visited_urls)

    def test_start_crawling_follows_links_respects_max_pages(self):
        base_url = "http://example.com/home"
        crawler = Crawler(base_url, self._get_config_for_crawler(), max_pages=2)

        # Define side effects for parser to simulate link discovery
        # Page 1 -> Page 2
        # Page 2 -> No new links
        def parser_side_effect(html, url, cs, ns, nps):
            if url == "http://example.com/home":
                return ("<p>Home content</p>", ["http://example.com/page2"])
            elif url == "http://example.com/page2":
                return ("<p>Page 2 content</p>", [])
            return (None, [])
        self.mock_parser.side_effect = parser_side_effect

        crawler.start_crawling()

        self.assertEqual(self.mock_analyzer.analyze_url_for_selectors.call_count, 2)
        self.mock_analyzer.analyze_url_for_selectors.assert_any_call("http://example.com/home", crawler.config)
        self.mock_analyzer.analyze_url_for_selectors.assert_any_call("http://example.com/page2", crawler.config)

        self.assertEqual(self.mock_requests_get.call_count, 2)
        self.assertEqual(self.mock_parser.call_count, 2)
        self.assertEqual(self.mock_writer.call_count, 2)
        self.assertEqual(crawler.pages_processed_count, 2)
        self.assertIn("http://example.com/home", crawler.visited_urls)
        self.assertIn("http://example.com/page2", crawler.visited_urls)

    def test_start_crawling_respects_max_depth(self):
        # Depth: 0 -> 1 -> 2 (stop)
        crawler = Crawler("http://example.com/level0", self._get_config_for_crawler(), max_depth=1, max_pages=10) # max_pages high enough

        def parser_side_effect(html, url, cs, ns, nps):
            if url == "http://example.com/level0":
                return ("Content L0", ["http://example.com/level1"])
            elif url == "http://example.com/level1":
                return ("Content L1", ["http://example.com/level2_not_crawled"]) # This link should be added but not processed
            return (None, [])
        self.mock_parser.side_effect = parser_side_effect

        crawler.start_crawling()

        # Should process level0 and level1
        self.assertEqual(crawler.pages_processed_count, 2)
        self.assertIn("http://example.com/level0", crawler.visited_urls)
        self.assertIn("http://example.com/level1", crawler.visited_urls)
        self.assertNotIn("http://example.com/level2_not_crawled", crawler.visited_urls) # Not processed

        # Check if level2_not_crawled was considered for queueing (it should be, but then dropped by depth in main loop or add_url)
        # The add_url_to_queue itself should prevent adding if depth > max_depth
        # So, it should not even be in the queue if add_url_to_queue is correct
        found_in_queue = False
        for url_in_q, _ in crawler.url_queue: # Check remaining queue
            if url_in_q == "http://example.com/level2_not_crawled":
                found_in_q = True
                break
        self.assertFalse(found_in_queue, "URL deeper than max_depth should not be in queue if add_url_to_queue works correctly")


    def test_error_in_analyzer(self):
        self.mock_analyzer.analyze_url_for_selectors.return_value = None # Simulate analyzer failure
        crawler = Crawler("http://example.com/page_analyzer_fails", self._get_config_for_crawler(), max_pages=1)
        crawler.start_crawling()

        self.mock_analyzer.analyze_url_for_selectors.assert_called_once()
        self.mock_requests_get.assert_not_called() # Should skip download if no selectors
        self.mock_parser.assert_not_called()
        self.mock_writer.assert_not_called()
        self.assertEqual(crawler.pages_processed_count, 1) # Processed, but failed internally

    def test_error_in_requests_get(self):
        self.mock_requests_get.side_effect = requests.exceptions.RequestException("Test network error")
        crawler = Crawler("http://example.com/page_download_fails", self._get_config_for_crawler(), max_pages=1)
        crawler.start_crawling()

        self.mock_analyzer.analyze_url_for_selectors.assert_called_once()
        self.mock_requests_get.assert_called_once()
        self.mock_parser.assert_not_called() # Should skip if download fails
        self.mock_writer.assert_not_called()
        self.assertEqual(crawler.pages_processed_count, 1)

    def test_error_in_parser(self):
        self.mock_parser.side_effect = Exception("Test parsing error")
        crawler = Crawler("http://example.com/page_parser_fails", self._get_config_for_crawler(), max_pages=1)
        crawler.start_crawling()

        self.mock_analyzer.analyze_url_for_selectors.assert_called_once()
        self.mock_requests_get.assert_called_once()
        self.mock_parser.assert_called_once()
        self.mock_writer.assert_not_called() # Should skip if parse fails
        self.assertEqual(crawler.pages_processed_count, 1)

    def test_error_in_writer(self):
        self.mock_writer.return_value = None # Simulate writer failure
        crawler = Crawler("http://example.com/page_writer_fails", self._get_config_for_crawler(), max_pages=1)
        crawler.start_crawling()

        self.mock_analyzer.analyze_url_for_selectors.assert_called_once()
        self.mock_requests_get.assert_called_once()
        self.mock_parser.assert_called_once()
        self.mock_writer.assert_called_once() # Writer is called, but returns None
        self.assertEqual(crawler.pages_processed_count, 1)

    def test_normalize_url_removes_fragment(self):
        crawler = Crawler("http://example.com", self._get_config_for_crawler())
        self.assertEqual(crawler._normalize_url("http://example.com/page#section1"), "http://example.com/page")
        self.assertEqual(crawler._normalize_url("http://example.com/page?q=1#section1"), "http://example.com/page?q=1")


if __name__ == '__main__':
    unittest.main()
