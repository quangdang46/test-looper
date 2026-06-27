# Spec: Add `hello.py` printing `"Hello from Looper!"` (Issue #85)

## Problem

**Issue #85** asks for a `hello.py` script that prints `"Hello from Looper!"` with an optional `--name` flag to customize the greeting. The repository already has:

- `greeting.py` (PR #37) with `greet(name: str = "World") -> str` returning `"Hello, {name}!"`
- `hello.py` already on `main` (PR #93) that imports `greet()` from `greeting.py` and prints `"Hello, World!"` by default

The issue's desired output format is `"Hello from {name}!"`, which is **incompatible** with `greeting.py`'s `"Hello, {name}!"` template. Simply importing `greeting.py`'s `greet()` and passing a different default cannot produce the required template.

Additionally, 6 prior implementation attempts on worker branches exist but none ever landed on `main`.

## Background

A previous issue (#93) added `hello.py` to `main` that reuses `greeting.py`'s `greet()`. Issue #72 attempted a standalone `hello.py` with its own `greet()` but was superseded by #93. Issue #85 is a new request with a distinct template requirement (`"Hello from {name}!"`) — conceptually closer to the #72 approach than the #93 approach.

## Goals

1. Modify `hello.py` to print `"Hello from Looper!"` (instead of current `"Hello, World!"`).
2. Keep `--name` flag support via `argparse`.
3. Use a custom `greet()` function with the `"Hello from {name}!"` format — not importing from `greeting.py`.
4. Default value for `--name` must be `"Looper"` (so bare invocation prints `"Hello from Looper!"`).
5. Keep `greeting.py` unchanged.
6. Preserve all existing files' structure — no refactoring.

## Non-goals

- No changes to `greeting.py` or its `greet()` function signature.
- No changes to `greeting.py`'s `main()` or CLI behavior.
- No packaging / setup.py / pyproject.toml.
- No modifications to other existing scripts or test infrastructure.

---

## Implementation Steps

### Step 1 — Replace `hello.py` content

Modify `hello.py` at the repo root. The current version imports `greet()` from `greeting.py` and uses default `"World"`. The new version defines its own `greet()` with the `"Hello from {name}!"` template.

**New `hello.py`:**

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

**Rationale for key changes:**

| Change | Reason |
|--------|--------|
| Own `greet()` (not importing from `greeting.py`) | The issue requires `"Hello from {name}!"` format, which `greeting.py`'s `"Hello, {name}!"` cannot produce. A standalone function avoids coupling the two scripts against a cosmetic template difference. |
| `default="Looper"` | Matches the issue's explicit example output `"Hello from Looper!"`. |
| Default type hint for `greet()` | `greet(name: str = "Looper")` makes the default clear at a glance and consistent with `greeting.py`'s pattern. |

### Step 2 — Verify correctness

After writing the file, validate:

```bash
cd /private/tmp/test-looper
python3 hello.py                    # → "Hello from Looper!"
python3 hello.py --name Alice       # → "Hello from Alice!"
python3 hello.py --name "Bob Dole"  # → "Hello from Bob Dole!"
python3 hello.py --help             # shows help text
python3 hello.py --bogus            # exits non-zero with error
```

Also verify no regressions:

```bash
python3 greeting.py                    # → "Hello, World!" (unchanged)
python3 greeting.py Alice              # → "Hello, Alice!" (unchanged)
python3 -c "from greeting import greet; print(greet())"  # → "Hello, World!"
```

### Step 3 — Commit and push

Working from the repo root:

```bash
git add hello.py
git commit -m "feat: implement add hello.py (#85)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

---

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **MODIFY** — replace `greeting.py` import with own `greet()`, change default to `"Looper"` | Output template changes from `"Hello, {name}!"` to `"Hello from {name}!"` |
| `greeting.py` | untouched | No changes to shared library |

## Backward compatibility

- `greeting.py` is completely unchanged — `python3 greeting.py` still prints `"Hello, World!"`, all imports work.
- `hello.py` **changes output format**: `python3 hello.py` was `"Hello, World!"` → now `"Hello from Looper!"`.
- Any test or script that checks `hello.py` output literally will need a new golden value.
- The `--name` flag interface is preserved; only the default value and output template change.
