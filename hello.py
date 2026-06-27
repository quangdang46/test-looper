#!/usr/bin/env python3
"""A simple greeting script using argparse."""

import argparse


def greet(name: str = "Looper") -> str:
    """Return a greeting string for the given name."""
    return f"Hello from {name}!"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Print a greeting."
    )
    parser.add_argument(
        "--name", "-n",
        default="Looper",
        help="Who to greet (default: Looper)"
    )
    return parser.parse_args()


def main() -> None:
    """Parse arguments and print the greeting."""
    args = parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
