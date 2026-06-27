#!/usr/bin/env python3
"""A prime number checker."""

import argparse
import math


def is_prime(n: int) -> bool:
    """Return True if n is a prime number, False otherwise.

    Handles edge cases: negative numbers, 0, and 1 all return False.
    Uses trial division up to sqrt(n) for efficiency with large numbers.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = int(math.isqrt(n))
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return False
    return True


def main() -> None:
    """Parse command-line arguments and print whether the number is prime."""
    parser = argparse.ArgumentParser(
        description="Check if a number is prime."
    )
    parser.add_argument(
        "--number",
        type=int,
        required=True,
        help="Number to check for primality",
    )
    args = parser.parse_args()
    print(is_prime(args.number))


if __name__ == "__main__":
    main()
