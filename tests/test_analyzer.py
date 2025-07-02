import unittest
from unittest.mock import patch, MagicMock
import os
import requests

# Ensure d4jules.src.core is discoverable.
# This might require adjusting PYTHONPATH or how tests are run in a real CI.
# For this environment, direct import is attempted.
from d4jules.src.core.analyzer import (
    analyze_url_for_selectors,
    HtmlSelectors,
    AnalyzerError,
    NetworkError,
    LLMAnalysisError
)
# Note: ConfigError from config_loader is not directly tested here,
# as analyzer.py does its own config validation for keys it needs.

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.test_url = "http://fake-test-url.com"
        self.sample_html_content = "<html><body><h1>Title</h1><p>Content</p><nav><a href='/nav'>Nav</a></nav></body></html>"
        self.mock_config_valid = {
            'api_key': 'test_api_key',
            'model_name': 'test_model'
        }
        self.mock_config_no_apikey = {
            'model_name': 'test_model'
        }
        self.mock_config_no_modelname = {
            'api_key': 'test_api_key'
        }

    @patch('d4jules.src.core.analyzer.requests.get')
    @patch('d4jules.src.core.analyzer.ChatGoogleGenerativeAI')
    def test_analyze_url_success(self, MockChatGoogleGenerativeAI, mock_requests_get):
        # Setup mock for requests.get
        mock_response_get = MagicMock()
        mock_response_get.text = self.sample_html_content
        mock_response_get.raise_for_status = MagicMock() # Ensure it doesn't raise error
        mock_requests_get.return_value = mock_response_get

        # Setup mock for LLM
        mock_llm_instance = MagicMock()
        mock_structured_llm = MagicMock()
        expected_selectors = HtmlSelectors(
            content_selector="p",
            navigation_selector="nav a",
            next_page_selector=None
        )
        mock_structured_llm.invoke.return_value = expected_selectors
        mock_llm_instance.with_structured_output.return_value = mock_structured_llm
        MockChatGoogleGenerativeAI.return_value = mock_llm_instance

        # Call the function
        result = analyze_url_for_selectors(self.test_url, self.mock_config_valid)

        # Assertions
        mock_requests_get.assert_called_once_with(self.test_url, timeout=30)
        MockChatGoogleGenerativeAI.assert_called_once_with(model=self.mock_config_valid['model_name'], temperature=0)
        mock_llm_instance.with_structured_output.assert_called_once_with(HtmlSelectors)
        mock_structured_llm.invoke.assert_called_once() # We can inspect the prompt if needed
        self.assertEqual(result, expected_selectors)
        self.assertEqual(os.environ.get("GOOGLE_API_KEY"), self.mock_config_valid['api_key'])


    @patch('d4jules.src.core.analyzer.requests.get')
    def test_analyze_url_network_error(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.RequestException("Test network error")

        with self.assertRaisesRegex(NetworkError, f"Error fetching URL '{self.test_url}': Test network error"):
            analyze_url_for_selectors(self.test_url, self.mock_config_valid)

    @patch('d4jules.src.core.analyzer.requests.get')
    @patch('d4jules.src.core.analyzer.ChatGoogleGenerativeAI')
    def test_analyze_url_llm_init_error(self, MockChatGoogleGenerativeAI, mock_requests_get):
        mock_response_get = MagicMock()
        mock_response_get.text = self.sample_html_content
        mock_requests_get.return_value = mock_response_get

        MockChatGoogleGenerativeAI.side_effect = Exception("Test LLM init error")

        with self.assertRaisesRegex(LLMAnalysisError, "Error initializing LLM or structuring output: Test LLM init error"):
            analyze_url_for_selectors(self.test_url, self.mock_config_valid)

    @patch('d4jules.src.core.analyzer.requests.get')
    @patch('d4jules.src.core.analyzer.ChatGoogleGenerativeAI')
    def test_analyze_url_llm_invoke_error(self, MockChatGoogleGenerativeAI, mock_requests_get):
        mock_response_get = MagicMock()
        mock_response_get.text = self.sample_html_content
        mock_requests_get.return_value = mock_response_get

        mock_llm_instance = MagicMock()
        mock_structured_llm = MagicMock()
        mock_structured_llm.invoke.side_effect = Exception("Test LLM invoke error")
        mock_llm_instance.with_structured_output.return_value = mock_structured_llm
        MockChatGoogleGenerativeAI.return_value = mock_llm_instance

        with self.assertRaisesRegex(LLMAnalysisError, f"Error during LLM analysis for '{self.test_url}': Test LLM invoke error"):
            analyze_url_for_selectors(self.test_url, self.mock_config_valid)

    @patch('d4jules.src.core.analyzer.requests.get')
    @patch('d4jules.src.core.analyzer.ChatGoogleGenerativeAI')
    def test_analyze_url_llm_bad_response_type(self, MockChatGoogleGenerativeAI, mock_requests_get):
        mock_response_get = MagicMock()
        mock_response_get.text = self.sample_html_content
        mock_requests_get.return_value = mock_response_get

        mock_llm_instance = MagicMock()
        mock_structured_llm = MagicMock()
        mock_structured_llm.invoke.return_value = {"data": "not an HtmlSelectors object"} # Incorrect type
        mock_llm_instance.with_structured_output.return_value = mock_structured_llm
        MockChatGoogleGenerativeAI.return_value = mock_llm_instance

        with self.assertRaisesRegex(LLMAnalysisError, "LLM response is not of the expected type HtmlSelectors"):
            analyze_url_for_selectors(self.test_url, self.mock_config_valid)

    def test_missing_api_key_in_config(self):
        with self.assertRaisesRegex(AnalyzerError, "API key not found in configuration for analyzer."):
            analyze_url_for_selectors(self.test_url, self.mock_config_no_apikey)

    def test_missing_model_name_in_config(self):
        with self.assertRaisesRegex(AnalyzerError, "Model name not found in configuration for analyzer."):
            analyze_url_for_selectors(self.test_url, self.mock_config_no_modelname)

if __name__ == '__main__':
    unittest.main()
