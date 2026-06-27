# Spec: Add `hello.py` with `--name` flag (Issue #85)

**Issue:** #85 — Create `hello.py` that prints `"Hello from Looper!"` with optional `--name` flag.

---

## Objective

Add a new executable `hello.py` script at the repo root that prints a greeting and accepts a `--name` argument via Python's `argparse` module. The default greeting (`"Hello from Looper!"`) differs from the existing `greeting.py` (`"Hello, World!"`), so `hello.py` defines its own `greet()` function rather than reusing `greeting.py`'s.

## Background

The repo already has `greeting.py` with:
- `greet(name: str = "World") -> str` returning `f"Hello, {name}!"`
- Positional argument parsing via `sys.argv`

Issue #85 asks for a **separate** script with `"Hello from {name}!"` format and `argparse` `--name` flag. Because the template string differs (`"from"` vs `,` and default `"Looper"` vs `"World"`), `hello.py` owns its own `greet()` rather than importing `greeting.py`'s.

A prior attempt for issue #72 landed `hello.py` on `main` (commit `e26dea2`), so `hello.py` already exists at the repo root with the correct implementation. This spec documents the expected state and verification steps.

## Implementation Steps

### Step 1 — Verify / create `hello.py`

**File location:** `/private/tmp/test-looper/hello.py` (repo root, alongside `greeting.py`)

**Required structure:**

```python
#!/usr/bin/env python3
"""A simple hello script with argparse support."""

import argparse

# Own greet() — "Hello from {name}!" format differs from greeting.py's "Hello, {name}!"

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

| Choice | Reason |
|--------|--------|
| Own `greet()` (not importing `greeting.py`) | The issue specifies `"Hello from {name}!"` format with `"Looper"` default — different from `greeting.py`'s `"Hello, {name}!"` / `"World"`. A standalone function avoids coupling unrelated scripts against a cosmetic template choice. |
| `default="Looper"` | Matches the issue requirement: bare invocation prints `"Hello from Looper!"`. |
| `--name` flag (not positional) | Consistent with common argparse patterns; more self-documenting than a positional argument for a single optional value. |
| Shebang line | Makes the file directly executable (`./hello.py`). |
| `if __name__ == "__main__"` guard | Allows `greet()` to be imported from `hello.py` in the future without triggering `main()`. |

### Step 2 — Verify correctness

Run each of the following from the repo root and confirm the output:

```bash
cd /private/tmp/test-looper

# Default (no args) → "Hello from Looper!"
python3 hello.py

# Custom name → "Hello from Alice!"
python3 hello.py --name Alice

# Quoted name with space → "Hello from Bob Dole!"
python3 hello.py --name "Bob Dole"

# Help text
python3 hello.py --help

# Unknown flag → non-zero exit + error message
python3 hello.py --unknown-flag
```

The first three assertions each cover one path through the single branch point (`name` defaulted vs overridden with simple vs multi-word value). The `--help` test verifies argparse help renders correctly. The unknown-flag test verifies argparse error handling.

### Step 3 — Commit (if file is new or changed)

```bash
cd /private/tmp/test-looper
git add hello.py
git commit -m "feat: add hello.py with argparse --name support (#85)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

The commit message follows the existing repo convention: `feat:` prefix, issue reference `(#85)`, and the Claude co-author trailer.

## Files Touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **CREATE** (if missing) or **verification only** (if present) | New script with shebang, own `greet()`, argparse `--name` |
| `greeting.py` | untouched | No changes to the existing script or its interface |

## Acceptance Criteria

1. `python3 hello.py` prints `Hello from Looper!` (uses the argparse default `"Looper"`).
2. `python3 hello.py --name Alice` prints `Hello from Alice!`.
3. `python3 hello.py --name "Bob Smith"` prints `Hello from Bob Smith!`.
4. `python3 hello.py --help` prints a help message describing the `--name` flag.
5. `python3 hello.py --unknown-flag` exits with non-zero exit code and prints an error.
6. `greeting.py` is not modified.
7. `python3 greeting.py` still prints `Hello, World!` (backward compatibility).

## Risks

- **File already exists from issue #72** — If `hello.py` is already on `main` with matching content, no changes needed; skip creation and go straight to verification.
- **Worktree placement** — Must create `hello.py` at the repo root, not inside `.looper/worktrees/`, so the file lands on `main` after merging the PR.
