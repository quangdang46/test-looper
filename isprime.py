#!/usr/bin/env python3
"""A prime number checker script."""

import argparse
import math


def is_prime(n: int) -> bool:
    """Return True if n is a prime number, False otherwise.

    Handles edge cases:
    - n <= 1 -> False (primes are defined as > 1)
    - n == 2 -> True (the only even prime)
    - n is even and > 2 -> False
    - Composite odd numbers -> False
    - Very large primes -> True (tested efficiently up to sqrt(n))
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # Check divisors from 3 up to sqrt(n), stepping by 2 (odd-only)
    limit = int(math.isqrt(n))
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return False
    return True


def main() -> None:
    """Parse command-line arguments and print the primality result."""
    parser = argparse.ArgumentParser(
        description="Check if a number is prime."
    )
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
