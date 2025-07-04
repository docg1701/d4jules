import unittest
from unittest.mock import MagicMock, patch
import requests

# Assuming src is in PYTHONPATH or tests are run from project root
from src.core.crawler import Crawler
from src.core.analyzer import HtmlSelectors, AnalyzerError, NetworkError, LLMAnalysisError # For mocking and error simulation

class TestCrawler(unittest.TestCase):

    def setUp(self):
        self.mock_analyzer_func = MagicMock()
        self.mock_parser_func = MagicMock()
        self.mock_writer_func = MagicMock()
        self.mock_analyzer_config = {'api_key': 'test_key', 'model_name': 'test_model'}
        self.default_output_dir = "test_output_dir"

        # Default crawler instance for tests that don't need specific setup for these mocks
        self.crawler = Crawler(
            analyzer_func=self.mock_analyzer_func,
            parser_func=self.mock_parser_func,
            writer_func=self.mock_writer_func,
            analyzer_config=self.mock_analyzer_config,
            output_dir=self.default_output_dir
        )

    def test_initialization_empty_with_mocks(self):
        # Test initialization without base_url but with required functions
        crawler = Crawler(
            analyzer_func=self.mock_analyzer_func,
            parser_func=self.mock_parser_func,
            writer_func=self.mock_writer_func,
            analyzer_config=self.mock_analyzer_config,
            output_dir=self.default_output_dir
        )
        self.assertEqual(crawler.base_url, "")
        self.assertEqual(crawler.get_queue_size(), 0)
        self.assertEqual(crawler.get_visited_count(), 0)
        self.assertIsNone(crawler.max_pages)
        self.assertIsNone(crawler.max_depth)
        self.assertEqual(crawler.analyzer_func, self.mock_analyzer_func)
        self.assertEqual(crawler.parser_func, self.mock_parser_func)
        self.assertEqual(crawler.writer_func, self.mock_writer_func)
        self.assertEqual(crawler.analyzer_config, self.mock_analyzer_config)
        self.assertEqual(crawler.output_dir, self.default_output_dir)


    def test_initialization_missing_funcs_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "analyzer_func, parser_func, and writer_func must be provided."):
            Crawler(parser_func=self.mock_parser_func, writer_func=self.mock_writer_func)
        with self.assertRaisesRegex(ValueError, "analyzer_func, parser_func, and writer_func must be provided."):
            Crawler(analyzer_func=self.mock_analyzer_func, writer_func=self.mock_writer_func)
        with self.assertRaisesRegex(ValueError, "analyzer_func, parser_func, and writer_func must be provided."):
            Crawler(analyzer_func=self.mock_analyzer_func, parser_func=self.mock_parser_func)


    def test_initialization_with_base_url_and_mocks(self):
        base = "https://example.com"
        crawler = Crawler(
            base_url=base,
            analyzer_func=self.mock_analyzer_func,
            parser_func=self.mock_parser_func,
            writer_func=self.mock_writer_func,
            analyzer_config=self.mock_analyzer_config
        )
        self.assertEqual(crawler.base_url, base)
        self.assertEqual(crawler.get_queue_size(), 1) # Base URL is added
        self.assertEqual(crawler.get_visited_count(), 0)
        self.assertIn("https://example.com/", crawler._queue_set)


    def test_normalize_url(self):
        # This test remains largely the same as it tests a private utility method
        # whose direct behavior hasn't changed.
        # Instantiating a crawler with mocks for this test.
        test_cases = {
            "http://example.com": "http://example.com/",
            "https://example.com/path": "https://example.com/path",
            "https://Example.com/Path": "https://example.com/Path",
            "https://example.com/path#fragment": "https://example.com/path",
            "https://example.com/path/": "https://example.com/path",
            "https://example.com/": "https://example.com/",
            "example.com": "https://example.com/",
            "example.com/path": "https://example.com/path",
            "ftp://example.com": "",
            "": "",
            "   ": "",
            "http://": "",
            "http:///path": "",
            "http://example.com/a/./b/../c": "http://example.com/a/./b/../c",
        }
        for original, expected in test_cases.items():
            self.assertEqual(self.crawler._normalize_url(original), expected, f"Failed for: {original}")

    def test_add_url_and_get_next_url(self):
        url1 = "https://example.com/page1"
        url2 = "https://example.com/page2"
        normalized_url1 = self.crawler._normalize_url(url1)
        normalized_url2 = self.crawler._normalize_url(url2)

        self.crawler.add_url(url1, depth=0)
        self.assertEqual(self.crawler.get_queue_size(), 1)
        self.assertIn(normalized_url1, self.crawler._queue_set)
        # Check if the item in queue is a tuple (url, depth)
        self.assertEqual(self.crawler.to_visit_queue[0], (normalized_url1, 0))


        self.crawler.add_url(url2, depth=0)
        self.assertEqual(self.crawler.get_queue_size(), 2)
        self.assertIn(normalized_url2, self.crawler._queue_set)
        self.assertEqual(self.crawler.to_visit_queue[1], (normalized_url2, 0))

        ret_url1, ret_depth1 = self.crawler.get_next_url()
        self.assertEqual(ret_url1, normalized_url1)
        self.assertEqual(ret_depth1, 0)
        self.assertEqual(self.crawler.get_visited_count(), 1)

        ret_url2, ret_depth2 = self.crawler.get_next_url()
        self.assertEqual(ret_url2, normalized_url2)
        self.assertEqual(ret_depth2, 0)
        self.assertEqual(self.crawler.get_visited_count(), 2)

        ret_url_none, ret_depth_none = self.crawler.get_next_url()
        self.assertIsNone(ret_url_none)
        self.assertIsNone(ret_depth_none)


    def test_add_url_duplicates_and_visited(self):
        url1 = "https://example.com/page1"
        normalized_url1 = self.crawler._normalize_url(url1)

        self.crawler.add_url(url1, depth=0)
        self.assertEqual(self.crawler.get_queue_size(), 1)
        self.crawler.add_url(url1, depth=0) # duplicate
        self.assertEqual(self.crawler.get_queue_size(), 1)
        self.crawler.add_url("https://Example.com/page1#frag", depth=0) # duplicate via normalization
        self.assertEqual(self.crawler.get_queue_size(), 1)

        # Mark as visited *before* get_next_url for this specific test logic
        self.crawler.mark_as_visited(url1)
        self.assertEqual(self.crawler.get_visited_count(), 1)

        # Try adding a URL that is already in _queue_set (but also marked visited now)
        # Since it's in visited_urls, it shouldn't be added.
        # And if it was only in _queue_set, it also wouldn't be added.
        self.crawler.add_url(url1, depth=0)
        self.assertEqual(self.crawler.get_queue_size(), 1) # Still the original one in queue

        retrieved_url, retrieved_depth = self.crawler.get_next_url()
        self.assertEqual(retrieved_url, normalized_url1)
        self.assertEqual(retrieved_depth, 0)
        self.assertEqual(self.crawler.get_queue_size(), 0)
        # get_next_url also calls mark_as_visited, so count remains 1
        self.assertIn(normalized_url1, self.crawler.visited_urls)
        self.assertEqual(self.crawler.get_visited_count(), 1)


        self.crawler.add_url(url1, depth=0) # Should not be added as it's in visited_urls
        self.assertEqual(self.crawler.get_queue_size(), 0)


    def test_add_invalid_urls(self):
        self.crawler.add_url(None, depth=0) # type: ignore
        self.crawler.add_url("", depth=0)
        self.crawler.add_url("  ", depth=0)
        self.crawler.add_url("ftp://invalid.com", depth=0)
        self.assertEqual(self.crawler.get_queue_size(), 0)

    def test_add_urls_list(self):
        # add_urls now needs current_depth
        urls = [
            "https://example.com/p1", "https://example.com/p2",
            "https://example.com/p1", "ftp://bad.com", "https://example.com/P2#frag"
        ]
        self.crawler.add_urls(urls, current_depth=0) # Adds with depth 1
        self.assertEqual(self.crawler.get_queue_size(), 3)

        # Check actual items in queue
        queue_items = [item[0] for item in list(self.crawler.to_visit_queue)]
        self.assertIn(self.crawler._normalize_url("https://example.com/p1"), queue_items)
        self.assertIn(self.crawler._normalize_url("https://example.com/p2"), queue_items)
        self.assertIn(self.crawler._normalize_url("https://example.com/P2"), queue_items)
        for _, depth in self.crawler.to_visit_queue:
            self.assertEqual(depth, 1)


    def test_mark_as_visited(self):
        url = "https://example.com/path"
        normalized_url = "https://example.com/path"
        self.crawler.mark_as_visited(url)
        self.assertIn(normalized_url, self.crawler.visited_urls)
        self.assertEqual(self.crawler.get_visited_count(), 1)
        self.crawler.mark_as_visited(url + "#frag") # mark again
        self.assertEqual(self.crawler.get_visited_count(), 1)


    def test_state_methods(self):
        self.assertFalse(self.crawler.has_next_url())
        self.crawler.add_url("https://example.com/one", depth=0)
        self.assertTrue(self.crawler.has_next_url())
        self.crawler.get_next_url()
        self.assertFalse(self.crawler.has_next_url())


    def test_can_crawl_url_domain_scoping(self):
        base = "https://docs.example.com/product/"
        # Re-initialize crawler for this specific base_url test
        crawler_scoped = Crawler(
            base_url=base,
            analyzer_func=self.mock_analyzer_func,
            parser_func=self.mock_parser_func,
            writer_func=self.mock_writer_func,
            analyzer_config=self.mock_analyzer_config
        )
        self.assertTrue(crawler_scoped.can_crawl_url("https://docs.example.com/product/page1"))
        self.assertFalse(crawler_scoped.can_crawl_url("https://api.example.com/data"))

        # Test with no base_url (should always be true for valid URLs)
        # self.crawler is already initialized without a base_url for its queue here
        self.assertTrue(self.crawler.can_crawl_url("https://any.valid.url.com/path"))
        self.assertFalse(self.crawler.can_crawl_url("ftp://invalid.scheme.com"))


    @patch('src.core.crawler.requests.get')
    def test_start_crawling_successful_run_one_page(self, mock_requests_get):
        test_url = "http://example.com/page1"
        mock_html_content = "<html><body>Test Content</body></html>"

        mock_response = MagicMock()
        mock_response.text = mock_html_content
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        mock_selectors = HtmlSelectors(content_selector="body", navigation_selector="nav", next_page_selector=None)
        self.mock_analyzer_func.return_value = mock_selectors

        mock_parsed_content_html = "<body>Test Content</body>"
        mock_extracted_links = ["http://example.com/link1", "http://example.com/link2"]
        self.mock_parser_func.return_value = (mock_parsed_content_html, mock_extracted_links)

        self.mock_writer_func.return_value = f"{self.default_output_dir}/example_com_page1.md"

        crawler_instance = Crawler(
            base_url=test_url,
            max_pages=1,
            analyzer_func=self.mock_analyzer_func,
            parser_func=self.mock_parser_func,
            writer_func=self.mock_writer_func,
            analyzer_config=self.mock_analyzer_config,
            output_dir=self.default_output_dir
        )
        crawler_instance.start_crawling()

        normalized_test_url = self.crawler._normalize_url(test_url)
        self.mock_analyzer_func.assert_called_once_with(normalized_test_url, self.mock_analyzer_config)
        mock_requests_get.assert_called_once_with(normalized_test_url, timeout=30)
        self.mock_parser_func.assert_called_once_with(
            mock_html_content,
            normalized_test_url,
            mock_selectors.content_selector,
            mock_selectors.navigation_selector,
            mock_selectors.next_page_selector
        )
        self.mock_writer_func.assert_called_once_with(
            normalized_test_url,
            mock_parsed_content_html,
            self.default_output_dir
        )
        self.assertEqual(crawler_instance.get_visited_count(), 1)
        self.assertIn(normalized_test_url, crawler_instance.visited_urls)

        # Check if new links were added to queue with correct depth
        self.assertEqual(crawler_instance.get_queue_size(), 2)

        expected_link1_norm = self.crawler._normalize_url("http://example.com/link1")
        expected_link2_norm = self.crawler._normalize_url("http://example.com/link2")

        found_link1 = False
        found_link2 = False
        for item_url, item_depth in crawler_instance.to_visit_queue:
            if item_url == expected_link1_norm and item_depth == 1:
                found_link1 = True
            if item_url == expected_link2_norm and item_depth == 1:
                found_link2 = True
        self.assertTrue(found_link1, "Link 1 not found in queue with correct depth")
        self.assertTrue(found_link2, "Link 2 not found in queue with correct depth")


    @patch('src.core.crawler.requests.get')
    def test_start_crawling_analyzer_error(self, mock_requests_get):
        test_url = "http://example.com/analyzer_fails"
        normalized_test_url = self.crawler._normalize_url(test_url)
        self.mock_analyzer_func.side_effect = LLMAnalysisError("LLM failed")

        crawler_instance = Crawler(
            base_url=test_url, max_pages=1,
            analyzer_func=self.mock_analyzer_func, parser_func=self.mock_parser_func,
            writer_func=self.mock_writer_func, analyzer_config=self.mock_analyzer_config
        )
        crawler_instance.start_crawling()

        self.mock_analyzer_func.assert_called_once_with(normalized_test_url, self.mock_analyzer_config)
        mock_requests_get.assert_not_called()
        self.mock_parser_func.assert_not_called()
        self.mock_writer_func.assert_not_called()
        self.assertEqual(crawler_instance.get_visited_count(), 1)
        self.assertEqual(crawler_instance.get_queue_size(), 0)


    @patch('src.core.crawler.requests.get')
    def test_start_crawling_requests_error_for_parser(self, mock_requests_get):
        test_url = "http://example.com/fetch_fails_for_parser"
        mock_selectors = HtmlSelectors(content_selector="body", navigation_selector="nav")
        self.mock_analyzer_func.return_value = mock_selectors

        mock_requests_get.side_effect = requests.exceptions.RequestException("Fetch for parser failed")

        crawler_instance = Crawler(
            base_url=test_url, max_pages=1,
            analyzer_func=self.mock_analyzer_func, parser_func=self.mock_parser_func,
            writer_func=self.mock_writer_func, analyzer_config=self.mock_analyzer_config
        )
        crawler_instance.start_crawling()

        self.mock_analyzer_func.assert_called_once()
        mock_requests_get.assert_called_once()
        self.mock_parser_func.assert_not_called()
        self.mock_writer_func.assert_not_called()
        self.assertEqual(crawler_instance.get_visited_count(), 1)
        self.assertEqual(crawler_instance.get_queue_size(), 0)


    @patch('src.core.crawler.requests.get')
    def test_start_crawling_parser_error(self, mock_requests_get):
        test_url = "http://example.com/parser_fails"
        mock_html_content = "<html></html>"
        mock_response = MagicMock(text=mock_html_content)
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        mock_selectors = HtmlSelectors(content_selector="body", navigation_selector="nav")
        self.mock_analyzer_func.return_value = mock_selectors
        self.mock_parser_func.side_effect = Exception("Parsing failed")

        crawler_instance = Crawler(
            base_url=test_url, max_pages=1,
            analyzer_func=self.mock_analyzer_func, parser_func=self.mock_parser_func,
            writer_func=self.mock_writer_func, analyzer_config=self.mock_analyzer_config
        )
        crawler_instance.start_crawling()

        self.mock_analyzer_func.assert_called_once()
        mock_requests_get.assert_called_once()
        self.mock_parser_func.assert_called_once()
        self.mock_writer_func.assert_not_called()
        self.assertEqual(crawler_instance.get_visited_count(), 1)

    @patch('src.core.crawler.requests.get')
    def test_start_crawling_writer_error(self, mock_requests_get):
        test_url = "http://example.com/writer_fails"
        mock_html_content = "<html><body>Content</body></html>"
        mock_response = MagicMock(text=mock_html_content)
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        mock_selectors = HtmlSelectors(content_selector="body", navigation_selector="nav")
        self.mock_analyzer_func.return_value = mock_selectors
        self.mock_parser_func.return_value = ("<body>Content</body>", ["http://example.com/newlink"])
        self.mock_writer_func.side_effect = Exception("Writer failed")

        crawler_instance = Crawler(
            base_url=test_url, max_pages=1,
            analyzer_func=self.mock_analyzer_func, parser_func=self.mock_parser_func,
            writer_func=self.mock_writer_func, analyzer_config=self.mock_analyzer_config
        )
        crawler_instance.start_crawling()

        self.mock_writer_func.assert_called_once()
        self.assertEqual(crawler_instance.get_visited_count(), 1)
        self.assertEqual(crawler_instance.get_queue_size(), 1) # New link should still be added
        self.assertIn(self.crawler._normalize_url("http://example.com/newlink"), crawler_instance._queue_set)

    def test_max_pages_limit(self):
        # This test will need multiple "successful" page processings mocked
        # to ensure it stops at max_pages.
        # For simplicity, we'll mock that each page processing adds one new link.

        # Setup mocks to always succeed and return one new link
        self.mock_analyzer_func.return_value = HtmlSelectors(content_selector="body", navigation_selector="nav")

        # Mock requests.get globally for this test
        mock_get_patcher = patch('src.core.crawler.requests.get')
        mock_requests_get = mock_get_patcher.start()
        self.addCleanup(mock_get_patcher.stop) # Ensure patch is stopped after test

        mock_response = MagicMock(text="<html></html>")
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        # Each call to parser_func will return a new unique link to keep crawl going
        link_counter = 0
        def side_effect_parser(*args, **kwargs):
            nonlocal link_counter
            link_counter += 1
            return ("content", [f"http://example.com/gen_link_{link_counter}"])
        self.mock_parser_func.side_effect = side_effect_parser
        self.mock_writer_func.return_value = "path/to/file.md"

        crawler_instance = Crawler(
            base_url="http://example.com/start", max_pages=3,
            analyzer_func=self.mock_analyzer_func, parser_func=self.mock_parser_func,
            writer_func=self.mock_writer_func, analyzer_config=self.mock_analyzer_config
        )
        crawler_instance.start_crawling()

        self.assertEqual(self.mock_analyzer_func.call_count, 3)
        self.assertEqual(mock_requests_get.call_count, 3)
        self.assertEqual(self.mock_parser_func.call_count, 3)
        self.assertEqual(self.mock_writer_func.call_count, 3)
        self.assertEqual(crawler_instance.get_visited_count(), 3)
        # After 3 pages, the 3rd page processing adds one more link (gen_link_3)
        # So queue size should be 1, with (gen_link_3, depth=3)
        self.assertEqual(crawler_instance.get_queue_size(), 1)
        if crawler_instance.get_queue_size() == 1:
            queued_url, queued_depth = crawler_instance.to_visit_queue[0]
            self.assertEqual(queued_url, self.crawler._normalize_url("http://example.com/gen_link_3"))
            self.assertEqual(queued_depth, 3) # start (0), gen_link_1 (1), gen_link_2 (2) -> processed. gen_link_3 is depth 3.


    def test_max_depth_limit(self):
        # Mock setup
        self.mock_analyzer_func.return_value = HtmlSelectors(content_selector="body", navigation_selector="nav")
        mock_get_patcher = patch('src.core.crawler.requests.get')
        mock_requests_get = mock_get_patcher.start()
        self.addCleanup(mock_get_patcher.stop)
        mock_response = MagicMock(text="<html></html>")
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response
        self.mock_writer_func.return_value = "path/to/file.md"

        # Parser side effect to generate links based on depth
        # page_at_depth_0 -> link_at_depth_1
        # page_at_depth_1 -> link_at_depth_2
        # page_at_depth_2 -> link_at_depth_3 (this should not be added if max_depth is 1)
        def SUT_parser_side_effect(html, url, cs, ns, nps):
            # Determine current depth based on URL (simplified for test)
            # This is a bit of a hack for testing, real depth comes from queue
            depth_from_url = 0
            if "depth1" in url: depth_from_url = 1
            elif "depth2" in url: depth_from_url = 2

            return ("content", [f"http://example.com/next_link_from_{url.split('/')[-1]}_to_depth{depth_from_url + 1}"])

        self.mock_parser_func.side_effect = SUT_parser_side_effect

        # Test with max_depth = 0
        # Should only process base_url, no new links added to queue effectively for processing
        crawler_depth_0 = Crawler(
            base_url="http://example.com/start_depth0", max_depth=0,
            analyzer_func=self.mock_analyzer_func, parser_func=self.mock_parser_func,
            writer_func=self.mock_writer_func, analyzer_config=self.mock_analyzer_config
        )
        crawler_depth_0.start_crawling()
        self.assertEqual(self.mock_analyzer_func.call_count, 1) # Only base URL
        self.assertEqual(crawler_depth_0.get_visited_count(), 1)
        self.assertEqual(crawler_depth_0.get_queue_size(), 0) # Links from depth 0 would be depth 1, exceeding max_depth 0

        # Reset mocks for next test
        self.mock_analyzer_func.reset_mock()
        self.mock_parser_func.reset_mock() # Reset side_effect too if needed, or re-assign
        self.mock_writer_func.reset_mock()
        mock_requests_get.reset_mock()
        self.mock_parser_func.side_effect = SUT_parser_side_effect # Re-assign side effect

        # Test with max_depth = 1
        # Should process base_url (depth 0) and its children (depth 1)
        # Links generated from depth 1 pages (which would be depth 2) should not be added for processing.
        crawler_depth_1 = Crawler(
            base_url="http://example.com/start_depth1", max_depth=1,
            analyzer_func=self.mock_analyzer_func, parser_func=self.mock_parser_func,
            writer_func=self.mock_writer_func, analyzer_config=self.mock_analyzer_config
        )
        # Mock parser to return a fixed link name for predictability
        # URL from depth 0: "http://example.com/start_depth1" -> parser adds "link_to_depth1"
        # URL from depth 1: "http://example.com/link_to_depth1" -> parser adds "link_to_depth2"

        links_from_depth_0_page = ["http://example.com/page_at_depth_1"]
        links_from_depth_1_page = ["http://example.com/page_at_depth_2"]

        def specific_parser_side_effect(html, url, cs, ns, nps):
            if "start_depth1" in url: # Depth 0 page
                return ("content_d0", links_from_depth_0_page)
            elif "page_at_depth_1" in url: # Depth 1 page
                return ("content_d1", links_from_depth_1_page)
            return ("default_content", [])

        self.mock_parser_func.side_effect = specific_parser_side_effect

        crawler_depth_1.start_crawling()

        # Expected calls:
        # 1. Analyze "start_depth1" (depth 0)
        # 2. Parse "start_depth1", adds "page_at_depth_1" (depth 1) to queue
        # 3. Analyze "page_at_depth_1" (depth 1)
        # 4. Parse "page_at_depth_1", attempts to add "page_at_depth_2" (depth 2) - should be blocked by max_depth=1
        self.assertEqual(self.mock_analyzer_func.call_count, 2) # start_depth1, page_at_depth_1
        self.assertEqual(mock_requests_get.call_count, 2)
        self.assertEqual(self.mock_parser_func.call_count, 2)
        self.assertEqual(crawler_depth_1.get_visited_count(), 2)
        self.assertEqual(crawler_depth_1.get_queue_size(), 0) # page_at_depth_2 (depth 2) should not be added

        # Verify that add_url was not called for page_at_depth_2 or similar
        # This requires checking calls to crawler_depth_1.add_url or inspecting the queue more deeply
        # For now, queue_size being 0 after processing 2 pages is a good indicator.


if __name__ == '__main__':
    unittest.main()
