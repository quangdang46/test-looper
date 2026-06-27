#!/usr/bin/env python3
"""A greeting script with argparse --name flag support."""

import argparse
from typing import Optional


def greet(name: Optional[str] = None) -> str:
    """Return a greeting string for the given name.

    Args:
        name: The person to greet. If None, returns the default greeting.

    Returns:
        A greeting string.
    """
    if name:
        return f"Hello from Looper, {name}!"
    return "Hello from Looper!"


def main() -> None:
    """Parse command-line arguments and print a greeting."""
    parser = argparse.ArgumentParser(description="Print a greeting from Looper.")
    parser.add_argument(
        "--name", "-n",
        type=str,
        default=None,
        help="The person to greet (optional).",
    )
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
