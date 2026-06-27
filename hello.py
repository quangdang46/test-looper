#!/usr/bin/env python3
"""Greeting script with optional --name flag."""

import argparse
from greeting import greet


def main() -> None:
    """Parse --name and print the greeting."""
    parser = argparse.ArgumentParser(description="Print a greeting.")
    parser.add_argument("--name", default="Looper", help="Name to greet")
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
