# Spec: hello.py with argparse `--name` flag

Issue: #101
Spec: specs/101-spec/spec.md

---

## Objective

Add a new `hello.py` script that prints a greeting and accepts a `--name` argument via Python's `argparse` module, building on the existing `greeting.py` library function.

## Background

The repository already has `greeting.py` (landed via #37) which provides a `greet(name)` function returning `"Hello, {name}!"`. The `hello.py` script should import and reuse this function, adding a CLI interface via `argparse` rather than hardcoding the name or reading from `sys.argv` directly.

A prior attempt (issue #93) added `hello.py` with argparse support but needs to be revisited. Issue #101 is a clean specification for the implementation.

## Current state

A `hello.py` script exists in the working tree at the repo root with the following implementation:

```python
#!/usr/bin/env python3
"""A simple hello script using argparse."""

import argparse
from greeting import greet


def main() -> None:
    """Parse command-line arguments and print a greeting."""
    parser = argparse.ArgumentParser(description="Print a greeting.")
    parser.add_argument(
        "--name",
        type=str,
        default="World",
        help="Name to greet (default: World)",
    )
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
```

This implementation correctly fulfills the issue requirements. Verification steps below confirm the script behaves as expected.

## Implementation Plan

Since the file already exists with the correct implementation, the primary work is **verification and landing**.

### Step 1 — Verify correctness

Run the following assertions from the repo root:

```bash
cd /private/tmp/test-looper
python3 hello.py                        # → "Hello, World!"
python3 hello.py --name Alice           # → "Hello, Alice!"
python3 hello.py --name "Bob Smith"     # → "Hello, Bob Smith!"
python3 hello.py --help                 # shows usage and --name flag description
python3 hello.py --unknown-flag         # exits with error (non-zero exit code)
```

Each outcome must match the expected output exactly.

### Step 2 — Verify no regressions in `greeting.py`

```bash
python3 greeting.py                     # → "Hello, World!"
python3 greeting.py Alice               # → "Hello, Alice!"
```

### Step 3 — Commit and push

```bash
git add hello.py
git commit -m "feat: hello.py with argparse --name flag, reusing greet() from greeting.py (#101)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

## Files Touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **Verify** (exists) | Imports `greet` from `greeting.py`; parses `--name` via argparse with default `"World"` |
| `greeting.py` | Untouched | No changes needed |

## Acceptance Criteria

1. `python3 hello.py` prints `Hello, World!`
2. `python3 hello.py --name Alice` prints `Hello, Alice!`
3. `python3 hello.py --name "Bob Smith"` prints `Hello, Bob Smith!`
4. `python3 hello.py --help` displays usage text with `--name` flag described
5. `python3 hello.py --unknown-flag` exits non-zero with an error message
6. `greeting.py` remains unmodified
