#!/usr/bin/env python3
"""A simple hello script with argparse support, built on greeting.py."""

import argparse
from greeting import greet


def main() -> None:
    """Parse --name argument and print greeting."""
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
