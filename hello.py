#!/usr/bin/env python3
"""A friendly greeting script using argparse."""

import argparse


def greet(name: str = "Looper") -> str:
    """Return a greeting string for the given name."""
    return f"Hello from {name}!"


def main() -> None:
    """Parse command-line arguments and print a greeting."""
    parser = argparse.ArgumentParser(
        description="Print a friendly greeting."
    )
    parser.add_argument(
        "--name", "-n",
        default="Looper",
        help="The name to greet (default: Looper).",
    )
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
