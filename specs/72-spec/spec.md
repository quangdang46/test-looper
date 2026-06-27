# Spec: Implement `hello.py` (Issue #72)

> **Status:** Issue #72 is OPEN. A prior attempt (#93) landed `hello.py` on `main` but with a different approach (imported `greet()` from `greeting.py`, used `"Hello, {name}!"` format, default `"World"`). Issue #72 calls for its own `greet()` with `"Hello from {name}!"` format and `"Looper"` default. This plan reconciles the two by replacing the current `hello.py` with the #72-specified version.

## Context

Issue #72 (original): Add `hello.py` with its own `greet()` returning `"Hello from {name}!"`, using `argparse --name` with default `"Looper"`.

Issue #93 (merged): Added `hello.py` that **reuses** `greeting.py`'s `greet()` (returning `"Hello, {name}!"`) with default `"World"`.

The #93 implementation is currently on `main`. Issue #72 remains **open** and its requirements differ from what #93 delivered:

| Aspect | #72 requirement | #93 implementation (current `main`) |
|--------|----------------|-------------------------------------|
| `greet()` source | Own function in `hello.py` | Imports from `greeting.py` |
| Greeting format | `"Hello from {name}!"` | `"Hello, {name}!"` |
| Default `--name` | `"Looper"` | `"World"` |

## Goals

1. **Replace** the current `hello.py` with the version specified by #72 (own `greet()`, `"Hello from {name}!"`, default `"Looper"`).
2. Use `argparse` for CLI argument parsing with a `--name` flag.
3. Keep `greeting.py` unchanged — it retains its own `greet()` with `"Hello, {name}!"` format.
4. Both scripts remain independently runnable with distinct output formats.

## Non-goals

- No changes to `greeting.py` or its `greet()` function.
- No packaging / `setup.py` / `pyproject.toml`.
- No error handling beyond what `argparse` provides for `--name`.
- No changes to the `greeting.py` import behavior — `from greeting import greet` continues to work.

---

## Implementation Steps

### Step 1 — Replace `hello.py`

Overwrite the existing file at `hello.py` (repo root).

**Structure:**

```python
#!/usr/bin/env python3
"""A simple hello script with argparse --name flag. Uses its own greet()."""

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

**Key design decisions:**

| Choice | Rationale |
|--------|-----------|
| Own `greet()` (not importing from `greeting.py`) | Issue #72 specifies `"Hello from {name}!"`, which differs from `greeting.py`'s `"Hello, {name}!"`. These are deliberately distinct formats. |
| `default="Looper"` | Matches the issue description: bare invocation must print `"Hello from Looper!"`. |
| `--name` flag (not positional) | Self-documenting; consistent with the prior #93 implementation's convention. |
| shebang line | Direct execution support (`./hello.py`). |
| `if __name__ == "__main__":` guard | Allows importing `greet()` from `hello.py` in the future if needed. |

### Step 2 — Verify correctness

```bash
cd /private/tmp/test-looper
python3 hello.py                     # → "Hello from Looper!"
python3 hello.py --name Alice        # → "Hello from Alice!"
python3 hello.py --name "Bob Dole"   # → "Hello from Bob Dole!"
python3 hello.py --help              # shows help text
python3 hello.py --unknown-flag      # exits with error (non-zero)
python3 greeting.py                  # → "Hello, World!" (unchanged)
python3 greeting.py Alice            # → "Hello, Alice!" (unchanged)
python3 -c "from greeting import greet; print(greet())"  # still works
```

### Step 3 — Commit and push

```bash
git add hello.py
git commit -m "feat: hello.py with own greet() and 'Looper' default (#72)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

---

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **REPLACE** | Overwrite existing content with #72 version |
| `greeting.py` | untouched | Unchanged |

## Backward compatibility

- `greeting.py` is **completely unchanged** — `python3 greeting.py` still prints `"Hello, World!"`, `python3 greeting.py Alice` still prints `"Hello, Alice!"`.
- `hello.py` **changes behavior**: bare call now prints `"Hello from Looper!"` instead of `"Hello, World!"`. This is intentional to match issue #72's requirements.
- `from greeting import greet` continues to work for any code that imports from `greeting.py`.
