import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import html2text # For mocking its instance

# Assuming src is in PYTHONPATH or tests are run from project root
from src.core.writer import _generate_filename_from_url, save_content_as_markdown

class TestWriter(unittest.TestCase):

    def test_generate_filename_from_url_basic(self):
        url = "http://example.com/foo/bar.html"
        # Expected: example_com_foo_bar_html.md (current logic)
        # Original D12 might have suggested example_com_foo_bar.html.md
        # Current logic for "http://example.com/foo/bar.html":
        # netloc: example.com -> example_com
        # path_parts: ['foo', 'bar.html'] -> example_com_foo_bar.html
        # re.sub against [^\w._-]+ : no change
        # strip('_'): no change
        # endswith('.md'): no -> example_com_foo_bar.html.md (This is if '.' is allowed by \w)
        # If \w does not include '.', then 'bar.html' becomes 'bar_html'.
        # Let's check re.sub(r'[^\w._-]+', '_', filename)
        # \w includes letters, numbers, and underscore. It does NOT include dot.
        # The regex [^\w._-] means a dot . is NOT replaced.
        # So, "bar.html" path part remains "bar.html".
        # filename becomes "example_com_foo_bar.html"
        # re.sub does not change it.
        # .md is added if not present -> "example_com_foo_bar.html.md"
        self.assertEqual(_generate_filename_from_url(url), "example_com_foo_bar.html.md")

    def test_generate_filename_from_url_query_fragment(self):
        url = "https://sub.example.co.uk/path/to/doc.php?query=1&v=2#section-one"
        # netloc: sub_example_co_uk
        # path: path_to_doc.php
        # Expected based on dot not being replaced by re.sub: sub_example_co_uk_path_to_doc.php.md
        self.assertEqual(_generate_filename_from_url(url), "sub_example_co_uk_path_to_doc.php.md")

    def test_generate_filename_from_url_special_chars(self):
        url = "http://ex.com/a b/c!d@e.txt"
        # netloc: ex_com
        # path: a b_c!d@e.txt
        # re.sub: ex_com_a_b_c_d_e.txt (space, !, @ replaced by _)
        # Expected based on dot not being replaced: ex_com_a_b_c_d_e.txt.md
        self.assertEqual(_generate_filename_from_url(url), "ex_com_a_b_c_d_e.txt.md")

    def test_generate_filename_from_url_trailing_slash(self):
        url = "http://example.com/foo/bar/"
        # netloc: example_com
        # path: /foo/bar/ -> path_parts: ['foo', 'bar'] -> foo_bar
        # Expected: example_com_foo_bar.md
        self.assertEqual(_generate_filename_from_url(url), "example_com_foo_bar.md")

    def test_generate_filename_from_url_root(self):
        url = "http://example.com/"
        # netloc: example_com
        # path: / -> path_parts: []
        # Expected: example_com.md
        self.assertEqual(_generate_filename_from_url(url), "example_com.md")

    def test_generate_filename_from_url_root_no_slash(self):
        url = "http://example.com"
        # netloc: example_com
        # path: "" -> path_parts: []
        # Expected: example_com.md
        self.assertEqual(_generate_filename_from_url(url), "example_com.md")

    def test_generate_filename_from_url_empty_path_after_domain(self):
        url = "http://example.com?" # query after domain, no path
        self.assertEqual(_generate_filename_from_url(url), "example_com.md")
        url = "http://example.com#" # fragment after domain, no path
        self.assertEqual(_generate_filename_from_url(url), "example_com.md")


    def test_generate_filename_from_url_only_domain_special_chars(self):
        url = "http://my-site.example_domain.com/"
        # my-site.example_domain.com -> my-site_example_domain_com
        # Hyphen is allowed by \w._-
        self.assertEqual(_generate_filename_from_url(url), "my-site_example_domain_com.md")

    def test_generate_filename_from_url_resulting_empty_or_underscore(self):
        # Pathological cases that might result in empty or "_" before "index" fallback
        url1 = "http://_/_" # netloc: _, path: /_
                            # filename: __ -> re.sub keeps it -> strip '_' -> "" -> "index.md"
        self.assertEqual(_generate_filename_from_url(url1), "index.md")
        url2 = "http://.../" # netloc: ... -> ___
                             # filename: ___ -> re.sub keeps it -> strip '_' -> "" -> "index.md"
        self.assertEqual(_generate_filename_from_url(url2), "index.md")
        url3 = "http://_/"
        self.assertEqual(_generate_filename_from_url(url3), "index.md") # netloc: _, path_parts: [] -> filename: _ -> index.md
        url4 = "http:///" # Handled by urlparse, netloc becomes empty, path "/"
                          # This case might depend on how urlparse handles "http:///"
                          # urlparse("http:///") gives ParseResult(scheme='http', netloc='', path='/', ...)
                          # _generate_filename_from_url currently expects netloc.
                          # If netloc is empty, it might behave unexpectedly.
                          # The code has `filename = parsed_url.netloc.replace('.', '_')`
                          # If netloc is "", filename is "". Then `if not filename: filename="index"`
        self.assertEqual(_generate_filename_from_url(url4), "index.md")


    def test_generate_filename_from_url_long_name_truncation(self):
        base = "http://example.com/"
        long_path_part = "a" * 150
        url = base + long_path_part
        # Expected filename: example_com_aaaaaaaa...(100-3=97 chars for name)_aaa.md
        # MAX_FILENAME_LENGTH = 100
        # ext_part = ".md" (len 3)
        # name_part = name_part[:100 - 3 -1] -> name_part[:96]
        # filename = "example_com_" (12 chars) + long_path_part (150 chars)
        # full_name_before_trunc = "example_com_" + long_path_part -> len 162
        # stem = "example_com_" + long_path_part
        # stem_truncated = stem[:96]
        # expected_filename = stem_truncated + ".md"

        generated_name = _generate_filename_from_url(url)
        self.assertTrue(len(generated_name) <= 100)
        self.assertTrue(generated_name.startswith("example_com_"))
        self.assertTrue(generated_name.endswith(".md"))
        # Check actual stem length
        stem_len = len(Path(generated_name).stem)
        self.assertEqual(stem_len, 100 - 3) # 97 for the stem part that is truncated

    def test_generate_filename_from_url_already_md(self):
        url = "http://example.com/mydoc.md"
        # netloc: example_com
        # path: /mydoc.md -> path_parts: ['mydoc.md'] -> mydoc.md
        # re.sub does not change it. Ends with .md is true.
        # Expected: example_com_mydoc.md
        self.assertEqual(_generate_filename_from_url(url), "example_com_mydoc.md")

    def test_generate_filename_from_url_leading_trailing_underscores_in_parts(self):
        url = "http://_example_.com/_foo_/_bar_html"
        # netloc: _example_.com -> _example__com
        # path: /_foo_/_bar_html -> _foo__, _bar_html
        # joined: _foo___bar_html
        # filename: _example__com__foo___bar_html
        # re.sub: no change
        # strip('_'): example__com__foo___bar_html
        # Expected: example__com__foo___bar_html.md
        self.assertEqual(_generate_filename_from_url(url), "example__com__foo___bar_html.md")


    @patch('src.core.writer.Path.mkdir')
    @patch('src.core.writer.open', new_callable=mock_open)
    @patch('src.core.writer._generate_filename_from_url')
    @patch('html2text.HTML2Text') # Patch the class
    def test_save_content_as_markdown_success(self, MockHTML2Text, mock_gen_filename, mock_file_open, mock_mkdir):
        # Setup mocks
        mock_h_instance = MockHTML2Text.return_value
        mock_h_instance.handle.return_value = "## Markdown Content"
        mock_gen_filename.return_value = "test_file.md"

        page_url = "http://example.com/test"
        html_content = "<h1>Hello</h1>"
        output_dir = "test_output"

        expected_filepath = str(Path(output_dir) / "test_file.md")

        result_filepath = save_content_as_markdown(page_url, html_content, output_dir)

        MockHTML2Text.assert_called_once() # Check if HTML2Text was instantiated
        mock_h_instance.handle.assert_called_once_with(html_content)
        mock_gen_filename.assert_called_once_with(page_url)
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_file_open.assert_called_once_with(Path(output_dir) / "test_file.md", 'w', encoding='utf-8')
        mock_file_open().write.assert_called_once_with("## Markdown Content")
        self.assertEqual(result_filepath, expected_filepath)

    def test_save_content_as_markdown_html_content_none(self):
        result_filepath = save_content_as_markdown("http://example.com/any", None, "test_output")
        self.assertIsNone(result_filepath)

    @patch('src.core.writer.Path.mkdir')
    @patch('src.core.writer.open', new_callable=mock_open)
    @patch('src.core.writer._generate_filename_from_url')
    @patch('html2text.HTML2Text')
    def test_save_content_as_markdown_html2text_error(self, MockHTML2Text, mock_gen_filename, mock_file_open, mock_mkdir):
        mock_h_instance = MockHTML2Text.return_value
        mock_h_instance.handle.side_effect = Exception("HTML2Text conversion error")
        mock_gen_filename.return_value = "error_file.md"

        result_filepath = save_content_as_markdown("http://example.com/error", "<h1>Fail</h1>", "test_output")

        self.assertIsNone(result_filepath)
        # If h.handle fails, code returns before mkdir or file_open are called.
        mock_mkdir.assert_not_called()
        mock_file_open.assert_not_called()

    @patch('src.core.writer.Path.mkdir', side_effect=IOError("mkdir failed"))
    @patch('src.core.writer.open', new_callable=mock_open)
    @patch('src.core.writer._generate_filename_from_url')
    @patch('html2text.HTML2Text')
    def test_save_content_as_markdown_mkdir_error(self, MockHTML2Text, mock_gen_filename, mock_file_open, mock_mkdir_error):
        mock_h_instance = MockHTML2Text.return_value
        mock_h_instance.handle.return_value = "## Markdown"
        mock_gen_filename.return_value = "mkdir_error.md"

        result_filepath = save_content_as_markdown("http://example.com/mkdir_fail", "<h1>Content</h1>", "test_output_mkdir")

        self.assertIsNone(result_filepath)
        mock_mkdir_error.assert_called_once_with(parents=True, exist_ok=True)
        mock_file_open.assert_not_called()

    @patch('src.core.writer.Path.mkdir')
    @patch('src.core.writer.open', side_effect=IOError("open failed"))
    @patch('src.core.writer._generate_filename_from_url')
    @patch('html2text.HTML2Text')
    def test_save_content_as_markdown_file_open_error(self, MockHTML2Text, mock_gen_filename, mock_open_error, mock_mkdir):
        mock_h_instance = MockHTML2Text.return_value
        mock_h_instance.handle.return_value = "## Markdown"
        mock_gen_filename.return_value = "open_error.md"

        output_dir = "test_output_open"
        expected_file_path_obj = Path(output_dir) / "open_error.md"

        result_filepath = save_content_as_markdown("http://example.com/open_fail", "<h1>Content</h1>", output_dir)

        self.assertIsNone(result_filepath)
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_open_error.assert_called_once_with(expected_file_path_obj, 'w', encoding='utf-8')

    @patch('src.core.writer.Path.mkdir')
    @patch('src.core.writer.open', new_callable=mock_open)
    @patch('src.core.writer._generate_filename_from_url')
    @patch('html2text.HTML2Text')
    def test_save_content_as_markdown_default_output_dir(self, MockHTML2Text, mock_gen_filename, mock_file_open, mock_mkdir):
        mock_h_instance = MockHTML2Text.return_value
        mock_h_instance.handle.return_value = "## Default Dir Markdown"
        mock_gen_filename.return_value = "default_dir_file.md"

        page_url = "http://example.com/default_dir_test"
        html_content = "<h1>Default</h1>"

        # Call with default output_dir
        expected_filepath = str(Path("output") / "default_dir_file.md")

        result_filepath = save_content_as_markdown(page_url, html_content) # No output_dir arg

        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        # Check that the path object used for mkdir was Path("output") by checking its call to open
        # The mock_mkdir itself is Path.mkdir, not the instance.
        # The fact that mock_file_open is called with Path("output") / ... confirms output_path was Path("output")
        # No direct way to check the instance on which mock_mkdir (the method) was called without more complex mocking.
        # The assert_called_once_with for mock_mkdir is sufficient for its arguments.
        # args, _ = mock_mkdir.call_args # This would be empty for (parents=True, exist_ok=True)
        # self.assertEqual(args[0], Path("output")) # This is incorrect for method mock.

        mock_file_open.assert_called_once_with(Path("output") / "default_dir_file.md", 'w', encoding='utf-8')
        mock_file_open().write.assert_called_once_with("## Default Dir Markdown")
        self.assertEqual(result_filepath, expected_filepath)

if __name__ == '__main__':
    unittest.main()
