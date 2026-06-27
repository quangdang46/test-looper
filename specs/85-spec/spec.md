# Spec: Add `hello.py` (Issue #85)

Issue: #85
Phase: Plan

---

## Objective

**Issue #85** asks for a `hello.py` script at the repo root that prints `"Hello from Looper!"` and accepts an optional `--name` flag via `argparse` to customize the greeting. The output format (`"Hello from {name}!"`) differs from the existing `greeting.py`'s `"Hello, {name}!"` (default `"World"`), so `hello.py` will define its own `greet()` function.

## Background

Prior attempts (issues #72, #93) landed `hello.py` in worktree branches. Issue #85 is a clean entry — same end state, same pattern: an executable Python script at the repo root with its own `greet()` function and `argparse` CLI.

The existing `greeting.py` (`specs/37-spec`) is left untouched.

## Implementation Steps

### Step 1 — Create `hello.py`

Create a new file `hello.py` at the repository root with the following structure:

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

### Step 2 — Verify correctness

Run the following validation commands from the repo root:

```bash
python3 hello.py                        # → "Hello from Looper!"
python3 hello.py --name Alice           # → "Hello from Alice!"
python3 hello.py --name "Bob Dole"      # → "Hello from Bob Dole!"
python3 hello.py --help                 # shows help text, exits 0
python3 hello.py --unknown-flag         # exits non-zero with error
```

| Command | Expected output | What it tests |
|---------|----------------|---------------|
| `python3 hello.py` | `Hello from Looper!` | Default value for `--name` |
| `python3 hello.py --name Alice` | `Hello from Alice!` | Custom single-word name |
| `python3 hello.py --name "Bob Dole"` | `Hello from Bob Dole!` | Quoted multi-word name |
| `python3 hello.py --help` | Usage + flag help | argparse help output |
| `python3 hello.py --unknown-flag` | stderr error, exit 1 | Unknown flag rejection |

### Step 3 — Ensure greeting.py is unchanged

Confirm no regression:

```bash
python3 greeting.py                     # → "Hello, World!"
python3 greeting.py Alice               # → "Hello, Alice!"
python3 -c "from greeting import greet; print(greet())"  # → "Hello, World!"
```

### Step 4 — Commit

```bash
git add hello.py
git commit -m "feat: add hello.py with argparse --name support (#85)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **CREATE** — at repo root | Executable shebang script with own `greet()` and `argparse` CLI |
| `greeting.py` | untouched | No changes |

## Acceptance criteria

1. `python3 hello.py` prints `Hello from Looper!`
2. `python3 hello.py --name Alice` prints `Hello from Alice!`
3. `python3 hello.py --name "Bob Smith"` prints `Hello from Bob Smith!`
4. `python3 hello.py --help` prints usage and exits 0
5. `python3 hello.py --unknown-flag` exits non-zero with error
6. `greeting.py` is not modified; `python3 greeting.py` still prints `Hello, World!`
