#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
goodbye.py — Sends off the user with a friendly farewell.

Prints a goodbye message to stdout. Defaults to "Goodbye from Looper!"
when no custom name is provided.

Usage:
    python3 goodbye.py
    python3 goodbye.py --name World
    ./goodbye.py --name "Bob"
"""

import argparse


def get_goodbye(name: str = "Looper") -> str:
    """Return a goodbye string for the given name."""
    return f"Goodbye from {name}!"


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a configurable goodbye.")
    parser.add_argument(
        "--name",
        type=str,
        default="Looper",
        help="The name to say goodbye to (default: Looper).",
    )
    args = parser.parse_args()
    print(get_goodbye(args.name))


if __name__ == "__main__":
    main()
