#!/usr/bin/env python3
"""Check whether a number is prime."""

import argparse


def is_prime(n: int) -> bool:
    """Return True if n is prime, False otherwise.

    Handles edge cases:
    - n <= 1          -> False  (by definition, primes are > 1)
    - n == 2          -> True   (smallest and only even prime)
    - n % 2 == 0      -> False  (any other even number)

    For n > 2, tests odd divisors from 3 up to sqrt(n).
    The loop exits immediately when i*i exceeds n, i.e. when no divisor
    was found below sqrt(n).
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def main() -> None:
    """Parse CLI arguments and print primality result."""
    parser = argparse.ArgumentParser(
        description="Check if a number is prime.",
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
