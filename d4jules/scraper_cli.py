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
    print("\nURL received. Further processing (analysis, scraping) will be implemented in next tasks.")
    print("----------------------------------------------------")


if __name__ == "__main__":
    main()
