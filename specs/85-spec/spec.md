# Spec: Add `hello.py` with `"Hello from Looper!"` greeting (Issue #85)

## Problem

**Issue #85** asks to `Create hello.py that prints "Hello from Looper!" with optional --name flag.`

The current `hello.py` on `main` (merged via #93) imports `greet()` from `greeting.py`, which returns `"Hello, {name}!"`. However, issue #85 specifies the **"Hello from"** template — `"Hello from Looper!"` / `"Hello from {name}!"` — which is a different format from `greeting.py`'s `"Hello, {name}!"`.

Two things must change to satisfy the issue:
1. **Default** — bare invocation must print `"Hello from Looper!"` (not `"Hello, World!"`)
2. **Template** — `--name Alice` must print `"Hello from Alice!"` (not `"Hello, Alice!"`)

## Goals

1. Modify `hello.py` so it prints `"Hello from Looper!"` when called with no arguments.
2. Keep the `--name` flag via `argparse`; `--name <value>` prints `"Hello from <value>!"`.
3. Default for `--name` must be `"Looper"` so bare invocation matches the issue description.
4. Keep `greeting.py` completely unchanged — no modifications to its `greet()` or `main()`.

## Non-goals

- No changes to `greeting.py` or its import chain.
- No packaging / `setup.py` / `pyproject.toml`.
- No new files; all changes stay inside `hello.py`.
- No refactoring of `greeting.py`'s `main()` or `greet()`.

---

## Implementation Steps

### Step 1 — Modify `hello.py`

The current file at the repository root (`hello.py`) reuses `greeting.py`'s `greet()` via `from greeting import greet`. Replace that import with a locally-defined `greet()` that produces the `"Hello from {name}!"` template, and change the argparse default from `"World"` to `"Looper"`.

**Before (current state from #93):**

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

**After (issue #85):**

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

**Changes summarized:**

| Change | From | To |
|--------|------|----|
| Import | `from greeting import greet` | _removed_ (no import needed) |
| `greet()` source | external (`greeting.py`) | local in `hello.py` |
| Template | `"Hello, {name}!"` | `"Hello from {name}!"` |
| Default `--name` | `"World"` | `"Looper"` |

**Rationale:**

- **Local `greet()` instead of import** — the `"Hello from"` template doesn't exist in `greeting.py`, so importing is no longer useful. A local function keeps `hello.py` self-contained and `greeting.py` unchanged.
- **Default `"Looper"`** — matches the issue description verbatim: "prints 'Hello from Looper!'".

### Step 2 — Verify correctness

Run from the repository root:

```bash
python3 hello.py                        # → "Hello from Looper!"
python3 hello.py --name Alice           # → "Hello from Alice!"
python3 hello.py --name "Bob Dole"      # → "Hello from Bob Dole!"
python3 hello.py --help                 # shows help text
python3 hello.py --unknown-flag         # exits non-zero, prints error
```

| Test | Expected output | What it validates |
|------|----------------|-------------------|
| bare call | `Hello from Looper!` | default value |
| `--name Alice` | `Hello from Alice!` | flag override |
| `--name "Bob Dole"` | `Hello from Bob Dole!` | quoted multi-word names |
| `--help` | argparse help text | usage doc |
| `--unknown-flag` | error + exit != 0 | flag validation |

Also confirm `greeting.py` is untouched:

```bash
python3 greeting.py                    # → "Hello, World!"  (unchanged)
python3 greeting.py Alice              # → "Hello, Alice!"  (unchanged)
python3 -c "from greeting import greet; print(greet())"  # → "Hello, World!"
```

### Step 3 — Commit

```bash
git add hello.py
git commit -m "feat: update hello.py with 'Hello from Looper' format (#85)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

The commit message follows the repo's existing convention (`feat:` prefix, issue reference in parens, Claude co-author trailer).

---

## Files touched

| File | Action |
|------|--------|
| `hello.py` | **MODIFY** — replace import with local `greet()`, change template and default |
| `greeting.py` | untouched |

## Acceptance Criteria

1. `python3 hello.py` prints `Hello from Looper!`
2. `python3 hello.py --name Alice` prints `Hello from Alice!`
3. `python3 hello.py --name "Bob Smith"` prints `Hello from Bob Smith!`
4. `python3 hello.py --help` prints a help message describing `--name`
5. `python3 hello.py --unknown-flag` exits non-zero
6. `greeting.py` is not modified; `python3 greeting.py` still prints `Hello, World!`
7. `python3 -c "from greeting import greet; print(greet())"` still works

## Backward compatibility

The change from `"Hello, World!"` to `"Hello from Looper!"` is a deliberate break per the issue requirements. `greeting.py` remains a stable library — any consumer importing `greet()` from `greeting.py` sees zero change.
