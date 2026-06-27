# Spec: Add `hello.py` with `"Hello from Looper!"` output (Issue #85)

## Problem

**Issue #85** asks for a `hello.py` script at the repo root that prints `"Hello from Looper!"` and accepts an optional `--name` flag to customize the greeting.

The repo already has `greeting.py` (PR #37) whose `greet()` returns `"Hello, {name}!"` — a different template string. The issue's example output uses `"Hello from Looper!"`, which means the greeting format is `"Hello from {name}!"` rather than `"Hello, {name}!"`. Since the template differs, `hello.py` will define its own `greet()` function rather than importing from `greeting.py`.

Note: Previous attempts (#72 and #93) landed `hello.py` on `main` with different defaults/import strategies. This issue supersedes those efforts with the correct template and default.

## Goals

1. Maintain the existing `hello.py` at the repo root (modify it in-place).
2. Use `argparse` for CLI argument parsing with a `--name` flag.
3. Define a `greet()` function with `"Hello from {name}!"` format (distinct from `greeting.py`'s `"Hello, {name}!"`).
4. Default value for `--name` shall be `"Looper"` — bare invocation must print `"Hello from Looper!"`.
5. Keep `greeting.py` unchanged.

## Non-goals

- No changes to `greeting.py` or its test infrastructure.
- No packaging / `setup.py` / `pyproject.toml` — both scripts run as `python3 hello.py`.
- No error handling beyond what `argparse` provides for `--name`.

---

## Implementation Steps

### Step 1 — Modify `hello.py`

Replace the contents of `hello.py` at the repo root.

**Current state (from issue #93):**

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

**Desired state:**

```python
#!/usr/bin/env python3
"""A simple hello script using argparse."""

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

**Key changes from the current file:**

| What | Why |
|------|-----|
| Remove `from greeting import greet` | The issue uses `"Hello from {name}!"` format, which differs from `greeting.py`'s `"Hello, {name}!"`. Owning `greet()` decouples the two scripts. |
| Add local `greet(name="Looper") -> str` | Returns `f"Hello from {name}!"`. Default `"Looper"` matches the issue's example output. |
| Change argparse default from `"World"` to `"Looper"` | Must match `greet()`'s default so the bare call and `--name Looper` produce identical output. |

**Rationale for keeping the rest:**

| Aspect | Reason |
|--------|--------|
| Shebang line | Makes the file directly executable (`./hello.py`) for local testing. |
| `__name__ == "__main__"` guard | Allows `greet()` to be imported from `hello.py` in the future if needed. |
| `argparse.ArgumentParser` | Consistent with the existing pattern; self-documenting. |
| `--name` flag (not positional) | Flags are more self-documenting and consistent with common argparse patterns. |

### Step 2 — Verify correctness

After modifying `hello.py`, validate:

```bash
cd /private/tmp/test-looper
python3 hello.py                    # → "Hello from Looper!"
python3 hello.py --name Alice       # → "Hello from Alice!"
python3 hello.py --name "Bob Dole"  # → "Hello from Bob Dole!"
python3 hello.py --help             # shows help text with --name flag described
python3 hello.py --unknown-flag     # exits non-zero with error message
```

The first three assertions each check one path through the single branch point (`name` defaulted vs overridden). The `--help` test is a usability check. The `--unknown-flag` test confirms argparse rejects unknown arguments (exits non-zero).

### Step 3 — Commit and push

Working from the repo root:

```bash
git add hello.py
git commit -m "feat: hello.py with custom greet() returning 'Hello from {name}!' (#85)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

The commit message follows the repo's existing convention (see `6afb126` and `48ed356`): start with `feat:`, reference the issue with `(#85)`, and include the Claude co-author trailer.

---

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **MODIFY** | Replace `greeting.py` import with own `greet()` that returns `"Hello from {name}!"`; change default from `"World"` to `"Looper"`. |
| `greeting.py` | untouched | No changes needed. |

## Backward compatibility

This change replaces the current `hello.py` behavior (printing `"Hello, World!"` / `"Hello, Alice!"`) with the new format (`"Hello from Looper!"` / `"Hello from Alice!"`). Since `hello.py` is a new script that has not been stabilized for external consumers, this is acceptable and intentional per the issue.

`greeting.py` works exactly as before — `python3 greeting.py` still prints `"Hello, World!"`, `python3 greeting.py Alice` prints `"Hello, Alice!"`.
