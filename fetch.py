#!/usr/bin/env python3
"""
A simple Python script that fetches a URL and prints the HTTP status code.

This script demonstrates basic HTTP web fetching functionality using Python's
standard library (urllib).
"""

import urllib.request
import urllib.error
import sys


def fetch_url_status(url: str) -> int:
    """
    Fetch the given URL and return the HTTP status code.

    Args:
        url: The URL to fetch

    Returns:
        The HTTP status code as an integer

    Raises:
        urllib.error.URLError: If there's a network or URL-related error
        urllib.error.HTTPError: If the server returns an HTTP error status
    """
    try:
        with urllib.request.urlopen(url) as response:
            return response.getcode()
    except urllib.error.HTTPError as e:
        # Server returned an error status (4xx, 5xx)
        print(f"HTTP Error: {e.code} - {e.reason}")
        raise
    except urllib.error.URLError as e:
        # Network-related error (DNS failure, connection refused, etc.)
        print(f"Network Error: {e.reason}")
        raise
    except Exception as e:
        # Any other unexpected error
        print(f"Unexpected error: {e}")
        raise


def main() -> None:
    """Main function to execute the fetch operation."""
    url = "https://example.com"

    try:
        print(f"Fetching {url}...")
        status_code = fetch_url_status(url)
        print(f"Status code: {status_code}")
        return 0

    except (urllib.error.HTTPError, urllib.error.URLError):
        # These are handled in fetch_url_status, so we exit with error code
        return 1
    except Exception as e:
        print(f"Unexpected error during fetch: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())