#!/usr/bin/env python3
"""A simple greeting script."""

import sys


def greet(name: str = "World") -> str:
    """Return a greeting string for the given name."""
    return f"Hello, {name}!"


def main() -> None:
    """Parse command-line arguments and print a greeting."""
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    print(greet(name))


if __name__ == "__main__":
    main()
