import unittest
from unittest.mock import patch, MagicMock

# Import necessary components from the analyzer module
# Adjust the import path based on your project structure
# Assuming src is in PYTHONPATH or tests are run from project root
from src.core.analyzer import (
    analyze_url_for_selectors,
    HtmlSelectors,
    AnalyzerError,
    NetworkError,
    LLMAnalysisError
)
import requests.exceptions

import os # For patch.dict

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        self.test_url = "http://example.com/testpage"
        self.mock_config = {
            'api_key': 'test_api_key_XYZ123',
            'model_name': 'test_model_name'
        }
        self.expected_selectors = HtmlSelectors(
            content_selector="div.content",
            navigation_selector="nav.menu",
            next_page_selector="a.next"
        )
        self.mock_http_response = MagicMock()
        self.mock_http_response.text = "<html><body>Mock HTML for test</body></html>"
        self.mock_http_response.raise_for_status = MagicMock()

    @patch.dict(os.environ, {}, clear=True)
    @patch('src.core.analyzer.requests.get')
    @patch('src.core.analyzer.ChatGoogleGenerativeAI')
    @patch('langchain_core.runnables.base.RunnableSequence.invoke') # Corrected path
    def test_analyze_url_success(self, mock_chain_invoke, MockChatGoogleGenerativeAI, mock_requests_get):
        mock_requests_get.return_value = self.mock_http_response

        # Mock ChatGoogleGenerativeAI and its with_structured_output to ensure they are called
        mock_llm_instance = MagicMock()
        MockChatGoogleGenerativeAI.return_value = mock_llm_instance
        # The actual structured_llm object is part of the chain, whose invoke is now mocked

        mock_chain_invoke.return_value = self.expected_selectors

        result = analyze_url_for_selectors(self.test_url, self.mock_config)

        mock_requests_get.assert_called_once_with(self.test_url, timeout=30)
        self.mock_http_response.raise_for_status.assert_called_once()
        MockChatGoogleGenerativeAI.assert_called_once_with(model=self.mock_config['model_name'], temperature=0)
        mock_llm_instance.with_structured_output.assert_called_once_with(HtmlSelectors)
        mock_chain_invoke.assert_called_once()
        self.assertEqual(result, self.expected_selectors)
        self.assertIsInstance(result, HtmlSelectors)
        self.assertEqual(os.environ.get("GOOGLE_API_KEY"), self.mock_config['api_key'])

    @patch('src.core.analyzer.requests.get')
    def test_network_error(self, mock_requests_get):
        mock_requests_get.side_effect = requests.exceptions.RequestException("Test network error")

        with self.assertRaisesRegex(NetworkError, "Error fetching URL .*'http://example.com/testpage'.*: Test network error"):
            analyze_url_for_selectors(self.test_url, self.mock_config)
        mock_requests_get.assert_called_once_with(self.test_url, timeout=30)

    @patch.dict(os.environ, {}, clear=True)
    @patch('src.core.analyzer.requests.get')
    @patch('src.core.analyzer.ChatGoogleGenerativeAI')
    # No chain invoke here as error is before chain creation potentially
    def test_llm_initialization_error(self, MockChatGoogleGenerativeAI, mock_requests_get):
        mock_requests_get.return_value = self.mock_http_response # To pass the requests part
        MockChatGoogleGenerativeAI.side_effect = Exception("Test LLM init error")

        with self.assertRaisesRegex(LLMAnalysisError, "Error initializing LLM or structuring output: Test LLM init error"):
            analyze_url_for_selectors(self.test_url, self.mock_config)
        MockChatGoogleGenerativeAI.assert_called_once_with(model=self.mock_config['model_name'], temperature=0)
        self.assertEqual(os.environ.get("GOOGLE_API_KEY"), self.mock_config['api_key'])

    @patch.dict(os.environ, {}, clear=True)
    @patch('src.core.analyzer.requests.get')
    @patch('src.core.analyzer.ChatGoogleGenerativeAI')
    @patch('langchain_core.runnables.base.RunnableSequence.invoke') # Corrected path
    def test_llm_invoke_error(self, mock_chain_invoke, MockChatGoogleGenerativeAI, mock_requests_get):
        mock_requests_get.return_value = self.mock_http_response
        MockChatGoogleGenerativeAI.return_value = MagicMock()

        mock_chain_invoke.side_effect = Exception("Test LLM invoke error")

        expected_regex = r"Error during LLM analysis for '{}': Test LLM invoke error".format(self.test_url)
        with self.assertRaisesRegex(LLMAnalysisError, expected_regex):
            analyze_url_for_selectors(self.test_url, self.mock_config)
        mock_chain_invoke.assert_called_once()
        self.assertEqual(os.environ.get("GOOGLE_API_KEY"), self.mock_config['api_key'])

    @patch.dict(os.environ, {}, clear=True)
    @patch('src.core.analyzer.requests.get')
    @patch('src.core.analyzer.ChatGoogleGenerativeAI')
    @patch('langchain_core.runnables.base.RunnableSequence.invoke') # Corrected path
    def test_llm_bad_response_type(self, mock_chain_invoke, MockChatGoogleGenerativeAI, mock_requests_get):
        mock_requests_get.return_value = self.mock_http_response
        MockChatGoogleGenerativeAI.return_value = MagicMock()

        mock_chain_invoke.return_value = {"unexpected": "dictionary"}

        with self.assertRaisesRegex(LLMAnalysisError, "LLM response is not of the expected type HtmlSelectors. Got: <class 'dict'>"):
            analyze_url_for_selectors(self.test_url, self.mock_config)
        mock_chain_invoke.assert_called_once()
        self.assertEqual(os.environ.get("GOOGLE_API_KEY"), self.mock_config['api_key'])

    def test_missing_api_key_in_config(self):
        config_no_api_key = self.mock_config.copy()
        del config_no_api_key['api_key']
        with self.assertRaisesRegex(AnalyzerError, "API key not found in configuration for analyzer."):
            analyze_url_for_selectors(self.test_url, config_no_api_key)

    def test_missing_model_name_in_config(self):
        config_no_model_name = self.mock_config.copy()
        del config_no_model_name['model_name']
        with patch.dict(os.environ, {}, clear=True): # Ensure GOOGLE_API_KEY isn't set from elsewhere
             with self.assertRaisesRegex(AnalyzerError, "Model name not found in configuration for analyzer."):
                analyze_url_for_selectors(self.test_url, config_no_model_name)
        self.assertIsNone(os.environ.get("GOOGLE_API_KEY")) # Key shouldn't be set if model_name check fails

    @patch.dict(os.environ, {}, clear=True)
    @patch('src.core.analyzer.requests.get')
    @patch('src.core.analyzer.ChatGoogleGenerativeAI')
    @patch('langchain_core.runnables.base.RunnableSequence.invoke') # Corrected path
    def test_llm_returns_invalid_selector_data_causing_parser_error(self, mock_chain_invoke, MockChatGoogleGenerativeAI, mock_requests_get):
        mock_requests_get.return_value = self.mock_http_response
        MockChatGoogleGenerativeAI.return_value = MagicMock()

        mock_chain_invoke.side_effect = Exception("Simulated Pydantic validation error or OutputParserException")

        expected_regex = r"Error during LLM analysis for '{}': Simulated Pydantic validation error or OutputParserException".format(self.test_url)
        with self.assertRaisesRegex(LLMAnalysisError, expected_regex):
             analyze_url_for_selectors(self.test_url, self.mock_config)
        mock_chain_invoke.assert_called_once()
        self.assertEqual(os.environ.get("GOOGLE_API_KEY"), self.mock_config['api_key'])

if __name__ == '__main__':
    unittest.main()
