# Spec: Add a Temperature Converter Script (Issue #160)

## Problem

**Issue #160** asks for a `tempconv.py` script that converts between Celsius and Fahrenheit. The script should provide two conversion functions (`celsius_to_fahrenheit` and `fahrenheit_to_celsius`) and a CLI via `argparse` with `--celsius` and `--fahrenheit` flags. Both flags should be combinable to show both conversions, and the script must handle non-numeric input gracefully.

## Goals

1. Create an executable `tempconv.py` at the repo root.
2. Define `celsius_to_fahrenheit(c: float) -> float` and `fahrenheit_to_celsius(f: float) -> float` conversion functions.
3. Use `argparse` for CLI argument parsing with `--celsius` and `--fahrenheit` flags.
4. If both flags are provided, show both conversions (e.g. `100°C = 212°F, 32°F = 0°C`).
5. Handle non-numeric input gracefully with a clear error message and non-zero exit code.
6. Include a `main()` function with `if __name__ == "__main__":` guard.
7. Shebang line for direct execution.

## Non-goals

- No changes to existing files (`greeting.py`, `hello.py`, or others).
- No packaging / `setup.py` / `pyproject.toml`.
- No unit test files — functions are pure and easily testable manually.
- No interactive mode — all inputs via CLI flags.

---

## Implementation Steps

### Step 1 — Create `tempconv.py`

Create a new file at the repo root (`/private/tmp/test-looper/tempconv.py`).

**Structure:**

```python
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
```

**Rationale for key choices:**

| Choice | Reason |
|--------|--------|
| `type=float` for argparse | Handles both integer and decimal inputs; invalid strings like `"abc"` cause argparse to exit with a clear error automatically. |
| `args.celsius is not None` checks | The default is `None`, so we distinguish "flag not given" from "flag given with value 0". |
| Both-flag branch first | When both are provided, both conversions are shown in one line as specified. |
| `.1f` format | One decimal place is standard for temperature display (e.g. `100°C = 212.0°F`), avoids floating-point noise. |
| `parser.print_help()` + `sys.exit(1)` | When no flags are provided, shows usage and exits with non-zero rather than silently doing nothing. |
| shebang line | Makes the file directly executable (`./tempconv.py`) for local testing. |
| `__name__ == "__main__"` guard | Allows the conversion functions to be imported from `tempconv.py` in the future if needed. |
| `sys` import | Required for `sys.exit(1)` in the no-args case. |

### Step 2 — Verify correctness

After writing the file, validate:

```bash
cd /private/tmp/test-looper
python3 tempconv.py --celsius 0          # → "0.0°C = 32.0°F"
python3 tempconv.py --celsius 100        # → "100.0°C = 212.0°F"
python3 tempconv.py --fahrenheit 32      # → "32.0°F = 0.0°C"
python3 tempconv.py --fahrenheit 212     # → "212.0°F = 100.0°C"
python3 tempconv.py --celsius 25 --fahrenheit 77  # → "25.0°C = 77.0°F, 77.0°F = 25.0°C"
python3 tempconv.py                      # → prints help, exits 1
python3 tempconv.py --celsius abc        # → argparse error, exits 2
python3 tempconv.py -40                  # → prints help, exits 1 (no flags)
python3 tempconv.py --help               # → shows help text
```

The first four tests each exercise one conversion direction at a well-known value. The fifth tests combined flags. The sixth tests the no-flag error path. The seventh tests non-numeric input handling (argparse built-in). The eighth tests that bare numbers are rejected (they need `--celsius` or `--fahrenheit`).

### Step 3 — Commit and push

From the main repo at `/private/tmp/test-looper`:

```bash
git add tempconv.py
git commit -m "feat: add tempconv.py temperature converter script (#160)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

---

## Files touched

| File | Action |
|------|--------|
| `tempconv.py` | **CREATE** — executable Python script with shebang, conversion functions, and argparse CLI |

## Backward compatibility

No breaking changes. All existing files (`greeting.py`, `hello.py`) remain unchanged and fully functional.

## Edge cases and error handling

| Scenario | Behavior |
|----------|----------|
| `--celsius` with no value | argparse error: `argument --celsius: expected one argument` |
| `--celsius abc` (non-numeric) | argparse error: `argument --celsius: invalid float value: 'abc'` |
| No flags provided | Prints help text to stdout, exits with code 1 |
| `--celsius 0` | Correctly converts, argparse stores `0.0` which passes the `is not None` check |
| `--celsius -40` | Correctly converts (-40°C = -40°F, the crossing point) |
| Very large numbers | `float` handles scientific notation like `1e6` — no artificial bounds |


