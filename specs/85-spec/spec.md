# Spec: Add `hello.py` (Issue #85)

Issue: #85
Spec: `specs/85-spec/spec.md`

---

## Objective

Create a `hello.py` script at the repo root that prints `"Hello from Looper!"` and accepts an optional `--name` flag to customise the greeting message.

## Background

The repository already has `greeting.py` (issue #37) with its own `greet()` function returning `"Hello, {name}!"`. Issue #85 asks for a new `hello.py` that prints `"Hello from {name}!"` — a deliberately different output format. Because the template string differs (`from {name}` vs `, {name}`), `hello.py` defines its own `greet()` rather than importing from `greeting.py`, keeping the two scripts fully independent.

The actual `hello.py` was created in issue #72 and is already present on `main` with all the required functionality. This spec documents the requirements and verifies the existing implementation is correct.

## Requirements

1. `hello.py` exists as an executable Python script at the repo root (`/private/tmp/test-looper/hello.py`).
2. Uses `argparse` for CLI argument parsing with a `--name` flag.
3. Prints `"Hello from {name}!"` where `{name}` defaults to `"Looper"`.
4. Running bare (`python3 hello.py`) prints `"Hello from Looper!"`.
5. Running with `--name Alice` prints `"Hello from Alice!"`.
6. `greeting.py` is left unchanged — no refactoring or shared imports.

## Non-goals

- No changes to `greeting.py` or any existing files.
- No packaging / `setup.py` / `pyproject.toml`.
- No error handling beyond what `argparse` provides for `--name`.
- No tests or CI pipeline additions.

## Implementation Steps

### Step 1 — Verify `hello.py` exists and is correctly placed

The file must live at the repo root (`/private/tmp/test-looper/hello.py`), **not** inside `.looper/worktrees/` or any other subdirectory.

```bash
test -f /private/tmp/test-looper/hello.py && echo "EXISTS" || echo "MISSING"
```

### Step 2 — Verify the script structure

The `hello.py` file should contain:

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

Key design decisions:

| Choice | Rationale |
|--------|-----------|
| Own `greet()`, not importing from `greeting.py` | The output format `"Hello from {name}!"` differs from `greeting.py`'s `"Hello, {name}!"`. Keeping them independent prevents coupling on a cosmetic template choice. |
| `default="Looper"` | Matches the bare-invocation output `"Hello from Looper!"`. |
| `--name` as a flag (not positional) | More self-documenting and consistent with common `argparse` patterns for optional string inputs. |
| Shebang line | Makes the file directly executable (`./hello.py`). |
| `if __name__ == "__main__":` guard | Allows `greet()` to be imported from `hello.py` in the future if needed. |

### Step 3 — Verify correctness

Run the following assertions:

```bash
# Default invocation
python3 hello.py
# Expected: "Hello from Looper!"

# Custom name
python3 hello.py --name Alice
# Expected: "Hello from Alice!"

# Multi-word quoted name
python3 hello.py --name "Bob Dole"
# Expected: "Hello from Bob Dole!"

# Help flag
python3 hello.py --help
# Expected: shows usage line, --name description, and default value

# Unknown flag → non-zero exit
python3 hello.py --unknown-flag 2>&1
# Expected: prints error and exits with code 2
```

### Step 4 — Verify `greeting.py` is untouched

```bash
python3 greeting.py
# Expected: "Hello, World!"

python3 greeting.py Alice
# Expected: "Hello, Alice!"

python3 -c "from greeting import greet; print(greet())"
# Expected: "Hello, World!"
```

### Step 5 — Commit (if newly created)

If creating the file from scratch:

```bash
git add hello.py
git commit -m "feat: add hello.py with argparse --name support (#85)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

The commit message follows repo conventions: `feat:` prefix, parenthetical issue reference `(#85)`, and the Claude co-author trailer.

## Files touched

| File | Action |
|------|--------|
| `hello.py` | **CREATE** at repo root — executable Python script with shebang |
| `greeting.py` | untouched |

## Implementation status

`hello.py` already exists on `main` with the correct functionality (landed via issues #72 / #93). This spec serves as the canonical planning document for issue #85; no additional code changes are needed — only verification and closure.

## Acceptance criteria

1. `python3 hello.py` outputs `Hello from Looper!`
2. `python3 hello.py --name Alice` outputs `Hello from Alice!`
3. `python3 hello.py --name "Bob Smith"` outputs `Hello from Bob Smith!`
4. `python3 hello.py --help` shows help text describing the `--name` flag
5. `python3 hello.py --unknown-flag` exits non-zero with an error message
6. `greeting.py` is unchanged — `python3 greeting.py` still prints `Hello, World!`
7. `python3 -c "from greeting import greet; print(greet())"` still works
