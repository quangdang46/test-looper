#!/usr/bin/env python3
"""A simple Fibonacci number script."""


def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number.

    Args:
        n: The index in the Fibonacci sequence (non-negative integer).

    Returns:
        The nth Fibonacci number.

    Raises:
        ValueError: If n is negative.
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
    import argparse

    parser = argparse.ArgumentParser(
        description="Print the first N Fibonacci numbers."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of Fibonacci numbers to print (default: 10)",
    )
    args = parser.parse_args()

    if args.count < 0:
        print(f"Error: --count must be non-negative, got {args.count}")
        return

    for i in range(args.count):
        val = fibonacci(i)
        print(f"F({i}) = {val}")


if __name__ == "__main__":
    main()
