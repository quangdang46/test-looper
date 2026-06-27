# Spec: Create `hello.py` with `--name` via argparse (Issue #101)

Issue: #101
Labels: `dispatch/implement`, `looper/planned`, `looper:implement`

---

## Objective

Create `hello.py` at the repo root that uses Python's `argparse` module to accept a `--name` flag and prints a greeting. The script reuses the existing `greet()` function from `greeting.py` rather than duplicating greeting logic, and uses argparse instead of `greeting.py`'s current `sys.argv`-based parsing.

## Background

The repo already contains two greeting scripts:

| Script | Parsing method | greet() source | Default | Output format |
|--------|---------------|----------------|---------|--------------|
| `greeting.py` | `sys.argv` | Own | `"World"` | `Hello, {name}!` |
| `hello.py` (from #72, now on main) | argparse `--name` | Own | `"Looper"` | `Hello from {name}!` |

Issue #101 asks simply to **"Create hello.py with --name flag using argparse."** The previously merged `hello.py` (#72) already provides this, but it uses a different greeting format (`"Hello from"` with default `"Looper"`) and duplicates the `greet()` function from `greeting.py`.

This spec proposes a cleaner approach: **import `greet()` from `greeting.py`** and wrap it with argparse. This avoids function duplication and standardizes on the existing `"Hello, {name}!"` format, making `hello.py` a pure CLI wrapper over the library function.

## Goals

1. Create/replace `hello.py` with a clean argparse-based script.
2. Import `greet()` from `greeting.py` — no duplicate `greet()` definition.
3. `--name` flag with argparse, default `"World"` (matching `greeting.py`'s default).
4. `main()` function guarded by `if __name__ == "__main__":`.
5. `#!/usr/bin/env python3` shebang for direct execution.
6. All existing files (`greeting.py`) remain unchanged.

## Non-goals

- No changes to `greeting.py` or its `greet()` signature.
- No packaging / `setup.py` / `pyproject.toml`.
- No extra features beyond `--name` (no `--count`, no file output, etc.).

## Implementation Steps

### Step 1 — Create `hello.py`

Write a new file at the repo root, `hello.py`:

```python
#!/usr/bin/env python3
"""A simple hello script using argparse with greeting from greeting.py."""

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

**Key decisions:**

| Decision | Rationale |
|----------|-----------|
| Import `greet` from `greeting.py` | Avoids duplicating the `greet()` logic; keeps the greeting template in one place. The issue does not specify a custom output format. |
| Default `"World"` | Matches `greeting.py`'s `greet(name="World")` default, so bare `python3 hello.py` and `python3 greeting.py` produce the same output. |
| `--name` (not positional) | Following what #72 established; self-documenting at the CLI. |
| Shebang line | Direct execution (`./hello.py`) for local testing. |
| `if __name__ == "__main__"` guard | Allows `main()` to be imported in tests if needed, standard Python practice. |

### Step 2 — Verify correctness

Run from the repo root:

```bash
cd /private/tmp/test-looper

# Default invocation (matches greeting.py's default)
python3 hello.py                     # → "Hello, World!"

# Named invocations
python3 hello.py --name Alice        # → "Hello, Alice!"
python3 hello.py --name "Bob Smith"  # → "Hello, Bob Smith!"

# Help
python3 hello.py --help              # shows argparse help with --name flag

# Error on unknown flag
python3 hello.py --unknown-flag      # → exits non-zero, prints error

# greeting.py still works
python3 greeting.py                  # → "Hello, World!"
python3 greeting.py Alice            # → "Hello, Alice!"
python3 -c "from greeting import greet; print(greet())"  # → "Hello, World!"
```

### Step 3 — Commit

```bash
cd /private/tmp/test-looper
git add hello.py
git commit -m "feat: create hello.py with argparse --name flag (#101)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

*Note:* If `hello.py` already exists in the working tree (from previous merged work #72), the `git add` will stage the updated content — the commit message still references the correct issue.

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **CREATE** (or replace) | Imports `greet` from `greeting.py`; wraps with argparse `--name`; at repo root. |
| `greeting.py` | untouched | Unchanged. |

## Acceptance criteria

1. `python3 hello.py` prints `Hello, World!`
2. `python3 hello.py --name Alice` prints `Hello, Alice!`
3. `python3 hello.py --name "Bob Smith"` prints `Hello, Bob Smith!`
4. `python3 hello.py --help` prints a help message describing `--name`
5. `python3 hello.py --unknown-flag` exits non-zero with an error
6. `greeting.py` is not modified
7. `python3 greeting.py` still prints `Hello, World!`
8. `python3 -c "from greeting import greet; print(greet())"` still works

## Risks

- **Import path:** `from greeting import greet` requires running from the repo root (where `greeting.py` lives). Running from another directory will fail with `ModuleNotFoundError`. Document this in the script's docstring.
- **Existing hello.py:** If the previous `hello.py` (from #72) is present, it will be overwritten. Its custom `"Hello from"` format will be lost — confirm this is acceptable.
- **Default value mismatch:** The argparse default (`"World"`) must match `greeting.py`'s `greet()` default so bare-call behavior is consistent.
