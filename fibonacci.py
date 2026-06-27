#!/usr/bin/env python3
"""A simple Fibonacci number generator."""

import argparse


def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number (0-indexed).

    Args:
        n: The index of the Fibonacci number to compute.

    Returns:
        The nth Fibonacci number.

    Raises:
        ValueError: If n is negative.

    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(10)
        55
    """
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def main() -> None:
    """Parse command-line arguments and print Fibonacci numbers."""
    parser = argparse.ArgumentParser(
        description="Print Fibonacci numbers."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="How many Fibonacci numbers to print (default: 10)",
    )
    args = parser.parse_args()
    if args.count < 0:
        parser.error("--count must be non-negative")
    for i in range(args.count):
        print(fibonacci(i))


if __name__ == "__main__":
    main()
