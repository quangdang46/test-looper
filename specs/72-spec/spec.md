# Spec: Add a simple `hello.py` script (Issue #72)

**Issue:** #72 — Add a simple `hello.py` script
**Status:** Implemented (on current worktree branch)

---

## Objective

Create an executable `hello.py` script at the repo root that accepts an optional `--name` flag via `argparse` and prints a greeting. The script reuses the existing `greet()` function from `greeting.py` (PR #37) rather than defining its own greeting logic, keeping the codebase DRY.

## Background

The repository already has `greeting.py` with a `greet(name: str = "World") -> str` function that returns `f"Hello, {name}!"`. This spec reuses that function — the issue's ask for `"Hello from Looper!"` output could be satisfied by either approach, but importing the existing function avoids duplication and keeps the codebase consistent.

An earlier attempt on this issue produced an implementation with a second `greet()` function, but the final approach (guided by the #93 rework) lands on importing `greeting.greet`.

## Implementation Steps

### Step 1 — Create `hello.py`

Create `hello.py` at the repo root with the following structure:

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

**Key design choices:**

| Choice | Rationale |
|--------|-----------|
| Import `greet()` from `greeting.py` | Reuses existing function — avoids duplicating greeting logic. |
| `default="World"` | Matches `greeting.py`'s default so `python3 hello.py` and `python3 greeting.py` produce identical output. |
| `--name` flag | More self-documenting than a positional argument; standard argparse pattern. |
| `#!/usr/bin/env python3` shebang | Makes the file directly executable (`./hello.py`). |
| `__name__ == "__main__"` guard | Allows importing `main()` or other functions from `hello.py` if needed later. |
| `main()` function | Encapsulates CLI logic cleanly; follows `greeting.py`'s existing pattern. |

### Step 2 — Verify correctness

Run these smoke tests from the repo root:

```bash
python3 hello.py                    # → "Hello, World!"
python3 hello.py --name Alice       # → "Hello, Alice!"
python3 hello.py --name "Bob Dole"  # → "Hello, Bob Dole!"
python3 hello.py --help             # shows help text including --name flag
python3 hello.py --unknown-flag     # exits with error message and non-zero code
```

### Step 3 — Commit

```bash
git add hello.py
git commit -m "feat: add hello.py with argparse --name support (#72)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

The commit message follows repo conventions: `feat:` prefix, issue reference, and Claude co-author trailer (see existing commits `48ed356`, `217e6e7`).

---

## Files changed

| File | Action |
|------|--------|
| `hello.py` | **CREATE** — New script at repo root. |
| `greeting.py` | Untouched. |

## Acceptance criteria

1. `python3 hello.py` prints `Hello, World!` (argparse default matches `greeting.py` default).
2. `python3 hello.py --name Alice` prints `Hello, Alice!`.
3. `python3 hello.py --name "Bob Smith"` prints `Hello, Bob Smith!` (spaces in quoted names work).
4. `python3 hello.py --help` prints help text including the `--name` flag description.
5. `python3 hello.py --unknown-flag` exits with error (non-zero) and prints usage.
6. `greeting.py` is **not modified**.
7. `python3 -c "from greeting import greet; print(greet())"` still works — the import chain from `hello.py` doesn't break `greeting.py`'s importability.
8. Bare invocation of both scripts gives same output: `python3 hello.py` == `python3 greeting.py` == `Hello, World!`.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Import fails when running from outside repo root | Default to running from repo root (where `greeting.py` lives). The `from greeting import greet` import requires `greeting.py` to be in the same directory or on `sys.path`. |
| Argparse default diverging from `greeting.py`'s default | Set `default="World"` explicitly — matches `greeting.py`'s function signature default. |
| Regression on `greeting.py` | The spec explicitly avoids touching `greeting.py` at all; the acceptance criteria verify it still works. |
| File created inside `.looper/worktrees/` instead of repo root | Ensure the file is written to the repo root (next to `greeting.py`), not inside the worktree directory. |

## Compatibility

- `greeting.py` is completely untouched — its behavior, importability, and CLI output are unchanged.
- `hello.py` depends on `greeting.py` at import time, which is fine for a repo-root script.
- Both scripts run as `python3 <script>` — no packaging required.
