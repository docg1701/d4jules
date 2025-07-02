import unittest
from d4jules.core.parser import parse_html_content

class TestParseHtmlContent(unittest.TestCase):

    def test_basic_extraction(self):
        html_doc = """
        <html><head><title>Test Page</title></head>
        <body>
            <article id="main">
                <h1>Main Content</h1><p>Some text.</p>
                <a href="related.html">Related</a>
            </article>
            <nav id="navigation">
                <a href="/page1">Page 1</a>
                <a href="http://example.com/page2">Page 2</a>
                <a href="../page3">Page 3</a>
            </nav>
            <div class="pagination">
                <a href="?page=2" class="next">Next Page</a>
            </div>
        </body></html>
        """
        base_url = "http://example.com/current/"
        content_selector = "#main"
        nav_selector = "#navigation"
        next_page_selector = ".pagination a.next"

        content_html, urls = parse_html_content(
            html_doc, base_url, content_selector, nav_selector, next_page_selector
        )

        expected_content_html = '<article id="main">\n<h1>Main Content</h1><p>Some text.</p>\n<a href="related.html">Related</a>\n</article>'
        # Normalize expected HTML by parsing and regenerating to account for minor parser differences
        from bs4 import BeautifulSoup
        expected_content_html = str(BeautifulSoup(expected_content_html, 'html.parser').find(id="main"))


        self.assertEqual(str(BeautifulSoup(content_html, 'html.parser').find(id="main")), expected_content_html)

        expected_urls = sorted([
            "http://example.com/page1",
            "http://example.com/page2",
            "http://example.com/page3", # ../page3 relative to /current/
            "http://example.com/current/?page=2"
        ])
        self.assertEqual(urls, expected_urls)

    def test_no_content_found(self):
        html_doc = "<body><p>No article here.</p></body>"
        base_url = "http://example.com/"
        content_selector = "#nonexistent"
        nav_selector = None
        next_page_selector = None

        content_html, urls = parse_html_content(
            html_doc, base_url, content_selector, nav_selector, next_page_selector
        )
        self.assertIsNone(content_html)
        self.assertEqual(urls, [])

    def test_no_nav_links(self):
        html_doc = '<article id="main"><p>Content</p></article><nav id="empty_nav"></nav>'
        base_url = "http://example.com/"
        content_selector = "#main"
        nav_selector = "#empty_nav" # Selector exists but no links inside
        next_page_selector = None

        content_html, urls = parse_html_content(
            html_doc, base_url, content_selector, nav_selector, next_page_selector
        )
        self.assertIsNotNone(content_html)
        self.assertEqual(urls, [])

    def test_nav_selector_none(self):
        html_doc = '<article id="main"><p>Content</p></article><a href="/next" class="next-link">Next</a>'
        base_url = "http://example.com/"
        content_selector = "#main"
        nav_selector = None # No nav selector provided
        next_page_selector = ".next-link"

        content_html, urls = parse_html_content(
            html_doc, base_url, content_selector, nav_selector, next_page_selector
        )
        self.assertIsNotNone(content_html)
        self.assertEqual(urls, ["http://example.com/next"])

    def test_nav_selector_finds_no_elements(self):
        html_doc = '<article id="main"><p>Content</p></article>'
        base_url = "http://example.com/"
        content_selector = "#main"
        nav_selector = "#non_existent_nav" # Nav selector finds nothing
        next_page_selector = None

        content_html, urls = parse_html_content(
            html_doc, base_url, content_selector, nav_selector, next_page_selector
        )
        self.assertIsNotNone(content_html)
        self.assertEqual(urls, [])

    def test_no_next_page_link(self):
        html_doc = '<article id="main"><p>Content</p></article><nav id="nav"><a href="/p1">1</a></nav>'
        base_url = "http://example.com/"
        content_selector = "#main"
        nav_selector = "#nav"
        next_page_selector = ".no-such-next-link" # Selector finds nothing

        content_html, urls = parse_html_content(
            html_doc, base_url, content_selector, nav_selector, next_page_selector
        )
        self.assertIsNotNone(content_html)
        self.assertEqual(urls, ["http://example.com/p1"])

    def test_next_page_selector_none(self):
        html_doc = '<article id="main"><p>Content</p></article><nav id="nav"><a href="/p1">1</a></nav>'
        base_url = "http://example.com/"
        content_selector = "#main"
        nav_selector = "#nav"
        next_page_selector = None # No next page selector provided

        content_html, urls = parse_html_content(
            html_doc, base_url, content_selector, nav_selector, next_page_selector
        )
        self.assertIsNotNone(content_html)
        self.assertEqual(urls, ["http://example.com/p1"])

    def test_url_normalization_various_bases(self):
        html_doc = """
        <article id="content">Test</article>
        <nav>
            <a href="link1.html">Link 1</a>
            <a href="/abs/link2.html">Link 2</a>
            <a href="../up/link3.html">Link 3</a>
            <a href="http://other.com/link4.html">Link 4</a>
        </nav>
        <a href="next.html" class="next">Next</a>
        """
        base_url1 = "http://example.com/foo/bar/"
        content_html1, urls1 = parse_html_content(html_doc, base_url1, "#content", "nav", ".next")
        expected_urls1 = sorted([
            "http://example.com/foo/bar/link1.html",
            "http://example.com/abs/link2.html",
            "http://example.com/foo/up/link3.html",
            "http://other.com/link4.html",
            "http://example.com/foo/bar/next.html"
        ])
        self.assertEqual(urls1, expected_urls1)

        base_url2 = "http://example.com/foo/bar" # No trailing slash
        content_html2, urls2 = parse_html_content(html_doc, base_url2, "#content", "nav", ".next")
        expected_urls2 = sorted([
            "http://example.com/foo/link1.html", # Relative to /foo/
            "http://example.com/abs/link2.html",
            "http://example.com/up/link3.html", # Relative to /
            "http://other.com/link4.html",
            "http://example.com/foo/next.html"
        ])
        self.assertEqual(urls2, expected_urls2)

    def test_next_page_selector_is_the_link_itself(self):
        html_doc = """
        <article id="main">Content</article>
        <a href="next_page.html" class="next-button">Next</a>
        """
        base_url = "http://example.com/test/"
        content_selector = "#main"
        nav_selector = None
        next_page_selector = "a.next-button" # Selector is the link itself

        content_html, urls = parse_html_content(
            html_doc, base_url, content_selector, nav_selector, next_page_selector
        )
        self.assertEqual(urls, ["http://example.com/test/next_page.html"])

    def test_next_page_selector_points_to_container(self):
        html_doc = """
        <article id="main">Content</article>
        <div class="pagination">
            <a href="next_page_in_div.html" class="actual-link">Next</a>
        </div>
        """
        base_url = "http://example.com/test/"
        content_selector = "#main"
        nav_selector = None
        next_page_selector = "div.pagination" # Selector is container, link is inside

        content_html, urls = parse_html_content(
            html_doc, base_url, content_selector, nav_selector, next_page_selector
        )
        self.assertEqual(urls, ["http://example.com/test/next_page_in_div.html"])

    def test_duplicate_urls_are_handled(self):
        html_doc = """
        <html><body>
            <article id="main">Content</article>
            <nav id="navigation">
                <a href="page1.html">Page 1</a>
                <a href="page1.html">Page 1 Duplicate</a>
            </nav>
            <a href="page1.html" class="next">Next also Page 1</a>
        </body></html>
        """
        base_url = "http://example.com/"
        content_selector = "#main"
        nav_selector = "#navigation"
        next_page_selector = ".next"

        _, urls = parse_html_content(
            html_doc, base_url, content_selector, nav_selector, next_page_selector
        )
        self.assertEqual(urls, ["http://example.com/page1.html"]) # Only one instance

if __name__ == '__main__':
    unittest.main()
