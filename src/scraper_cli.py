#!/usr/bin/env python3
# scraper_cli.py

import sys
import logging
from .core.config_loader import load_config, ConfigError
from .core.logging_config import setup_logging # Added

# Configure logger for this module
# Note: Basic config should ideally be done once at the application entry point.
# We will do it in main().
logger = logging.getLogger(__name__)

def get_user_url() -> str | None:
    """
    Prompts the user for a URL and performs basic validation.
    Keeps prompting until a valid-looking URL is provided or the user cancels.
    """
    while True:
        try:
            url = input("Please enter the full URL of the documentation site to scrape (e.g., http://example.com): ")
            if not url:
                logger.warning("URL cannot be empty. Please try again or press Ctrl+C/Ctrl+D to exit.")
                continue
            if not (url.startswith("http://") or url.startswith("https://")):
                logger.warning("Invalid URL format. Please ensure it starts with 'http://' or 'https://'.")
                if "." in url and "/" in url and not url.startswith("http"):
                     try_prepend = input(f"Did you mean 'https://{url}'? (yes/no): ").lower()
                     if try_prepend == 'yes':
                         url = f"https://{url}"
                         logger.info(f"Using URL: {url}")
                     else:
                         continue
                else:
                    continue

            if "://" in url and "." not in url.split("://", 1)[1]:
                logger.warning("URL appears incomplete (missing a domain like '.com'). Please provide a full URL.")
                continue
            return url
        except EOFError: # Handle Ctrl+D
            logger.info("\nOperation cancelled by user (EOF). Exiting.")
            sys.exit(0)


def main():
    """
    Main entry point for the d4jules scraper CLI application.
    """
    # --- Setup Structured Logging ---
    setup_logging() # Initialize logging configuration
    # Logger instance for this module is already created at the top level

    logger.info("--- Welcome to d4jules - Documentation Scraper ---")

    # Load configuration
    config = None
    try:
        config = load_config()
        logger.info("Configuration loaded successfully.")
        logger.debug(f"Loaded config: API Key present: {'api_key' in config}, Model: {config.get('model_name')}")
    except ConfigError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please ensure 'config/config.ini' exists and is correctly formatted.")
        logger.error("You can copy 'config/config.ini.template' to 'config/config.ini' and fill in your API_KEY.")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"An unexpected error occurred while loading configuration: {e}", exc_info=True)
        sys.exit(1)

    # Get URL from user
    target_url = None
    try:
        target_url = get_user_url()
        if target_url is None:
            logger.error("No URL provided. Exiting.") # Should be caught by get_user_url's loop or EOF
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user (Ctrl+C). Exiting.")
        sys.exit(0)

    logger.info(f"URL to be processed: {target_url}")

    logger.info("Initializing Crawler...")
    try:
        # Imports moved here to ensure logging is configured before they might log something at import time (if they did)
        from .core.crawler import Crawler
        from .core.analyzer import analyze_url_for_selectors, AnalyzerError, NetworkError, LLMAnalysisError
        from .core.parser import parse_html_content
        from .core.writer import save_content_as_markdown

        limits_settings = config.get('crawler_limits', {})
        max_pages_val = limits_settings.get('max_pages')
        max_depth_val = limits_settings.get('max_depth')

        max_pages = None
        if isinstance(max_pages_val, int) and max_pages_val > 0:
            max_pages = max_pages_val

        max_depth = None
        if isinstance(max_depth_val, int) and max_depth_val >= 0:
            max_depth = max_depth_val

        analyzer_config_dict = {
            'api_key': config.get('api_key'),
            'model_name': config.get('model_name')
        }

        # Determine output directory
        # Example: output_dir = config.get('scraper_settings', {}).get('default_output_dir', 'output')
        # For now, hardcoding to 'output' as per Crawler's new default.
        output_dir = config.get('output_dir', 'output')


        crawler_instance = Crawler(
            base_url=target_url,
            max_pages=max_pages,
            max_depth=max_depth,
            analyzer_func=analyze_url_for_selectors,
            parser_func=parse_html_content,
            writer_func=save_content_as_markdown,
            analyzer_config=analyzer_config_dict,
            output_dir=output_dir
        )
        crawler_instance.start_crawling()

    except ImportError as e:
        logger.critical(f"Error importing core components: {e}. Please ensure src.core modules exist and are correct.", exc_info=True)
        sys.exit(1)
    except ConfigError as e: # Already handled above, but good practice if Crawler init itself could raise it
        logger.error(f"Configuration error during Crawler initialization: {e}", exc_info=True)
        sys.exit(1)
    except ValueError as e: # Catch ValueError from Crawler's __init__
        logger.error(f"Error initializing Crawler: {e}", exc_info=True)
        sys.exit(1)
    except (AnalyzerError, NetworkError, LLMAnalysisError) as e: # Errors from analyzer if not caught by crawler
        logger.error(f"Analysis phase error: {e}", exc_info=True)
        sys.exit(1)
    except Exception as e:
        logger.critical(f"An unexpected error occurred during the crawling process: {e}", exc_info=True)
        sys.exit(1)

    logger.info("--- d4jules scraping process finished ---")


if __name__ == "__main__":
    main()
