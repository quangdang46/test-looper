#!/usr/bin/env python3
"""A simple hello script using argparse with greeting from greeting.py.

NOTE: Run this script from the repo root (where greeting.py lives),
otherwise the import will fail with ModuleNotFoundError.
"""

import argparse

from greeting import greet


def main() -> None:
    """Parse command-line arguments and print a greeting."""
    parser = argparse.ArgumentParser(description="Print a greeting.")
    parser.add_argument(
        "--name",
        type=str,
        default="World",
        help="Name to greet (default: World)",
    )
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
