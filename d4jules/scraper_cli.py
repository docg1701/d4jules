#!/usr/bin/env python3
# d4jules/scraper_cli.py

import sys
from d4jules.src.core.config_loader import load_config, ConfigError

def get_user_url() -> str | None:
    """
    Prompts the user for a URL and performs basic validation.
    Keeps prompting until a valid-looking URL is provided or the user cancels.
    """
    while True:
        url = input("Please enter the full URL of the documentation site to scrape (e.g., http://example.com): ")
        if not url:
            print("URL cannot be empty. Please try again or press Ctrl+C to exit.")
            continue
        if not (url.startswith("http://") or url.startswith("https://")):
            print("Invalid URL format. Please ensure it starts with 'http://' or 'https://'.")
            # Offer to prepend if it looks like a common mistake
            if "." in url and "/" in url and not url.startswith("http"):
                 try_prepend = input(f"Did you mean 'https://{url}'? (yes/no): ").lower()
                 if try_prepend == 'yes':
                     url = f"https://{url}"
                     print(f"Using URL: {url}")
                     # Fall through to validation again, though it should pass now
                 else:
                     continue # Re-prompt
            else:
                continue # Re-prompt

        # Basic check for at least one dot after http(s):// and some path or TLD
        if "://" in url and "." not in url.split("://", 1)[1]:
            print("URL appears incomplete (missing a domain like '.com'). Please provide a full URL.")
            continue

        return url

def main():
    """
    Main entry point for the d4jules scraper CLI application.
    """
    print("--- Welcome to d4jules - Documentation Scraper ---")

    # Load configuration
    config = None
    try:
        # Assuming config_loader is in d4jules.src.core
        # The path to config.ini is relative to the project root where start.sh is typically run
        # If scraper_cli.py is run directly from d4jules/, this path might need adjustment
        # For now, using the path as defined in load_config default
        config = load_config()
        print("Configuration loaded successfully.")
        # You might want to print some config values here for debugging if needed, e.g., config.get('model_name')
    except ConfigError as e:
        print(f"Configuration error: {e}")
        print("Please ensure 'd4jules/config/config.ini' exists and is correctly formatted.")
        print("You can copy 'd4jules/config/config.ini.template' to 'd4jules/config/config.ini' and fill in your API_KEY.")
        sys.exit(1)
    except Exception as e: # Catch any other unexpected error during config load
        print(f"An unexpected error occurred while loading configuration: {e}")
        sys.exit(1)

    # Get URL from user
    target_url = None
    try:
        target_url = get_user_url()
        if target_url is None: # Should not happen with current get_user_url loop, but as safeguard
            print("No URL provided. Exiting.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting.")
        sys.exit(0)

    print(f"\nURL to be processed: {target_url}")

    # Placeholder for next steps
    # print("\nURL received. Further processing (analysis, scraping) will be implemented in next tasks.")
    # print("----------------------------------------------------")

    print("\nInitializing Crawler...")
    try:
        # Crawler class is in d4jules.src.core.crawler
        from d4jules.src.core.crawler import Crawler

        # Extract limits from config (now a dict), defaulting to None if not specified
        # load_config now processes sections into nested dicts, converting numbers
        limits_settings = config.get('crawler_limits', {}) # section name is lowercased by load_config

        max_pages_val = limits_settings.get('max_pages') # Will be int if conversion in load_config worked
        max_depth_val = limits_settings.get('max_depth')

        max_pages = None
        if isinstance(max_pages_val, int) and max_pages_val > 0:
            max_pages = max_pages_val

        max_depth = None
        if isinstance(max_depth_val, int) and max_depth_val >= 0: # Depth 0 is valid (crawl only base URL)
            max_depth = max_depth_val

        crawler_instance = Crawler(
            base_url=target_url,
            config=config, # Pass the whole config dict, Crawler can pick what it needs (e.g. api_key)
            max_pages=max_pages,
            max_depth=max_depth
        )
        crawler_instance.start_crawling()

    except ImportError as e:
        print(f"Error importing Crawler: {e}. Please ensure d4jules.core.crawler module exists.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during the crawling process: {e}")
        # Consider more detailed error logging or specific exception handling here
        sys.exit(1)

    print("\n--- d4jules scraping process finished ---")


if __name__ == "__main__":
    main()
