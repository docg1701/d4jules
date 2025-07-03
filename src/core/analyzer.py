import os
import requests
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field, field_validator
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# --- Custom Exceptions ---
class AnalyzerError(Exception):
    """Base class for exceptions in the analyzer module."""
    pass

class NetworkError(AnalyzerError):
    """Raised for network-related errors (e.g., fetching URL)."""
    pass

class LLMAnalysisError(AnalyzerError):
    """Raised for errors related to LLM analysis."""
    pass

# --- Pydantic Model for Structured Output ---
class HtmlSelectors(BaseModel):
    """
    Pydantic model for defining the expected structured output from the LLM.
    Specifies CSS selectors for different parts of an HTML document.
    """
    content_selector: str = Field(
        ...,  # Ellipsis means this field is required
        description="CSS selector for the main content area of the page."
    )
    navigation_selector: str = Field(
        ...,
        description="CSS selector for the primary navigation links container (e.g., sidebar, header menu)."
    )
    next_page_selector: Optional[str] = Field(
        default=None,
        description="CSS selector for the 'next page' link, if present (e.g., in pagination)."
    )

    @field_validator('*', mode='before')
    @classmethod
    def ensure_str_or_none(cls, value: Any, field) -> Optional[str]:
        if value is None and field.name == 'next_page_selector':
            return None
        if not isinstance(value, str):
            raise ValueError(f"{field.name} must be a string or None for next_page_selector")
        if not value.strip() and field.name != 'next_page_selector': # content and nav selectors cannot be empty strings
             raise ValueError(f"{field.name} cannot be an empty or whitespace-only string.")
        return value.strip()


# --- Main Analyzer Function ---
def analyze_url_for_selectors(url: str, config: Dict[str, Any]) -> HtmlSelectors:
    """
    Analyzes the HTML content of a given URL using an LLM to extract
    CSS selectors for main content, navigation, and next page links.

    Args:
        url: The URL of the page to analyze.
        config: A dictionary containing configuration, expected to have
                'api_key' and 'model_name'.

    Returns:
        An HtmlSelectors object containing the extracted CSS selectors.

    Raises:
        AnalyzerError: If API key or model name is missing in config.
        NetworkError: If there's an error fetching the URL.
        LLMAnalysisError: If there's an error during LLM initialization,
                          invocation, or if the response is not as expected.
    """
    api_key = config.get('api_key')
    model_name = config.get('model_name')

    if not api_key:
        raise AnalyzerError("API key not found in configuration for analyzer.")
    if not model_name:
        raise AnalyzerError("Model name not found in configuration for analyzer.")

    # Set API key in environment for LangChain
    os.environ["GOOGLE_API_KEY"] = api_key

    # 1. Fetch HTML content
    try:
        response = requests.get(url, timeout=30) # Timeout from test_analyzer
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        html_content = response.text
    except requests.exceptions.RequestException as e:
        raise NetworkError(f"Error fetching URL '{url}': {e}")

    # 2. Prepare LLM and Prompt
    # For very large HTML, consider sending only body or a snippet.
    # Max ~1M tokens for Gemini Flash, but prompt + HTML should be less.
    # A simple heuristic: take first N characters, try to keep it under 200k for safety.
    MAX_HTML_LENGTH_FOR_PROMPT = 200000
    if len(html_content) > MAX_HTML_LENGTH_FOR_PROMPT:
        html_snippet = html_content[:MAX_HTML_LENGTH_FOR_PROMPT] + "\n... (HTML truncated)"
    else:
        html_snippet = html_content

    system_prompt = (
        "You are an expert HTML analyzer. Your task is to identify CSS selectors "
        "for key parts of a documentation website page. Provide selectors that are robust and general "
        "enough to likely work on other similar pages of the same site, but specific enough to "
        "correctly target the desired elements on *this* page. "
        "Focus on standard HTML structure and common ID/class naming conventions for documentation sites."
    )

    human_prompt_template = (
        "Analyze the following HTML content from the URL '{url}'. "
        "Identify and provide the CSS selectors for:\n"
        "1. The main content area (e.g., the article body, primary documentation text).\n"
        "2. The primary navigation section (e.g., sidebar links, table of contents, header menu for navigating between pages/sections).\n"
        "3. (Optional) The 'next page' link if there is clear pagination for sequential reading (e.g., a button or link with text like 'Next', '>', 'Próximo'). If no such element is obvious, omit this selector.\n\n"
        "HTML Content Snippet:\n"
        "------------------------\n"
        "{html_content}\n"
        "------------------------\n"
        "Return the selectors in the specified structured format."
    )

    try:
        llm = ChatGoogleGenerativeAI(model=model_name, temperature=0) # Temperature 0 for deterministic output
        structured_llm = llm.with_structured_output(HtmlSelectors)
    except Exception as e:
        raise LLMAnalysisError(f"Error initializing LLM or structuring output: {e}")

    # 3. Invoke LLM
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", human_prompt_template)
    ])

    chain = prompt | structured_llm

    try:
        # print(f"DEBUG: Sending HTML (snippet length: {len(html_snippet)}) to LLM for URL: {url}") # For debugging
        result = chain.invoke({
            "url": url,
            "html_content": html_snippet
        })
    except Exception as e:
        raise LLMAnalysisError(f"Error during LLM analysis for '{url}': {e}")

    if not isinstance(result, HtmlSelectors):
        raise LLMAnalysisError(
            f"LLM response is not of the expected type HtmlSelectors. Got: {type(result)}"
        )

    return result


if __name__ == '__main__':
    # This is a basic example of how to use the analyzer.
    # It requires a valid config.ini and network access.
    print("Running basic analyzer test...")

    # Create a dummy config for local testing
    # In a real scenario, this would come from load_config() in scraper_cli.py

    # IMPORTANT: To run this __main__ block, you need to:
    # 1. Have a 'config/config.ini' file with a valid GOOGLE_API_KEY and a MODEL_NAME.
    #    Example config.ini:
    #    [GOOGLE_AI]
    #    API_KEY = YOUR_ACTUAL_API_KEY
    #
    #    [LLM]
    #    MODEL_NAME = gemini-1.5-flash-latest
    #
    # 2. The 'config' directory must be in the same parent directory as 'src'
    #    when running this script directly for the load_config default path to work.
    #    Alternatively, provide the path to load_config.

    try:
        from ..core.config_loader import load_config, ConfigError # Relative import for when run as part of package
        from pathlib import Path # Import Path here, as it's used if this block succeeds
    except ImportError:
        # Fallback for running script directly (assuming src is in PYTHONPATH or similar)
        # This is tricky. For direct execution, you might need to adjust PYTHONPATH.
        # A simpler way for this demo is to hardcode a test config if load_config fails.
        print("Could not perform relative import of config_loader. Using placeholder config for demo.")
        print("Ensure GOOGLE_API_KEY is in your environment or hardcoded for this demo to work.")
        if not os.getenv("GOOGLE_API_KEY"):
            print("WARNING: GOOGLE_API_KEY environment variable not set. LLM call will likely fail.")

        # Placeholder config if load_config is not available for this direct run
        # User needs to ensure GOOGLE_API_KEY is in their environment for this to work
        # or replace os.getenv("GOOGLE_API_KEY") with their actual key for a quick test.
        test_config = {
            'api_key': os.getenv("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY_HERE"),
            'model_name': 'gemini-1.5-flash-latest' # Or your preferred model
        }
        if test_config['api_key'] == "YOUR_GOOGLE_API_KEY_HERE":
            print("Please set your GOOGLE_API_KEY in the script or environment to run the demo.")
            exit(1)

    else: # If relative import worked
        try:
            # Determine path to config.ini relative to this file's location
            # Assuming project structure: <root>/src/core/analyzer.py and <root>/config/config.ini
            current_dir = Path(__file__).parent.resolve()
            config_file_path = current_dir.parent.parent / "config" / "config.ini"

            if not config_file_path.exists():
                print(f"Config file not found at expected path: {config_file_path}")
                print("Please ensure config/config.ini exists with your API key.")
                # Fallback to placeholder config for the demo if file not found
                test_config = {
                    'api_key': os.getenv("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY_HERE"),
                    'model_name': 'gemini-1.5-flash-latest'
                }
                if test_config['api_key'] == "YOUR_GOOGLE_API_KEY_HERE":
                    print("Please set your GOOGLE_API_KEY in the script or environment to run the demo.")
                    exit(1)
            else:
                raw_config = load_config(str(config_file_path))
                # Extract the specific keys needed by analyze_url_for_selectors
                test_config = {
                    'api_key': raw_config.get('api_key'), # load_config provides it flat
                    'model_name': raw_config.get('model_name') # load_config provides it flat
                }
                if not test_config['api_key'] or not test_config['model_name']:
                    print("API_KEY or MODEL_NAME missing from loaded config.ini. Check your config file.")
                    exit(1)

        except ConfigError as e:
            print(f"Error loading config: {e}")
            exit(1)


    # Test URL (use a site that's generally accessible and has clear structure)
    # Python docs are a good candidate.
    # test_url = "https://docs.python.org/3/library/pathlib.html"
    test_url = input(f"Enter a URL to analyze (e.g., https://docs.python.org/3/library/pathlib.html): ")
    if not test_url:
        test_url = "https://docs.python.org/3/library/pathlib.html"


    print(f"\nAnalyzing URL: {test_url} with model {test_config['model_name']}")

    try:
        selectors = analyze_url_for_selectors(test_url, test_config)
        print("\nSuccessfully extracted selectors:")
        print(f"  Content Selector: {selectors.content_selector}")
        print(f"  Navigation Selector: {selectors.navigation_selector}")
        print(f"  Next Page Selector: {selectors.next_page_selector if selectors.next_page_selector else 'N/A'}")
    except AnalyzerError as e:
        print(f"\nAnalysis Error: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

    # Clean up environment variable if it was set by this script
    if "GOOGLE_API_KEY" in os.environ and os.environ["GOOGLE_API_KEY"] == test_config['api_key']:
         # Be cautious if the key was already in the environment from elsewhere
         # For this demo, we assume we set it if it matches test_config.
         # A more robust way would be to store original value and restore.
         # For simplicity here, if it matches what we might have set, we unset.
         # This is mainly for the case where GOOGLE_API_KEY was NOT in env before this script.
         # If it was, this del might be undesired.
         # However, Langchain typically expects it in env.
         # The test code sets it and doesn't unset, so this is more for the __main__ demo.
         # Given the test sets it and doesn't unset, perhaps it's fine to leave it.
         # For now, let's not delete it, to align with test behavior.
         # del os.environ["GOOGLE_API_KEY"]
         pass
