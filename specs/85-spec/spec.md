# Spec: Add `hello.py` (Issue #85)

## Problem

**Issue #85** asks to create a `hello.py` script that prints `"Hello from Looper!"` with an optional `--name` flag.

## Current State

`hello.py` already exists on `main` with the exact behavior requested by this issue. It was implemented and merged via **PR #72** (commits `7a3ca8e` and `e26dea2`):

```python
#!/usr/bin/env python3
"""A simple hello script with argparse support."""

import argparse

def greet(name: str = "Looper") -> str:
    """Return a greeting string for the given name."""
    return f"Hello from {name}!"

def main() -> None:
    """Parse command-line arguments and print a greeting."""
    parser = argparse.ArgumentParser(description="Print a greeting.")
    parser.add_argument(
        "--name",
        type=str,
        default="Looper",
        help="Name to greet (default: Looper)",
    )
    args = parser.parse_args()
    print(greet(args.name))

if __name__ == "__main__":
    main()
```

The file lives at the repo root (`hello.py`), uses `argparse` with a `--name` flag defaulting to `"Looper"`, has its own `greet()` function with the `"Hello from {name}!"` format, and includes a shebang line and `__name__` guard.

## Goals

1. Verify that `hello.py` (already on `main`) meets all acceptance criteria from issue #85.
2. If the existing implementation is correct, confirm the issue can be closed as already complete.
3. If any discrepancy is found, identify and fix it.

## Non-goals

- No changes to `greeting.py` or its test infrastructure.
- No refactoring across scripts — `hello.py` owns its own `greet()` with the `"Hello from {name}!"` format, distinct from `greeting.py`'s `"Hello, {name}!"`.

---

## Implementation Steps

### Step 1 — Verify `hello.py` on `main`

Run acceptance tests against the existing `hello.py`:

```bash
cd /private/tmp/test-looper

# AC 1: bare invocation prints "Hello from Looper!"
python3 hello.py
# Expected: "Hello from Looper!"

# AC 2: --name flag overrides the default
python3 hello.py --name Alice
# Expected: "Hello from Alice!"

# AC 3: quoted names with spaces work
python3 hello.py --name "Bob Dole"
# Expected: "Hello from Bob Dole!"

# AC 4: --help prints usage information
python3 hello.py --help
# Expected: usage text describing --name flag

# AC 5: --unknown-flag exits non-zero with error
python3 hello.py --unknown-flag
# Expected: non-zero exit, argparse error message
```

### Step 2 — Confirm backward compatibility

Ensure the existing `greeting.py` is untouched:

```bash
python3 greeting.py
# Expected: "Hello, World!"

python3 greeting.py Alice
# Expected: "Hello, Alice!"

python3 -c "from greeting import greet; print(greet())"
# Expected: "Hello, World!"
```

### Step 3 — Verify file structure

Confirm `hello.py` is at the repo root (not inside `.looper/`):

```bash
ls -la hello.py
# Expected: a regular file at the repo root
```

---

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | Verify (already exists) | Created by PR #72; should already meet all criteria |
| `greeting.py` | untouched | No changes needed |

## Acceptance Criteria

1. `python3 hello.py` prints `Hello from Looper!`
2. `python3 hello.py --name Alice` prints `Hello from Alice!`
3. `python3 hello.py --name "Bob Dole"` prints `Hello from Bob Dole!`
4. `python3 hello.py --help` prints help text with `--name`
5. `python3 hello.py --unknown-flag` exits non-zero
6. `greeting.py` continues to work as before
