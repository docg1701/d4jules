import unittest
import tempfile
from pathlib import Path
import shutil # For cleaning up test directories

from d4jules.core.writer import _generate_filename_from_url, save_content_as_markdown

class TestGenerateFilenameFromUrl(unittest.TestCase):
    def test_simple_url(self):
        self.assertEqual(_generate_filename_from_url("http://example.com"), "example_com.md")
        self.assertEqual(_generate_filename_from_url("https://example.com/"), "example_com.md")

    def test_url_with_path(self):
        self.assertEqual(_generate_filename_from_url("http://example.com/foo/bar"), "example_com_foo_bar.md")
        self.assertEqual(_generate_filename_from_url("http://example.com/foo/bar.html"), "example_com_foo_bar.html.md")

    def test_url_with_query_and_fragment(self):
        self.assertEqual(_generate_filename_from_url("http://example.com/page?q=1#section"), "example_com_page.md")

    def test_url_with_special_chars(self):
        # Query parameters are expected to be ignored by current implementation
        self.assertEqual(_generate_filename_from_url("http://example.com/a*b?c=d/e"), "example_com_a_b.md")
        self.assertEqual(_generate_filename_from_url("http://test-site.com/path_with_numbers123"), "test-site_com_path_with_numbers123.md")

    def test_url_already_ends_with_md(self):
        # If path part already ends with .md, an additional .md should not be appended.
        self.assertEqual(_generate_filename_from_url("http://example.com/notes.md"), "example_com_notes.md")

    def test_empty_path(self):
        self.assertEqual(_generate_filename_from_url("http://example.com//"), "example_com.md")

    def test_root_url(self):
        self.assertEqual(_generate_filename_from_url("http://example.com"), "example_com.md")
        self.assertEqual(_generate_filename_from_url("http://localhost:8000"), "localhost_8000.md")

    def test_long_url_truncation(self):
        long_path = "a" * 120
        url = f"http://example.com/{long_path}"
        filename = _generate_filename_from_url(url)
        # Expected: example_com_ + 'a'* (100 - len("example_com_") - len(".md") - 1 for potential underscore if needed) + .md
        # This is an approximation, the actual length depends on the exact MAX_FILENAME_LENGTH and cleaning.
        # For MAX_FILENAME_LENGTH = 100
        # "example_com_" is 12 chars. ".md" is 3 chars. Total 15.
        # Remaining for name_part: 100 - 3 = 97.
        # So, "example_com_" + "a"*(97-12) = "example_com_" + "a"*85
        # Max length is 100
        self.assertTrue(len(filename) <= 100, f"Filename {filename} is too long.")
        self.assertTrue(filename.startswith("example_com_aaaaaaaaaa"), "Filename doesn't start as expected after truncation.")
        self.assertTrue(filename.endswith(".md"), "Filename doesn't end with .md after truncation.")

    def test_filename_becomes_empty_after_cleaning(self):
        self.assertEqual(_generate_filename_from_url("http://////"), "index.md")
        self.assertEqual(_generate_filename_from_url("http://..."), "index.md") # all dots become underscores, then stripped

class TestSaveContentAsMarkdown(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test outputs
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        # Remove the temporary directory after tests
        shutil.rmtree(self.test_dir)

    def test_save_basic_content(self):
        page_url = "http://example.com/testpage"
        html_content = "<h1>Hello</h1><p>This is <b>bold</b> text.</p>"

        expected_filename = "example_com_testpage.md"
        expected_markdown_content = "# Hello\n\nThis is **bold** text.\n\n" # Approximate, depends on html2text config

        file_path_str = save_content_as_markdown(page_url, html_content, output_dir=str(self.test_dir))
        self.assertIsNotNone(file_path_str)

        file_path = Path(file_path_str)
        self.assertEqual(file_path.name, expected_filename)
        self.assertTrue(file_path.exists())

        with open(file_path, 'r', encoding='utf-8') as f:
            saved_content = f.read()

        # We check for key elements because exact markdown can vary slightly with html2text versions/configs
        self.assertIn("# Hello", saved_content)
        self.assertIn("This is **bold** text.", saved_content)

    def test_save_no_html_content(self):
        page_url = "http://example.com/empty"
        file_path_str = save_content_as_markdown(page_url, None, output_dir=str(self.test_dir))
        self.assertIsNone(file_path_str)
        # Check that no file was created
        self.assertEqual(len(list(self.test_dir.iterdir())), 0)

    def test_output_directory_creation(self):
        page_url = "http://example.com/another/page"
        html_content = "<p>Test</p>"
        nested_output_dir = self.test_dir / "nested" / "output"

        # Ensure nested_output_dir does not exist initially
        self.assertFalse(nested_output_dir.exists())

        file_path_str = save_content_as_markdown(page_url, html_content, output_dir=str(nested_output_dir))
        self.assertIsNotNone(file_path_str)

        file_path = Path(file_path_str)
        self.assertTrue(nested_output_dir.exists())
        self.assertTrue(file_path.exists())
        self.assertEqual(file_path.name, "example_com_another_page.md")

    def test_filename_generation_integration(self):
        page_url = "https://sub.example.co.uk/path/to/document.html?query=param#fragment"
        html_content = "<h2>Test Title</h2>"
        expected_filename = "sub_example_co_uk_path_to_document.html.md"

        file_path_str = save_content_as_markdown(page_url, html_content, output_dir=str(self.test_dir))
        self.assertIsNotNone(file_path_str)
        file_path = Path(file_path_str)
        self.assertEqual(file_path.name, expected_filename)

    # Mocking html2text.HTML2Text().handle for error testing can be complex.
    # For now, we rely on its robustness. Testing file I/O errors would also require mocking open().
    # The current implementation prints errors but doesn't raise them in a way easily testable without mocks.

if __name__ == '__main__':
    unittest.main()
