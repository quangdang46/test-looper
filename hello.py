#!/usr/bin/env python3
"""Hello CLI — prints a greeting using argparse."""

import argparse


def greet(name: str = "World") -> str:
    """Return a greeting string for the given name."""
    return f"Hello, {name}!"


def main() -> None:
    """Parse command-line arguments and print a greeting."""
    parser = argparse.ArgumentParser(description="Print a greeting.")
    parser.add_argument("--name", "-n", default="World", help="Name to greet")
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
