# Spec: Implement `hello.py` (Issue #72)

## Problem

**Issue #72** asks for a `hello.py` script at the repo root that:

- Prints `"Hello from Looper!"` when run with no arguments.
- Accepts an optional `--name` flag to customize the greeting.
- Uses `argparse` for CLI argument parsing.

The repository already has `greeting.py` (PR #37) with a `greet(name: str = "World") -> str` function that returns `"Hello, {name}!"`. However, the output format requested by the issue (`"Hello from {name}!"`) differs from `greeting.py`'s template (`"Hello, {name}!"`), so `hello.py` will define its own `greet()` rather than import from `greeting.py`.

This keeps the two scripts decoupled — if either template format changes in the future, each can be updated independently without affecting the other.

## Goals

1. Create an executable `hello.py` at the repo root with a shebang line.
2. Use `argparse` for CLI argument parsing with a `--name` flag.
3. Define a local `greet()` function with `"Hello from {name}!"` template (distinct from `greeting.py`'s `"Hello, {name}!"`).
4. Default `--name` value must be `"Looper"` so bare invocation prints `"Hello from Looper!"`.
5. Keep `greeting.py` unchanged — do not refactor, import from, or extract code from it.

## Non-goals

- No changes to `greeting.py` or its test infrastructure.
- No packaging / `setup.py` / `pyproject.toml` — both scripts run as `python3 hello.py`.
- No error handling beyond what `argparse` provides for the `--name` argument.
- No unit tests — verification is via manual smoke tests listed in Step 2.

## Design decisions

| Decision | Rationale |
|----------|-----------|
| Own `greet()` vs import from `greeting.py` | The issue specifies `"Hello from {name}!"`, not `"Hello, {name}!"`. Defining a local `greet()` avoids coupling two scripts over a cosmetic template choice. |
| `default="Looper"` | Matches the issue statement "prints 'Hello from Looper!'" |
| `--name` flag (not positional arg) | Self-documenting at the call site; more discoverable via `--help`. |
| Shebang `#!/usr/bin/env python3` | Makes the file directly executable (`./hello.py`). |
| `if __name__ == "__main__"` guard | Allows `greet()` to be imported from `hello.py` if needed in the future. |
| No external dependencies | Both scripts use only the Python 3 stdlib (`argparse`). |
| No tests directory / test file | Existing pattern in the repo (neither `greeting.py` nor prior versions of `hello.py` have tests). |

## Implementation steps

### Step 1 — Create `hello.py`

Create a new file at the repo root with the following structure:

```python
#!/usr/bin/env python3
"""A simple hello script with argparse support."""

import argparse


def greet(name: str = "Looper") -> str:
    """Return a greeting string for the given name."""
    return f"Hello from {name}!"


def main() -> None:
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

> **Note on file system:** The canonical location is `/private/tmp/test-looper/hello.py` (the repo root outside any `.looper/worktrees/` directory). The CI / looper workflow will pick it up from there.

### Step 2 — Verify correctness

After writing the file, run these smoke tests from the repo root:

```bash
cd /private/tmp/test-looper

# Default invocation → "Hello from Looper!"
python3 hello.py

# Custom --name → "Hello from Alice!"
python3 hello.py --name Alice

# Multi-word name → "Hello from Bob Dole!"
python3 hello.py --name "Bob Dole"

# Help text → prints argparse help
python3 hello.py --help
```

Each of the first three assertions exercises one path through the code:
1. No `--name` → `greet()` receives the default `"Looper"`.
2. Short `--name` value → `greet()` receives the provided string.
3. Multi-word `--name` value → verifies quoting works correctly for shell.

The `--help` check validates that `argparse` produces readable output (subjective — at minimum confirm it shows `--name` and the description).

### Step 3 — Commit and push

Working from the main repo at `/private/tmp/test-looper`:

```bash
git add hello.py
git commit -m "feat: add hello.py with argparse --name support (#72)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

The commit message follows the repo's existing convention (see `217e6e7` and `48ed356`): start with `feat:`, briefly describe the change, reference the issue with `(#72)`, and include the Claude co-author trailer.

**Branch strategy:** Work on a feature branch derived from `main` (e.g. `worker/<uuid>` or a descriptive name like `feat/72-hello-py`). Open a PR targeting `main`.

## Alternative approaches considered but rejected

| Approach | Rejected because |
|----------|-----------------|
| Import `greet()` from `greeting.py` | `greeting.py`'s `greet()` returns `"Hello, {name}!"` — doesn't match the issue's `"Hello from {name}!"`. Either we'd add a parameter to `greeting.py`'s `greet()` (touches `greeting.py`, violates Non-goals) or we'd accept the wrong template. |
| Make `--name` a positional argument | Less self-documenting. With a flag, `python3 hello.py --name Alice` is clearer than `python3 hello.py Alice`, and `--help` makes the option visible without reading source. |
| Use `sys.argv` directly (like `greeting.py`) | `argparse` provides free `--help`, type validation, and is the standard for Python CLI tools with one or more optional flags. |

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **CREATE** | Executable Python script with shebang and `if __name__` guard |
| `greeting.py` | **untouched** | No changes |

## Backward compatibility

No breaking changes. `greeting.py` works exactly as before:

- `python3 greeting.py` → `"Hello, World!"`
- `python3 greeting.py Alice` → `"Hello, Alice!"`

The new `hello.py` is an independent script and does not affect any existing functionality.
