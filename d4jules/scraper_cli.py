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
        # Assuming Crawler class is in d4jules.core.crawler
        from d4jules.core.crawler import Crawler

        # Extract limits from config, defaulting to None if not specified
        # The structure config['limits']['max_pages'] is assumed from task D07/D02
        limits_config = config.get('crawler_limits', {}) # Changed section name to 'crawler_limits' for clarity
        max_pages = limits_config.getint('max_pages', fallback=None) # Use getint with fallback
        max_depth = limits_config.getint('max_depth', fallback=None) # Use getint with fallback

        if max_pages is not None: # getint might return 0 if key exists but is empty, treat 0 as unlimited for now or specific handling
             if max_pages <= 0: max_pages = None # Treat 0 or negative as no limit
        if max_depth is not None:
             if max_depth < 0: max_depth = None # Treat negative as no limit (0 means only base_url)


        crawler_instance = Crawler(
            base_url=target_url,
            config=config, # Pass the whole config object, Crawler can pick what it needs
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
