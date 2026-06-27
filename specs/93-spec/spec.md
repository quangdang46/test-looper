# Spec: Implement `hello.py` with `--name` flag (Issue #93)

## Problem

**Issue #93** asks to create `hello.py` with a `--name` flag. The repository already has `greeting.py` (PR #37) with a `greet()` function returning `"Hello, {name}!"`. Rather than duplicating the greeting logic, `hello.py` should import `greet()` from `greeting.py` and wrap it in an argparse-based CLI.

## Goals

1. Create `hello.py` at the repo root (if not present) that uses `argparse` for CLI argument parsing.
2. Provide a `--name` flag (default: `"World"`).
3. Reuse `greet()` from `greeting.py` — do not define a standalone `greet()` in `hello.py`.
4. Keep `greeting.py` unchanged.

## Non-goals

- No changes to `greeting.py` or its test infrastructure.
- No packaging / `setup.py` / `pyproject.toml` — both scripts run as `python3 hello.py`.
- No error handling beyond what `argparse` provides for `--name`.

---

## Implementation Steps

### Step 1 — Create `hello.py`

Create a new file `hello.py` at the repo root (alongside `greeting.py`).

**Structure:**

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

**Rationale for key choices:**

| Choice | Reason |
|--------|--------|
| Import `greet()` from `greeting.py` | The template format `"Hello, {name}!"` from `greeting.py` satisfies the issue. Reusing the function avoids code duplication and keeps a single source of truth for the greeting logic. |
| `default="World"` | Matches `greeting.py`'s `greet()` default; bare `python3 hello.py` prints `"Hello, World!"`. |
| `--name` flag (not positional) | Flags are more self-documenting and align with common argparse CLI patterns. |
| shebang line | Makes the file directly executable (`./hello.py`) for local testing. |
| `__name__ == "__main__"` guard | Standard Python idiom; keeps `main()` from running on import. |

### Step 2 — Verify correctness

After writing the file, validate from the repo root:

```bash
cd /private/tmp/test-looper
python3 hello.py                       # → "Hello, World!"
python3 hello.py --name Looper         # → "Hello, Looper!"
python3 hello.py --name Alice          # → "Hello, Alice!"
python3 hello.py --name "Bob Dole"     # → "Hello, Bob Dole!"
python3 hello.py --help                # shows help text
python3 hello.py --unknown-flag        # exits non-zero with error
```

The first four assertions each exercise the single branch point (`name` defaulted vs overridden, with a multi-word name variant). The `--help` check verifies argparse produces its expected usage output. The `--unknown-flag` test confirms argparse exits with a non-zero exit code on invalid input.

### Step 3 — Commit and push

```bash
git add hello.py
git commit -m "feat: hello.py with argparse --name flag, reusing greet() from greeting.py (#93)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

The commit message follows the repo's existing convention: start with `feat:`, reference the issue with `(#93)`, and include the Claude co-author trailer.

---

## Files touched

| File | Action | Detail |
|------|--------|--------|
| `hello.py` | **CREATE** | Executable Python script with shebang, argparse, and import from `greeting.py` |
| `greeting.py` | untouched | No changes needed |

## Backward compatibility

No breaking changes. `greeting.py` works exactly as before — `python3 greeting.py` still prints `"Hello, World!"`. `hello.py` is a new addition that depends on `greeting.py`'s public `greet()` API.
