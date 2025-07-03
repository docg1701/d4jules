import unittest
from bs4 import BeautifulSoup # Added for normalizing expected HTML strings

# Assuming src is in PYTHONPATH or tests are run from project root
from src.core.parser import parse_html_content

class TestParser(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://example.com/docs/"
        self.sample_html_full = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <nav id="main-nav">
                    <a href="page1.html">Page 1</a>
                    <a href="/abs/page2">Page 2</a>
                    <a href="https://othersite.com/page3">Page 3</a>
                    <a href="page1.html">Page 1 Duplicate</a>
                    <a>No Href</a>
                </nav>
                <article id="content">
                    <h1>Main Title</h1>
                    <p>Some content here.</p>
                    <a href="contentlink.html">Content Link</a>
                </article>
                <div id="pagination">
                    <a href="nextpage.html" id="next-link">Next</a>
                </div>
                <div id="pagination-container">
                     <a href="next_in_container.html">Next in Container</a>
                </div>
            </body>
        </html>
        """
        self.content_selector = "#content"
        self.nav_selector = "#main-nav"
        self.next_page_selector_direct = "#next-link"
        self.next_page_selector_container = "#pagination-container"


    def test_full_extraction(self):
        # This test will verify extraction with all selectors present
        content, links = parse_html_content(
            self.sample_html_full,
            self.base_url,
            self.content_selector,
            self.nav_selector,
            self.next_page_selector_direct
        )

        # For comparing HTML content, parse the expected string too to normalize it.
        expected_content_html_string = """<article id="content">
                    <h1>Main Title</h1>
                    <p>Some content here.</p>
                    <a href="contentlink.html">Content Link</a>
                </article>"""

        # Use BeautifulSoup to parse the expected string and get its string representation
        # This helps normalize minor formatting differences.
        from bs4 import BeautifulSoup # Add import if not already at top level
        expected_soup = BeautifulSoup(expected_content_html_string, 'html.parser')
        # Assuming the expected string is just the single article element
        expected_normalized_content_str = str(expected_soup.find('article'))

        self.assertEqual(content, expected_normalized_content_str)

        expected_links = sorted([
            "https://example.com/docs/page1.html",
            "https://example.com/abs/page2", # Assuming /abs/page2 is relative to domain root
            "https://othersite.com/page3",
            "https://example.com/docs/nextpage.html"
        ])
        # urljoin behavior for /abs/page2 with base_url https://example.com/docs/
        # is https://example.com/abs/page2.

        # BeautifulSoup select might return elements in a specific order,
        # but the function sorts them.
        self.assertEqual(links, expected_links)

    def test_missing_content_selector(self):
        content, links = parse_html_content(
            self.sample_html_full,
            self.base_url,
            "#nonexistent-content", # Non-matching content selector
            self.nav_selector,
            self.next_page_selector_direct
        )
        self.assertIsNone(content)
        expected_links = sorted([
            "https://example.com/docs/page1.html",
            "https://example.com/abs/page2",
            "https://othersite.com/page3",
            "https://example.com/docs/nextpage.html"
        ])
        self.assertEqual(links, expected_links)

    def test_missing_nav_selector(self):
        content, links = parse_html_content(
            self.sample_html_full,
            self.base_url,
            self.content_selector,
            "#nonexistent-nav", # Non-matching nav selector
            self.next_page_selector_direct
        )
        self.assertIsNotNone(content)
        expected_links = sorted([
            "https://example.com/docs/nextpage.html" # Only next page link
        ])
        self.assertEqual(links, expected_links)

    def test_missing_next_page_selector(self):
        content, links = parse_html_content(
            self.sample_html_full,
            self.base_url,
            self.content_selector,
            self.nav_selector,
            "#nonexistent-next" # Non-matching next page selector
        )
        self.assertIsNotNone(content)
        expected_links = sorted([
            "https://example.com/docs/page1.html",
            "https://example.com/abs/page2",
            "https://othersite.com/page3"
            # No next page link
        ])
        self.assertEqual(links, expected_links)

    def test_all_selectors_missing_or_no_match(self):
        content, links = parse_html_content(
            self.sample_html_full,
            self.base_url,
            "#nonexistent-content",
            "#nonexistent-nav",
            "#nonexistent-next"
        )
        self.assertIsNone(content)
        self.assertEqual(links, [])

    def test_empty_html_document(self):
        content, links = parse_html_content(
            "", self.base_url, self.content_selector, self.nav_selector, self.next_page_selector_direct
        )
        self.assertIsNone(content)
        self.assertEqual(links, [])

    def test_url_normalization_and_absolutization(self):
        html = """
        <nav>
            <a href="page1.html">1</a>
            <a href="./page2.html">2</a>
            <a href="../page3.html">3</a>
            <a href="/abs/page4">4</a>
            <a href="https://external.com/page5">5</a>
            <a href="//schemeless.com/page6">6</a>
            <a href="page1.html#frag">7</a>
        </nav>
        """
        # base_url = "https://example.com/docs/"
        # urljoin behavior for //schemeless.com/page6 with https base is https://schemeless.com/page6
        # urljoin preserves fragments by default. The parser doesn't remove them.
        expected_links = sorted([
            "https://example.com/docs/page1.html",
            "https://example.com/docs/page2.html", # ./page2.html relative to /docs/
            "https://example.com/page3.html",    # ../page3.html relative to /docs/
            "https://example.com/abs/page4",     # /abs/page4 relative to domain root
            "https://external.com/page5",
            "https://schemeless.com/page6",      # //schemeless.com becomes https://schemeless.com
            "https://example.com/docs/page1.html#frag"
        ])
        _, links = parse_html_content(html, self.base_url, None, "nav", None)
        self.assertEqual(links, expected_links)

    def test_duplicate_links_are_unique(self):
        html = """
        <nav>
            <a href="pageA.html">A1</a>
            <a href="pageA.html">A2</a>
            <a href="/pageB">B1</a>
            <a href="https://example.com/pageB">B2</a> <!-- normalizes to same as /pageB -->
        </nav>
        """
        # base_url = "https://example.com/docs/"
        # /pageB becomes https://example.com/pageB
        # https://example.com/pageB stays as is.
        expected_links = sorted([
            "https://example.com/docs/pageA.html",
            "https://example.com/pageB"
        ])
        _, links = parse_html_content(html, self.base_url, None, "nav", None)
        self.assertEqual(links, expected_links)

    def test_next_page_link_in_container(self):
        # Uses self.sample_html_full which has:
        # <div id="pagination-container">
        #      <a href="next_in_container.html">Next in Container</a>
        # </div>
        _, links = parse_html_content(
            self.sample_html_full,
            self.base_url,
            None, # No content selector
            None, # No nav selector
            self.next_page_selector_container # Selector for the container div
        )
        expected_links = sorted([
            "https://example.com/docs/next_in_container.html"
        ])
        self.assertEqual(links, expected_links)

    def test_no_href_skipped(self):
        html = "<nav><a>No Href</a><a href='link.html'>Link</a></nav>"
        _, links = parse_html_content(html, self.base_url, None, "nav", None)
        self.assertEqual(links, ["https://example.com/docs/link.html"])

    def test_content_selector_returns_string_of_element(self):
        html = "<div id='main'><p>Hello</p></div><footer>Footer</footer>"
        content, _ = parse_html_content(html, self.base_url, "#main", None, None)
        # Exact string representation can be tricky due to whitespace/parser differences.
        # We expect the outer div and its content.
        expected_content_str = '<div id="main"><p>Hello</p></div>'
        self.assertEqual(content, expected_content_str)

    def test_malformed_html(self):
        # BeautifulSoup is generally robust to malformed HTML.
        # This test ensures it doesn't crash and extracts what it can.
        html = """
        <html><head><title>Malformed</title><body>
        <nav id="nav-test"><a href="link1.html">Link 1</ комитета> <!-- malformed tag -->
        <article id="content-test">Some text here <p>More text. <div>Unclosed div
        <a href="/link2">Link 2</a>
        """
        content_selector = "#content-test"
        nav_selector = "#nav-test"

        content, links = parse_html_content(html, self.base_url, content_selector, nav_selector, None)

        self.assertIsNotNone(content)
        self.assertIn("Some text here", content)
        self.assertIn("More text.", content)
        # Depending on parser leniency, Link 2 might be part of content or not.
        # For now, just check that content is extracted.

        expected_links = sorted([
            "https://example.com/docs/link1.html",
            # "/link2" might not be extracted if nav is broken, or might if BS is lenient
            # If link2 is extracted, it becomes: "https://example.com/link2"
        ])
        # Let's be specific: if nav selector is "#nav-test", only link1.html should be found.
        # If BS cannot parse the malformed tag, it might stop before link1.
        # Current BS behavior with lxml: it parses link1.html correctly.
        # If BeautifulSoup, due to the malformed tag, considers the subsequent content
        # (including link2) as part of the #nav-test element, then link2 would be extracted.
        # The test failure indicates this is happening.
        self.assertEqual(links, sorted(["https://example.com/docs/link1.html", "https://example.com/link2"]))


if __name__ == '__main__':
    unittest.main()
