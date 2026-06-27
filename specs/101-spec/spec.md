# Spec: Implement `hello.py` (Issue #101)

> **Status:** Issue #101 is OPEN. Reconciles the requirements of issue #72 (original ask for `hello.py`) with the current on-`main` implementation from #93 (which imported from `greeting.py`). This spec replaces the #93-style `hello.py` with the #72/#101-intended version.

---

## Problem

Issue #101 requests a `hello.py` script with a `--name` flag using Python's `argparse` module. A prior implementation (#93) landed such a script on `main`, but it **reuses** `greeting.py`'s `greet()` function — meaning bare invocations print `"Hello, World!"` rather than `"Hello from Looper!"` as originally intended by #72 (which #101 supersedes).

| Aspect | #93 implementation (current `main`) | #101 requirement |
|--------|--------------------------------------|------------------|
| `greet()` source | Imports from `greeting.py` | Own function in `hello.py` |
| Greeting format | `"Hello, {name}!"` | `"Hello from {name}!"` |
| Default `--name` | `"World"` | `"Looper"` |

The two scripts (`hello.py` vs `greeting.py`) are deliberately distinct formats — they serve as independent examples, not duplicates.

## Goals

1. **Replace** the current `hello.py` with the #101-required version (own `greet()`, `"Hello from {name}!"`, default `"Looper"`).
2. Use `argparse` for CLI argument parsing with a `--name` flag.
3. Keep `greeting.py` **completely unchanged** — it retains its own `greet()` with `"Hello, {name}!"` format.
4. Both scripts remain independently runnable with distinct output formats.

## Non-goals

- No changes to `greeting.py` or its `greet()` function.
- No packaging / `setup.py` / `pyproject.toml`.
- No error handling beyond what `argparse` provides for `--name`.
- No changes to the `greeting.py` import — `from greeting import greet` continues to work.

---

## Implementation Steps

### Step 1 — Replace `hello.py`

Overwrite the existing `hello.py` at the repo root.

**Content:**

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
| Own `greet()` (not importing from `greeting.py`) | Issue #101 / #72 specifies `"Hello from {name}!"`, which differs from `greeting.py`'s `"Hello, {name}!"`. These are deliberately distinct formats. |
| `default="Looper"` | Matches the issue requirement: bare invocation must print `"Hello from Looper!"`. |
| `--name` flag (not positional) | Self-documenting; consistent with the prior #93 implementation's convention. |
| Shebang line | Direct execution support (`./hello.py`). |
| `if __name__ == "__main__":` guard | Allows importing `greet()` from `hello.py` in the future if needed. |

### Step 2 — Verify correctness

```bash
python3 hello.py                     # → "Hello from Looper!"
python3 hello.py --name Alice        # → "Hello from Alice!"
python3 hello.py --name "Bob Dole"   # → "Hello from Bob Dole!"
python3 hello.py --help              # shows help text
python3 hello.py --unknown-flag      # exits with error (non-zero)
python3 greeting.py                  # → "Hello, World!" (unchanged)
python3 greeting.py Alice            # → "Hello, Alice!" (unchanged)
python3 -c "from greeting import greet; print(greet())"  # still works
```

### Step 3 — Commit

```bash
git add hello.py
git commit -m "feat: hello.py with own greet() and 'Looper' default (#101)
Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **REPLACE** | Overwrite existing content with #101 version |
| `greeting.py` | untouched | Unchanged |

## Backward compatibility

- `greeting.py` is **completely unchanged** — `python3 greeting.py` still prints `"Hello, World!"`, `python3 greeting.py Alice` still prints `"Hello, Alice!"`.
- `hello.py` **changes behavior**: bare call now prints `"Hello from Looper!"` instead of `"Hello, World!"`. This is intentional to match issue #101's requirements.
- `from greeting import greet` continues to work for any code that imports from `greeting.py`.
