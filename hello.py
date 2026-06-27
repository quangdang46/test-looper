#!/usr/bin/env python3
"""Print a greeting with an optional custom name."""

import argparse
from typing import Optional


def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for hello.py.

    The parser accepts a single optional ``--name`` / ``-n`` flag
    whose default is ``"Looper"``.
    """
    parser = argparse.ArgumentParser(description="Print a greeting.")
    parser.add_argument(
        "--name",
        "-n",
        metavar="NAME",
        default="Looper",
        help="Who to greet",
    )
    return parser


def main(argv: Optional[list[str]] = None) -> None:
    """Parse arguments and print the greeting.

    Parameters
    ----------
    argv : list[str] or None
        Argument list to parse, or ``None`` to use ``sys.argv[1:]``.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    print(f"Hello from {args.name}!")


if __name__ == "__main__":
    main()
