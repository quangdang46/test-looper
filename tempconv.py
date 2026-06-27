#!/usr/bin/env python3
"""A simple temperature converter between Celsius and Fahrenheit."""

import argparse
import sys


def celsius_to_fahrenheit(c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (c * 9 / 5) + 32


def fahrenheit_to_celsius(f: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (f - 32) * 5 / 9


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert temperatures between Celsius and Fahrenheit."
    )
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

    if args.celsius is not None and args.fahrenheit is not None:
        c_to_f = celsius_to_fahrenheit(args.celsius)
        f_to_c = fahrenheit_to_celsius(args.fahrenheit)
        print(f"{args.celsius}°C = {c_to_f:.1f}°F, {args.fahrenheit}°F = {f_to_c:.1f}°C")
    elif args.celsius is not None:
        result = celsius_to_fahrenheit(args.celsius)
        print(f"{args.celsius}°C = {result:.1f}°F")
    elif args.fahrenheit is not None:
        result = fahrenheit_to_celsius(args.fahrenheit)
        print(f"{args.fahrenheit}°F = {result:.1f}°C")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
