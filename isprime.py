#!/usr/bin/env python3
"""A prime number checker script."""

import argparse
import sys


def is_prime(n: int) -> bool:
    """Return True if n is prime, False otherwise.

    Handles edge cases: n <= 1 returns False, even numbers > 2 return False.
    Uses trial division up to sqrt(n) (step 2 after checking 2).
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    limit = int(n ** 0.5) + 1
    for i in range(3, limit, 2):
        if n % i == 0:
            return False
    return True


def main() -> None:
    """Parse command-line arguments and print the primality result."""
    parser = argparse.ArgumentParser(description="Check if a number is prime.")
    parser.add_argument(
        "--number",
        type=int,
        required=True,
        help="Integer to check for primality",
    )
    args = parser.parse_args()
    print(is_prime(args.number))


if __name__ == "__main__":
    main()
