#!/usr/bin/env python3
"""A friendly greeting script using argparse."""

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Hello from Looper with optional personalized greeting."
    )
    parser.add_argument(
        "--name",
        type=str,
        default="Looper",
        help="Your name (default: Looper)",
    )
    return parser


def greet(name: str) -> str:
    """Return the greeting string."""
    return f"Hello from Looper{', ' + name if name != 'Looper' else ''}!"


def main() -> None:
    """Parse args and print greeting."""
    parser = build_parser()
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
