# Spec: Implement `hello.py` with `--name` flag using argparse (Issue #101)

**Issue:** #101 — `hello.py` with `--name` flag using argparse.
**Labels:** `dispatch/implement`, `looper/planned`, `looper:implement`, `looper:plan`

---

## Problem

The repo already has two Python scripts at the root:

1. **`greeting.py`** (issue #37) — defines `greet(name: str = "World") -> str` returning `"Hello, {name}!"`.
2. **`hello.py`** (issue #72) — defines its **own** `greet(name: str = "Looper") -> str` returning `"Hello from {name}!"`, plus `argparse` `--name` support.

Issue #101 asks for a `hello.py` that uses `argparse --name` but **reuses the existing `greet()` from `greeting.py`** rather than duplicating the greeting logic. This eliminates the code duplication introduced in #72 and ensures a single canonical greeting function.

## Goals

1. Modify `hello.py` to **import `greet()` from `greeting.py`** instead of defining its own.
2. Keep `argparse --name` support (already present in `hello.py`).
3. Change the argparse default from `"Looper"` to `"World"` to match `greeting.py`'s `greet()` default.
4. Output format changes from `"Hello from {name}!"` to `"Hello, {name}!"` (the `greeting.py` template), so `python3 hello.py` and `python3 greeting.py` produce identical output for the same name.
5. Leave `greeting.py` completely unchanged.
6. Preserve all existing test/verification infrastructure.

## Non-goals

- No changes to `greeting.py` or its `main()` / CLI behavior.
- No packaging or `pyproject.toml`.
- No new test files — verification is done manually via shell commands.

## Implementation Steps

### Step 1 — Update `hello.py`

Replace the current `hello.py` with a version that imports `greet()` from `greeting.py`.

**New `hello.py`:**

```python
#!/usr/bin/env python3
"""A simple hello script with argparse support."""

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

**Key changes from the current `hello.py` (issue #72):**

| Aspect | Before (#72) | After (#101) | Rationale |
|--------|-------------|--------------|-----------|
| `greet()` source | Defined locally | Imported from `greeting.py` | Eliminates code duplication; single source of truth for greeting logic |
| Default name | `"Looper"` | `"World"` | Matches `greeting.py`'s `greet()` default |
| Output template | `"Hello from {name}!"` | `"Hello, {name}!"` | Inherited from `greeting.py`'s `greet()` |
| `--name` flag | Supported | Supported | Unchanged |
| `main()` guard | Present | Present | Unchanged |
| Shebang | `#!/usr/bin/env python3` | `#!/usr/bin/env python3` | Unchanged |

### Step 2 — Verify correctness

Run the following validation commands from the repo root:

```bash
cd /private/tmp/test-looper
python3 hello.py                      # → "Hello, World!"
python3 hello.py --name Alice         # → "Hello, Alice!"
python3 hello.py --name "Bob Smith"   # → "Hello, Bob Smith!"
python3 hello.py --help               # shows help with --name flag
python3 hello.py --unknown-flag       # exits non-zero, prints error
python3 greeting.py                   # → "Hello, World!" (unchanged)
python3 greeting.py Alice             # → "Hello, Alice!" (unchanged)
python3 -c "from greeting import greet; print(greet())"  # → "Hello, World!"
```

### Step 3 — Commit

```bash
git add hello.py
git commit -m "feat: hello.py with argparse --name flag, reusing greet() from greeting.py (#101)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

The commit message follows the repo convention: `feat:` prefix, reference `(#101)`, and the Claude co-author trailer.

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **MODIFY** | Replace own `greet()` with `from greeting import greet`; change default to `"World"` |
| `greeting.py` | untouched | Not modified |

## Backward compatibility

- `greeting.py` works exactly as before — `python3 greeting.py` prints `"Hello, World!"`, `python3 greeting.py Alice` prints `"Hello, Alice!"`.
- `python3 -c "from greeting import greet; print(greet())"` still works (no import chain broken).
- The behavioral difference from the #72 version: `hello.py` now produces `"Hello, World!"` instead of `"Hello from Looper!"` when called without arguments.
