# Spec: Implement `hello.py` (Issue #72)

## Problem

**Issue #72** asks for a `hello.py` script that prints `"Hello from Looper!"` with an optional `--name` flag to customize the greeting. The repository already has `greeting.py` (PR #37) with its own `greet()` returning `"Hello, {name}!"` — since the output format for this issue is different (`"Hello from {name}!"` vs `"Hello, {name}!"`), `hello.py` will define its own `greet()` with the required template rather than importing from `greeting.py`.

## Goals

1. Create an executable `hello.py` at the repo root.
2. Use `argparse` for CLI argument parsing with a `--name` flag.
3. Own a `greet()` function with `"Hello from {name}!"` format (distinct from `greeting.py`'s `"Hello, {name}!"`).
4. Default value for `--name` must be `"Looper"` (so bare invocation prints `"Hello from Looper!"`).
5. Keep `greeting.py` unchanged — do not refactor or extract its `main()`.

## Non-goals

- No changes to `greeting.py` or its test infrastructure.
- No packaging / `setup.py` / `pyproject.toml` — both scripts run as `python3 hello.py`.
- No error handling beyond what `argparse` provides for `--name`.

---

## Implementation Steps

### Step 1 — Create `hello.py`

Create a new file `/private/tmp/test-looper/hello.py` (repo root).

**Structure:**

```python
#!/usr/bin/env python3
"""A simple hello script with argparse support."""

import argparse
# Own `greet()` — the issue asks for `"Hello from {name}!"` format
# which differs from greeting.py's `"Hello, {name}!"`

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

**Rationale for key choices:**

| Choice | Reason |
|--------|--------|
| Own `greet()` (not importing from `greeting.py`) | The issue specifies `"Hello from {name}!"` format, which differs from `greeting.py`'s `"Hello, {name}!"`. A standalone function avoids coupling the two scripts against a cosmetic template choice; if the template format needs to change in the future, each script can be updated independently. |
| `default="Looper"` | Matches the issue's example output `"Hello from Looper!"`. |
| `--name` (not positional) | Flags are more self-documenting, consistent with common argparse patterns. Positional would also work but flags are the pattern used more often when there's only one optional argument. |
| shebang line | Makes the file directly executable (`./hello.py`) for local testing. |
| `__name__ == "__main__"` guard | Allows `greet()` to be imported from `hello.py` in the future if needed. |

### Step 2 — Verify correctness

After writing the file, validate:

```bash
cd /private/tmp/test-looper
python3 hello.py                    # → "Hello from Looper!"
python3 hello.py --name Alice       # → "Hello from Alice!"
python3 hello.py --name "Bob Dole"  # → "Hello from Bob Dole!"
python3 hello.py --help             # shows help text
```

The first three assertions each check one path through the single branch point (`name` defaulted vs overridden). The `--help` test is a usability check and makes `argparse` produce its full output.

### Step 3 — Commit and push

Working from the main repo at `/private/tmp/test-looper`:

```bash
git add hello.py
git commit -m "feat: add hello.py with argparse --name support (#72)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

The commit message follows the repo's existing convention (see `48ed356` and `217e6e7`): start with `feat:`, reference the issue with `(#72)`, and include the Claude co-author trailer.

---

## Files touched

| File | Action |
|------|--------|
| `hello.py` | **CREATE** — executable Python script using shebang |
| `greeting.py` | untouched |

## Backward compatibility

No breaking changes. `greeting.py` works exactly as before — `python3 greeting.py` still prints `"Hello, World!"`, `python3 greeting.py Alice` prints `"Hello, Alice!"`.
