# Spec: hello.py with argparse `--name` flag (Issue #101)

Issue: #101 (quangdang46/test-looper)
Spec: specs/101-spec/spec.md

---

## Objective

Create `hello.py` at the repo root that uses `argparse` for a `--name` flag and imports `greet()` from `greeting.py` to produce the greeting string. This differs from the existing `hello.py` on `main` (landed via #72) which defines its own `greet()` — see [Background](#background).

## Background

The repository has two existing greeting scripts on `main`:

| File | Behavior | Source |
|------|----------|--------|
| `greeting.py` | `greet(name="World")` → `"Hello, {name}!"` via positional arg | Issue #37 |
| `hello.py` (current) | own `greet(name="Looper")` → `"Hello from {name}!"` via `--name` | Issue #72 |

Issue #72's `hello.py` duplicates the greeting logic by defining its own `greet()` with a different template (`"Hello from {name}!"`) and default (`"Looper"`). Issue #93 proposed an import-based approach instead, but that work landed in a worktree branch that was never merged to `main`.

Issue #101 is a fresh attempt to create `hello.py` that **reuses** `greeting.py`'s `greet()` — eliminating the code duplication while keeping the `--name` argparse interface.

## Design Decisions

| Choice | Rationale |
|--------|-----------|
| **Import `greet` from `greeting.py`** | Reuses existing `greet()` instead of defining a duplicate. The output format becomes `"Hello, {name}!"` (from `greeting.py`), not `"Hello from {name}!"` (from #72's version). |
| **`--name` default: `"World"`** | Matches `greeting.py`'s `greet()` default so bare invocation (`python3 hello.py`) matches `greeting.py`'s bare output. |
| **Replace existing `hello.py`** | The current `hello.py` is the one from #72. This spec replaces it in-place. |
| **Keep shebang and `__name__` guard** | Project convention; allows both direct execution and future imports. |
| **No changes to `greeting.py`** | The existing `greeting.py` is left completely untouched. |

## Implementation Steps

### Step 1 — Replace `hello.py`

Overwrite the existing `hello.py` at the repo root with:

```python
#!/usr/bin/env python3
"""A simple greeting script with argparse --name flag."""

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

Key differences from #72's `hello.py`:
- No own `greet()` — imports from `greeting.py`
- `--name` default is `"World"` (not `"Looper"`)
- Output format is `"Hello, {name}!"` (not `"Hello from {name}!"`)

### Step 2 — Verify correctness

Run from the repo root:

```bash
python3 hello.py                    # → "Hello, World!"
python3 hello.py --name Alice       # → "Hello, Alice!"
python3 hello.py --name "Bob Dole"  # → "Hello, Bob Dole!"
python3 hello.py --help             # shows help text
python3 hello.py --unknown-flag     # exits non-zero with error
```

### Step 3 — Commit

```bash
git add hello.py
git commit -m "feat: implement hello.py with --name flag using argparse (#101)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Files Touched

| File | Action |
|------|--------|
| `hello.py` | **REPLACE** — change import strategy and defaults |
| `greeting.py` | untouched |

## Acceptance Criteria

1. `python3 hello.py` prints `Hello, World!`
2. `python3 hello.py --name Alice` prints `Hello, Alice!`
3. `python3 hello.py --name "Bob Smith"` prints `Hello, Bob Smith!`
4. `python3 hello.py --help` prints a help message describing `--name`
5. `python3 hello.py --unknown-flag` exits non-zero with usage error
6. `greeting.py` is not modified
7. `python3 -c "from greeting import greet; print(greet())"` still works (no import chain break)

## Risks

- **Import path** — `from greeting import greet` requires running `hello.py` from the repo root (where `greeting.py` lives). Running from another directory breaks the import. Mitigated by running from repo root consistently.
- **Backward compatibility** — existing users of `hello.py` (if any) relying on `"Hello from Looper!"` format will see `"Hello, World!"` instead. Since this is a playground repo with no downstream consumers, this is acceptable.
