# Spec: Create `hello.py` with argparse `--name` flag (Issue #101)

## Problem

Issue #101 asks for a `hello.py` script that uses `argparse` to accept a `--name` flag and prints a greeting. The repo already has `greeting.py` (PR #37) with a `greet()` function returning `f"Hello, {name}!"`. A previous attempt (issue #72) added `hello.py` with its own `greet()` but that version was never landed on `main`. Issue #93 successfully landed `hello.py` that imports `greet()` from `greeting.py` (commit `6afb126`).

Since #93's implementation is already on `main`, issue #101 represents a re-grounding: the existing `hello.py` must be verified to match its spec, and any gaps or regressions must be addressed.

## Current state

| File | Status | Content |
|------|--------|---------|
| `greeting.py` | Exists, unchanged | Has `greet(name="World")` returning `f"Hello, {name}!"` |
| `hello.py` | Exists (from #93) | Imports `greet` from `greeting.py`, uses `argparse` with `--name` (default `"World"`) |

## Goals

1. Ensure `hello.py` is present at the repo root with the correct implementation.
2. Use `argparse` for CLI argument parsing with a `--name` flag (type `str`, default `"World"`).
3. Import and reuse `greet()` from `greeting.py` — do not duplicate the greeting logic.
4. Include a `main()` function guarded by `if __name__ == "__main__"`.
5. Keep `greeting.py` unchanged.

## Non-goals

- No changes to `greeting.py`.
- No packaging / `setup.py` / `pyproject.toml`.
- No additional flags beyond `--name`.

---

## Implementation Steps

### Step 1 — Verify `hello.py` exists with correct content

If `hello.py` already exists at the repo root (from a previous merge), verify it conforms to the expected implementation below. If it is missing or deviates, recreate or correct it.

**Required structure:**

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

**Key design decisions:**

| Choice | Reason |
|--------|--------|
| `import greet` from `greeting.py` | Reuses the canonical greeting logic; avoids duplicate code. The template `"Hello, {name}!"` lives in one place. |
| `default="World"` | Matches `greeting.py`'s `greet()` default — identical behavior on bare `python3 hello.py` and `python3 greeting.py`. |
| `--name` flag (not positional) | Consistent with common argparse patterns; self-documenting. |
| `main()` function + `__name__` guard | Allows importing `main()` in tests; standard Python entry-point pattern. |
| Shebang line | Makes the file directly executable for local testing. |

### Step 2 — Verify correctness

Run these assertions from the repo root:

```bash
cd /private/tmp/test-looper

# (1) Default invocation
python3 hello.py
# Expected: Hello, World!

# (2) Custom name
python3 hello.py --name Alice
# Expected: Hello, Alice!

# (3) Spaced name (quoted)
python3 hello.py --name "Bob Smith"
# Expected: Hello, Bob Smith!

# (4) Usage help
python3 hello.py --help
# Expected: prints argparse help showing the --name flag

# (5) Unknown flag exits non-zero
python3 hello.py --unknown-flag
# Expected: non-zero exit, error message on stderr

# (6) greeting.py is untouched
python3 greeting.py
# Expected: Hello, World!
python3 greeting.py Alice
# Expected: Hello, Alice!
```

### Step 3 — Commit and push (only if changes were needed)

If the file needed to be created or corrected:

```bash
git add hello.py
git commit -m "feat: hello.py with argparse --name flag, reusing greet() from greeting.py (#101)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

If the file already exists and is correct, no commit is necessary — the issue can be closed as already implemented.

---

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **Verify** (or recreate if missing) | Must import `greet` from `greeting.py`, use argparse with `--name` default `"World"` |
| `greeting.py` | untouched | No changes allowed |

## Acceptance criteria

1. `python3 hello.py` prints `Hello, World!`
2. `python3 hello.py --name Alice` prints `Hello, Alice!`
3. `python3 hello.py --name "Bob Smith"` prints `Hello, Bob Smith!`
4. `python3 hello.py --help` prints help text describing `--name`
5. `python3 hello.py --unknown-flag` exits non-zero with error
6. `greeting.py` is not modified
7. `python3 -c "from greeting import greet; print(greet())"` still works (no import chain breakage)

## Related issues

| Issue | Outcome |
|-------|---------|
| #37 | Added `greeting.py` with `greet()` — foundation for this work |
| #72 | First attempt at `hello.py` with own `greet()` — never merged |
| #93 | Second attempt — merged, `hello.py` imports `greet` from `greeting.py` |
| #101 | Current issue — verify and ground the implementation |
