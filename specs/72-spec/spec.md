# Implementation Plan — Issue #72: Add hello.py script

## Overview

Create a `hello.py` script that prints a greeting message `"Hello from Looper!"` with optional `--name` flag support via `argparse`. This mirrors the existing `greeting.py` pattern while establishing `argparse`-based CLI conventions for the repo.

## Requirements

- Script: `hello.py` at the project root
- Default output: `Hello from Looper!`
- With `--name <NAME>`: output changes to `Hello from Looper, <NAME>!`
- Use Python standard library `argparse` (no external dependencies)
- Executable shebang (`#!/usr/bin/env python3`)
- Include `main()` guard (`if __name__ == "__main__"`)
- Include module-level docstring

## Specification

### CLI interface

```
$ python hello.py
Hello from Looper!

$ python hello.py --name Dang
Hello from Looper, Dang!

$ python hello.py --help
usage: hello.py [-h] [--name NAME]

Hello from Looper with optional personalized greeting.

options:
  -h, --help           show this help message and exit
  --name NAME          Your name (default: Looper)
```

### Expected code structure

```python
#!/usr/bin/env python3
"""A friendly greeting script using argparse."""

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Hello from Looper with optional personalized greeting."
    )
    parser.add_argument(
        "--name",
        type=str,
        default="Looper",
        help="Your name (default: Looper)",
    )
    return parser


def greet(name: str) -> str:
    """Return the greeting string."""
    return f"Hello from Looper{', ' + name if name != 'Looper' else ''}!"


def main() -> None:
    """Parse args and print greeting."""
    parser = build_parser()
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
```

### Implementation steps

1. Create `hello.py` at the project root with the code above.
2. Verify it runs without arguments: `python hello.py` → `Hello from Looper!`
3. Verify with `--name` flag: `python hello.py --name Dang` → `Hello from Looper, Dang!`
4. Verify `--help` displays correctly.

### Key design decisions

- **argparse over sys.argv**: Issue explicitly requests `argparse` support. This also establishes a pattern for future CLI scripts.
- **Module-scoped parser factory**: `build_parser()` returns the parser rather than parsing inline, making it importable and testable by other modules.
- **Pure function `greet()`**: Separates greeting logic from I/O, testable without argument parsing.
- **Default `--name` value of `"Looper"`**: Keeps the base case `"Hello from Looper!"` — the word "Looper" serves as the default name rather than requiring a sentinel.

### Relationship to existing code

The existing `greeting.py` (#30, `greet(name) → f"Hello, {name}!"`) uses `sys.argv` directly. This new script intentionally uses `argparse` to demonstrate a more robust pattern. Both scripts should be kept as independent examples.

### Edge cases

| Input | Expected output |
|---|---|
| (no args) | `Hello from Looper!` |
| `--name ""` | `Hello from Looper, !` |
| `--name Looper` | `Hello from Looper!` |
| `--name Alice Bob` | Error: unrecognized (space needs quoting) |

No validation on name content — empty string, spaces, and special characters are passed through as-is.
