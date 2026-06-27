# Spec: `hello.py` with `--name` flag using argparse (Issue #101)

## Problem

**Issue #101** asks for a `hello.py` script with an `--name` flag using Python's `argparse` module. The repository already has `greeting.py` (PR #37) which provides a `greet(name: str = "World") -> str` function returning `"Hello, {name}!"`.

Two prior attempts exist — issue #72 and issue #93 — both of which created a `hello.py` that was either placed inside a `.looper/worktrees/` subdirectory or never properly merged onto `main`. The current worker branch (`worker/83331890-…`) carries a working `hello.py` from the #93 attempt, but the issue was reopened and relabeled (`looper/planned`, `looper:implement`, `looper:plan`), indicating the file still needs to be landed cleanly on `main`.

## Goals

1. Ensure `hello.py` exists at the repo root with correct shebang (`#!/usr/bin/env python3`).
2. Import `greet()` from `greeting.py` (not duplicate the greeting logic).
3. Use `argparse.ArgumentParser` to accept a `--name` flag (default `"World"` to match `greeting.py`'s `greet()` default).
4. Include a `main()` function guarded with `if __name__ == "__main__":`.
5. Leave `greeting.py` unchanged.

## Non-goals

- No changes to `greeting.py` or its test infrastructure.
- No packaging / `setup.py` / `pyproject.toml` — scripts run as `python3 hello.py`.
- No additional flags beyond `--name`.

---

## Implementation Steps

### Step 1 — Ensure `hello.py` exists at repo root

The file `/private/tmp/test-looper/hello.py` should already exist (from prior attempts). Verify or create it with the following content:

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

| Decision | Rationale |
|----------|-----------|
| Import `greet` from `greeting.py` | Reuses existing logic; avoids duplicating the greeting template string. |
| `default="World"` | Matches `greeting.py`'s `greet()` default so bare invocation (`python3 hello.py`) prints `"Hello, World!"`. |
| `--name` (not positional) | Self-documenting; consistent with common argparse patterns for optional named arguments. |
| Shebang + `if __name__` guard | Executable directly (`./hello.py`); importable by future scripts without running `main()`. |

### Step 2 — Verify correctness

Run each of the following from the repo root:

```bash
cd /private/tmp/test-looper
python3 hello.py                          # → "Hello, World!"       (default)
python3 hello.py --name Alice             # → "Hello, Alice!"       (simple flag)
python3 hello.py --name "Bob Dole"        # → "Hello, Bob Dole!"    (quoted with spaces)
python3 hello.py --help                   # prints usage + flag description
python3 hello.py --unknown-flag           # exits non-zero with error message
```

The first three assertions cover every path through the single branch point (`name` defaulted vs overridden by a flag value). `--help` is a usability check. `--unknown-flag` verifies argparse's built-in error handling.

### Step 3 — Commit and push

```bash
cd /private/tmp/test-looper
git add hello.py
git commit -m "feat: add hello.py with argparse --name flag (#101)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

**Placement guard:** Confirm `hello.py` is at the repo root (`/private/tmp/test-looper/hello.py`), not inside `.looper/worktrees/worker-*`. A file placed inside a worktree subdirectory will never land on `main` after the worktree is cleaned up.

---

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **Ensure at repo root** | Create if missing; verify content if present. |
| `greeting.py` | untouched | No changes to existing code. |

## Backward compatibility

No breaking changes. `greeting.py` works exactly as before — `python3 greeting.py World` prints `"Hello, World!"`, `python3 greeting.py Alice` prints `"Hello, Alice!"`.

## Acceptance criteria checklist

1. `python3 hello.py` → `Hello, World!`
2. `python3 hello.py --name Alice` → `Hello, Alice!`
3. `python3 hello.py --name "Bob Smith"` → `Hello, Bob Smith!`
4. `python3 hello.py --help` shows usage with `--name` description
5. `python3 hello.py --unknown-flag` exits non-zero with error
6. `python3 -c "from greeting import greet; print(greet())"` still works
7. `greeting.py` has zero modifications (verified via `git diff greeting.py`)
8. File is at repo root, confirmed by `ls $(git rev-parse --show-toplevel)/hello.py`
