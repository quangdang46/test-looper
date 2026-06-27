#!/usr/bin/env python3
"""A simple temperature converter script."""

import argparse
import sys


def celsius_to_fahrenheit(c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (c * 9 / 5) + 32


def fahrenheit_to_celsius(f: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (f - 32) * 5 / 9


def main() -> None:
    """Parse command-line arguments and print temperature conversions."""
    parser = argparse.ArgumentParser(description="Convert temperatures between Celsius and Fahrenheit.")
    parser.add_argument(
        "--celsius",
        type=float,
        help="Temperature in Celsius to convert to Fahrenheit",
    )
    parser.add_argument(
        "--fahrenheit",
        type=float,
        help="Temperature in Fahrenheit to convert to Celsius",
    )
    args = parser.parse_args()

    if args.celsius is not None:
        f = celsius_to_fahrenheit(args.celsius)
        print(f"{args.celsius}°C = {f}°F")

    if args.fahrenheit is not None:
        c = fahrenheit_to_celsius(args.fahrenheit)
        print(f"{args.fahrenheit}°F = {c}°C")

    if args.celsius is None and args.fahrenheit is None:
        parser.print_usage(sys.stderr)
        print(f"error: at least one of --celsius or --fahrenheit is required", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
