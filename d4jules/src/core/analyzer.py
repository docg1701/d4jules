import os
import requests
from typing import Optional, Dict, Any

from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
# Assuming ConfigError is defined in config_loader and imported via __init__
# If not, it might need to be defined here or imported differently if tests are run directly on analyzer
# For now, let's assume it would be imported from a shared exceptions module or config_loader
# from .config_loader import ConfigError # This would be a circular dependency if ConfigError is specific to config_loader

# Custom Exceptions
class AnalyzerError(Exception):
    """Base exception for analyzer module errors."""
    pass

class NetworkError(AnalyzerError):
    """Exception for network-related errors during HTML fetching."""
    pass

class LLMAnalysisError(AnalyzerError):
    """Exception for errors during LLM analysis or response parsing."""
    pass

# Pydantic model for structured output
class HtmlSelectors(BaseModel):
    """
    Defines the CSS selectors for extracting key information from a documentation page.
    """
    content_selector: str = Field(description="A CSS selector to identify the main content area of the page (e.g., 'article.content', 'div#main-text').")
    navigation_selector: str = Field(description="A CSS selector that targets navigation links to other relevant pages within the same documentation site (e.g., 'nav .menu-item a', 'ul.sidebar-links > li > a'). This should ideally capture links to other articles or sections, not just page furniture.")
    next_page_selector: Optional[str] = Field(default=None, description="A CSS selector for the 'next page' link if the content is paginated (e.g., 'a.pagination-next', 'link[rel=\"next\"]').")

    @validator('content_selector', 'navigation_selector', 'next_page_selector')
    def selector_must_be_valid_or_none(cls, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("Selector must be a string or None")
        if value == "": # Empty string is not a useful selector
            return None
        return value


def analyze_url_for_selectors(url: str, config: Dict[str, Any]) -> HtmlSelectors:
    """
    Analyzes the HTML content of a given URL to extract CSS selectors for content,
    navigation, and next page links using an LLM.

    Args:
        url: The URL of the documentation page to analyze.
        config: A dictionary containing configuration, expected to have:
                'api_key' (str): The Google AI API key.
                'model_name' (str): The name of the Gemini model to use.

    Returns:
        An HtmlSelectors Pydantic object containing the extracted selectors.

    Raises:
        NetworkError: If there's an issue fetching the URL.
        LLMAnalysisError: If there's an issue with LLM analysis or parsing the response.
        # ConfigError: If essential config keys ('api_key', 'model_name') are missing.
        # This should ideally be checked before calling this function, or ConfigError needs to be accessible.
        # For now, directly checking keys from 'config' dict.
    """
    api_key = config.get('api_key')
    model_name = config.get('model_name')

    if not api_key:
        # Re-raise or use a local error if ConfigError from config_loader is not directly available/appropriate here
        raise AnalyzerError("API key not found in configuration for analyzer.")
    if not model_name:
        raise AnalyzerError("Model name not found in configuration for analyzer.")

    os.environ["GOOGLE_API_KEY"] = api_key

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        html_content = response.text
    except requests.exceptions.RequestException as e:
        raise NetworkError(f"Error fetching URL '{url}': {e}")

    if not html_content:
        raise NetworkError(f"No content fetched from URL '{url}'.")

    try:
        llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
        structured_llm = llm.with_structured_output(HtmlSelectors)
    except Exception as e:
        raise LLMAnalysisError(f"Error initializing LLM or structuring output: {e}")

    max_html_length = 30000
    if len(html_content) > max_html_length:
        html_snippet = html_content[:max_html_length] + "\n... (HTML truncated) ..."
    else:
        html_snippet = html_content

    prompt_messages = [
        SystemMessage(
            content=(
                "You are an expert web scraper and frontend developer. Your task is to analyze the provided HTML "
                "content from a technical documentation website and identify robust CSS selectors for key page elements. "
                "Focus on selectors that are likely to be stable and accurately capture the intended information. "
                "Provide selectors for the main content area, primary navigation links (excluding headers/footers/breadcrumbs if possible, focus on links to other docs/articles), "
                "and a 'next page' link if present for pagination."
            )
        ),
        HumanMessage(
            content=f"""
            Please analyze the following HTML content from the URL: {url}

            HTML Content Snippet:
            ```html
            {html_snippet}
            ```

            Based on this HTML, identify the CSS selectors as per the required structured format.
            If a selector for 'next_page_selector' is not clearly identifiable or applicable, omit it or return null/None for it.
            Ensure the navigation_selector targets links that lead to other distinct documentation pages or main sections, not just in-page anchors or utility links unless they are the primary navigation.
            """
        ),
    ]

    try:
        llm_response = structured_llm.invoke(prompt_messages)

        if not isinstance(llm_response, HtmlSelectors):
             raise LLMAnalysisError(f"LLM response is not of the expected type HtmlSelectors. Got: {type(llm_response)}")

        return llm_response

    except Exception as e:
        raise LLMAnalysisError(f"Error during LLM analysis for '{url}': {e}")

# Removed the __main__ block to prevent syntax issues during import.
# Testing should be done via the dedicated test suite.
