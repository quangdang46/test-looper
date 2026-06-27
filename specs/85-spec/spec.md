# Spec: Create `hello.py` (Issue #85)

> **Status:** Issue #85 is OPEN. Requires `hello.py` that prints `"Hello from Looper!"` with an optional `--name` flag.

## Context

Issue #85 asks for a `hello.py` script that prints `"Hello from Looper!"` by default, with an optional `--name` flag to greet a specific name.

The current `hello.py` on `main` was delivered by [#93](https://github.com/quangdang46/test-looper/pull/93). It **reuses** `greeting.py`'s `greet()` function, which uses the format `"Hello, {name}!"` with default `"World"`. This does **not** match issue #85's requirements.

| Aspect | #85 requirement | Current `main` (`hello.py` from #93) |
|--------|----------------|--------------------------------------|
| `greet()` source | Own function in `hello.py` | Imports from `greeting.py` |
| Greeting format | `"Hello from {name}!"` | `"Hello, {name}!"` |
| Default `--name` | `"Looper"` | `"World"` |

## Goals

1. **Create** `hello.py` (or replace the existing one) with its **own** `greet()` function that returns `"Hello from {name}!"` and defaults to `"Looper"`.
2. Use `argparse` for CLI argument parsing with a `--name` flag.
3. Keep `greeting.py` **unchanged** — it retains its own `greet()` with the `"Hello, {name}!"` format.
4. Both scripts remain independently runnable with distinct output formats.

## Non-goals

- No changes to `greeting.py` or its `greet()` function.
- No packaging, `setup.py`, or `pyproject.toml`.
- No error handling beyond what `argparse` provides for `--name`.
- No changes to import behaviour — `from greeting import greet` continues to work.
- No changes to CI/CD, tests, or documentation beyond this one file.

---

## Implementation Steps

### Step 1 — Write `hello.py`

Overwrite the existing file at `hello.py` (repo root) with the #85-specified version.

**Structure:**

```python
#!/usr/bin/env python3
"""A simple hello script with argparse --name flag."""

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
| Own `greet()` (not importing from `greeting.py`) | Issue #85 specifies `"Hello from {name}!"`, which is deliberately different from `greeting.py`'s `"Hello, {name}!"`. |
| `default="Looper"` | Matches the issue description: bare invocation must print `"Hello from Looper!"`. |
| `--name` flag (not positional) | Self-documenting; consistent with the existing `hello.py` convention. |
| Shebang line | Direct execution support (`./hello.py`). |
| `if __name__ == "__main__":` guard | Allows importing `greet()` from `hello.py` in the future if needed. |

### Step 2 — Verify correctness

```bash
python3 hello.py                     # → "Hello from Looper!"
python3 hello.py --name Alice        # → "Hello from Alice!"
python3 hello.py --name "Bob Smith"  # → "Hello from Bob Smith!"
python3 hello.py --help              # shows help text
python3 hello.py --unknown-flag      # exits with error (non-zero)
python3 greeting.py                  # → "Hello, World!" (unchanged)
python3 greeting.py Alice            # → "Hello, Alice!" (unchanged)
python3 -c "from greeting import greet; print(greet())"  # still works
```

### Step 3 — Commit and push

```bash
git add hello.py
git commit -m "feat: hello.py with own greet() and 'Looper' default (#85)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

---

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **REPLACE** | Overwrite existing content with #85 version (own `greet()`, `"Hello from {name}!"`, default `"Looper"`) |
| `greeting.py` | untouched | Unchanged |

## Backward compatibility

- `greeting.py` is **completely unchanged** — `python3 greeting.py` still prints `"Hello, World!"`.
- `hello.py` **changes behaviour**: bare call now prints `"Hello from Looper!"` instead of `"Hello, World!"`. This is intentional to match issue #85's requirements.
- `from greeting import greet` continues to work for any code that imports from `greeting.py`.
