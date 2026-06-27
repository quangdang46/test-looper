# Spec: Implement `hello.py` with `"Hello from Looper!"` (Issue #72)

## Problem

**Issue #72** asks for a `hello.py` script that prints `"Hello from Looper!"` with an optional `--name` flag to customize the greeting.

The repository currently has:

| File | Content | Issue |
|------|---------|-------|
| `greeting.py` | `greet()` returning `"Hello, {name}!"` | #37 |
| `hello.py` | Imports `greet()` from `greeting.py`, default `--name "World"` | #93 (merged) |

The existing `hello.py` (from #93) reuses `greeting.py`'s `greet()` and outputs `"Hello, World!"`, which **does not satisfy #72's requirement** of `"Hello from Looper!"`. Since the template format differs (`"Hello from {name}!"` vs `"Hello, {name}!"`), the cleanest approach is for `hello.py` to define its own `greet()`.

## Goals

1. Overwrite `hello.py` at the repo root with a corrected implementation.
2. Use `argparse` with a `--name` flag (default: `"Looper"`).
3. Define a standalone `greet()` returning `"Hello from {name}!"` (distinct from `greeting.py`).
4. Keep `greeting.py` unchanged.
5. Support quoted names with spaces (`--name "Bob Smith"`).

## Non-goals

- No changes to `greeting.py` or its `greet()`.
- No refactoring/extraction of shared logic between the two scripts.
- No packaging / `pyproject.toml`.
- No handling for `--name` beyond what `argparse` provides natively.

## Implementation Steps

### Step 1 — Overwrite `hello.py`

Replace the existing `hello.py` (repo root) with:

```python
#!/usr/bin/env python3
"""A simple hello script using argparse — prints 'Hello from {name}!'."""

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

| Decision | Rationale |
|----------|-----------|
| Own `greet()` instead of importing from `greeting.py` | The output template `"Hello from {name}!"` is fundamentally different from `greeting.py`'s `"Hello, {name}!"`. Importing would couple the two scripts unnecessarily; keeping them independent allows each to evolve separately. |
| `--name` default `"Looper"` | Matches the bare-invocation output `"Hello from Looper!"` requested by the issue. |
| `--name` flag (not positional) | Self-documenting at the call site; standard argparse pattern for optional named arguments. |
| Shebang + `if __name__` guard | Enables direct execution (`./hello.py`) and future importability. |

### Step 2 — Verify correctness

Run from the repo root:

```bash
python3 hello.py                     # → "Hello from Looper!"
python3 hello.py --name Alice        # → "Hello from Alice!"
python3 hello.py --name "Bob Dole"   # → "Hello from Bob Dole!"
python3 hello.py --help              # shows help with --name flag
python3 hello.py --unknown           # exits non-zero, prints error
```

These five checks cover:
- Default path (no `--name` supplied)
- Simple `--name` override
- Quoted multi-word name
- Usability (help text renders)
- Error handling (argparse unknown flag → non-zero exit)

### Step 3 — Commit and push

```bash
git add hello.py
git commit -m "feat: implement hello.py with own greet(), --name default Looper (#72)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

## Files touched

| File | Action | Details |
|------|--------|---------|
| `hello.py` | **OVERWRITE** | Replace import-based impl with standalone `greet()` using `"Hello from {name}!"` template |
| `greeting.py` | untouched | No changes |

## Acceptance criteria

1. `python3 hello.py` → `Hello from Looper!`
2. `python3 hello.py --name Alice` → `Hello from Alice!`
3. `python3 hello.py --name "Bob Smith"` → `Hello from Bob Smith!`
4. `python3 hello.py --help` → exits 0, shows `--name` flag in help text
5. `python3 hello.py --unknown` → exits non-zero, prints unrecognized arguments error
6. `python3 greeting.py` still prints `Hello, World!` (untouched)

## Backward compatibility

No breaking changes. The existing `greeting.py` continues to work identically. Callers that import `greet` from `greeting.py` are unaffected. The only behavioral change is `hello.py`'s output format — any scripts/pipelines that depend on the old `"Hello, ..."` output from `hello.py` will need adjusting.
