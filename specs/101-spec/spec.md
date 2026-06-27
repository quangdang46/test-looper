# Spec: hello.py with `--name` flag using argparse (Issue #101)

## Problem

**Issue #101** asks to create a `hello.py` script with an `--name` flag using Python's `argparse` module.

## Current State

`hello.py` already exists on `main` (committed via PR #93, `6afb126`). It:
- Uses `#!/usr/bin/env python3` shebang
- Imports `greet()` from `greeting.py`
- Parses `--name` via `argparse` with a default of `"World"`
- Prints the result of `greet(args.name)` → `"Hello, {name}!"`

The existing implementation on `main` satisfies the literal requirements of issue #101 ("Create hello.py with --name flag using argparse").

## Goals

1. Verify that the existing `hello.py` on `main` satisfies issue #101's requirements.
2. If it does, confirm the issue can be closed with the current state.
3. If not (e.g., a different greeting format is expected), make the necessary changes.

## Non-goals

- No changes to `greeting.py`.
- No packaging / `setup.py` / `pyproject.toml`.

## Verification

Run the following from the repo root and confirm all outputs match:

```bash
python3 hello.py                  # → "Hello, World!"
python3 hello.py --name Alice     # → "Hello, Alice!"
python3 hello.py --name "Bob"     # → "Hello, Bob!"
python3 hello.py --help           # shows help describing --name
python3 hello.py --bogus          # exits non-zero with error
```

These cover:
- Default behavior (`--name` not provided → argparse default `"World"` used)
- Named override (short string, one word)
- Named override (quoted multi-word string)
- Help text rendering
- Error on unknown flags (argparse handles this automatically)

---

## Implementation Steps

### Step 1 — Check if changes are needed

Run the verification block above. If all commands produce the expected output, the existing implementation on `main` already satisfies issue #101. Proceed to Step 3 (close the issue).

If the output format or behavior differs from what the issue expects, proceed to Step 2.

### Step 2 — Update `hello.py` (if needed)

If the greeting format or argparse behavior needs adjustment, edit `hello.py` accordingly from the repo root.

**Structure (current, already matches requirements):**

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

**Key design choices (already in place):**

| Choice | Reason |
|--------|--------|
| `--name` flag (not positional) | Self-documenting, standard argparse pattern |
| `default="World"` | Matches `greeting.py`'s `greet()` default |
| Imports `greet` from `greeting.py` | Reuses existing library function; avoids duplicating greeting logic |
| `if __name__ == "__main__":` guard | Follows Python best practices for script + importable module |
| shebang line | File is directly executable |

### Step 3 — Confirm and close

Once verification passes against `main`, issue #101 can be closed as already implemented (landed via PR #93).

---

## Files touched

| File | Action |
|------|--------|
| `hello.py` | **Already exists** on `main` — verify only, no changes needed |
| `greeting.py` | **Untouched** |

## Backward compatibility

No breaking changes. `greeting.py` works exactly as before. `hello.py` already works on `main`.
