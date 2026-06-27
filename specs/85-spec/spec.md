# Spec: Implement `hello.py` with "Hello from Looper!" (Issue #85)

## Problem

**Issue #85** asks for a `hello.py` script that prints `"Hello from Looper!"` with an optional `--name` flag to customize the greeting. The repository already has `greeting.py` (PR #37, `greet()` returns `"Hello, {name}!"`) and a current `hello.py` that imports `greet()` from `greeting.py` — producing `"Hello, World!"` by default. Neither the default name (`"World"`) nor the template (`"Hello, {name}!"`) matches the required output (`"Hello from Looper!"`).

Since the greeting format requested by #85 (`"Hello from {name}!"`) differs from `greeting.py`'s format (`"Hello, {name}!"`), `hello.py` must define its own `greet()` function with the required template rather than importing from `greeting.py`.

## Prior attempts

| Issue | Approach | Status |
|-------|----------|--------|
| #72 | Own `greet()` in `hello.py` with `"Hello from {name}!"` template and `--name` flag defaulting to `"Looper"` | Merged in worktree, never landed on `main` |
| #93 | Reuse `greet()` from `greeting.py` with `--name` flag defaulting to `"World"` | Landed on `main` (current `hello.py`) but does not match #85's required output |
| #85 **(this)** | Own `greet()` in `hello.py` with `"Hello from {name}!"` template and `--name` flag defaulting to `"Looper"` | Target |

## Goals

1. Modify the existing `hello.py` at the repo root to:
   - Own a `greet()` function using the `"Hello from {name}!"` template (distinct from `greeting.py`'s `"Hello, {name}!"`).
   - Use `argparse` for CLI parsing with a `--name` flag.
   - Default `--name` to `"Looper"` so bare invocation prints `"Hello from Looper!"`.
   - Keep a `main()` guard and shebang for executability.
2. Leave `greeting.py` completely unchanged.

## Non-goals

- No changes to `greeting.py` or its test infrastructure.
- No packaging / `setup.py` / `pyproject.toml` — the script runs as `python3 hello.py`.
- No error handling beyond what `argparse` provides for `--name`.
- No new test files — the issue scope is the script itself.

---

## Implementation Steps

### Step 1 — Update `hello.py`

Modify the existing `hello.py` to replace the `from greeting import greet` import with a self-contained version that matches the required output format.

**Resulting structure:**

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

**Changes from current `hello.py`:**

| Aspect | Before | After | Reason |
|--------|--------|-------|--------|
| Import | `from greeting import greet` | Own `greet()` function | The `"Hello from {name}!"` format differs from `greeting.py`'s `"Hello, {name}!"`. A standalone function decouples the two scripts; if the template changes later each can be updated independently. |
| Template | `f"Hello, {name}!"` (via `greeting.py`) | `f"Hello from {name}!"` | Matches the issue requirement directly. |
| Default | `"World"` | `"Looper"` | Matches the issue's example `"Hello from Looper!"`. |
| `argparse` default | `"World"` | `"Looper"` | Must match the function default so both code paths produce the same output. |

### Step 2 — Verify correctness

After updating the file, validate every code path:

```bash
cd /private/tmp/test-looper
python3 hello.py                    # → "Hello from Looper!"
python3 hello.py --name Alice       # → "Hello from Alice!"
python3 hello.py --name "Bob Dole"  # → "Hello from Bob Dole!"
python3 hello.py --help             # shows help text
python3 hello.py --unknown-flag     # exits non-zero with error message
```

The first three assertions each check one path through the single branch point (`name` defaulted vs overridden). The `--help` test is a usability check. The `--unknown-flag` test confirms argparse's built-in error handling works.

### Step 3 — Verify `greeting.py` is unchanged

```bash
python3 greeting.py                  # → "Hello, World!" (unchanged)
python3 greeting.py Alice            # → "Hello, Alice!" (unchanged)
python3 -c "from greeting import greet; print(greet())"  # → "Hello, World!"
```

The existing `greeting.py` and its import path must not be broken by the changes.

### Step 4 — Commit

```bash
git add hello.py
git commit -m "feat: update hello.py with own greet() and 'Hello from Looper!' default (#85)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

---

## Files touched

| File | Action |
|------|--------|
| `hello.py` | **MODIFY** — replace import from `greeting.py` with own `greet()`; change default name to `"Looper"`; change template to `"Hello from {name}!"`. |
| `greeting.py` | untouched |

## Backward compatibility

- `greeting.py` works exactly as before — `python3 greeting.py` still prints `"Hello, World!"`, `python3 greeting.py Alice` prints `"Hello, Alice!"`.
- `hello.py` changes its output format from `"Hello, {name}!"` to `"Hello from {name}!"` and its default name from `"World"` to `"Looper"`. This is a deliberate breaking change to match issue #85's requirements.

## Risks

| Risk | Mitigation |
|------|------------|
| Import path breaks if something imports `greet` from `hello.py` | This is a new change; no existing code depends on `hello.greet`. |
| Human runs `hello.py --name Alice` and expects `"Hello, Alice!"` (old format) | The issue explicitly asks for the new format; verify with the team if this is intentional. |
