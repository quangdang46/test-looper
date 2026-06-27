# Spec: hello.py with argparse `--name` flag

Issue: #93
Status: proposal

---

## Objective

Create `hello.py` — an executable Python script at the repo root that prints a greeting and accepts a `--name` argument via `argparse`. The script reuses the existing `greet()` function from `greeting.py` to avoid duplicating the greeting logic.

## Background

The repository already has `greeting.py` (PR #37) which provides a `greet(name: str = "World") -> str` function returning `"Hello, {name}!"` and a `main()` that reads from `sys.argv`. Issue #92 asks for a *new* script `hello.py` with equivalent functionality but using `argparse` for argument parsing rather than raw `sys.argv`.

A prior attempt (issue #72 / #101) added `hello.py` with a *separate* `greet()` returning `"Hello from {name}!"`. That version was created inside a git worktree (`.looper/worktrees/worker-*`) and never merged to `main`. Issue #93 is a fresh attempt to land `hello.py` on `main` — but this time reusing the existing `greeting.greet()` so there is only one `greet()` to maintain.

## Rationale — import vs. own greet

| Approach | Consequence |
|----------|-------------|
| **Import from `greeting.py`** (chosen) | Single source of truth for greeting logic. Any future changes to the greeting template or default affect both scripts. |
| Own `greet()` (as tried in #72) | Two functions with the same purpose to maintain. If the template or default drifts between them, the inconsistency looks like a bug. |

## Implementation Steps

### Step 1 — Remove stale `hello.py` (if present)

The current working tree may contain a `hello.py` from the #72 attempt that has its own `greet()` and a different default name (`"Looper"`) and template (`"Hello from {name}!"`). If present, **delete it** — the #93 implementation starts fresh:

```bash
rm hello.py   # only if it has the standalone greet()
```

### Step 2 — Create `hello.py`

Create a new file at the repo root (`/private/tmp/test-looper/hello.py`).

**Structure:**

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

| Choice | Reason |
|--------|--------|
| `from greeting import greet` | Reuses existing logic; avoids a second `greet()` to maintain. |
| `default="World"` | Must match `greeting.py`'s `greet()` default so bare invocation `python3 hello.py` produces the same output as `python3 greeting.py`. |
| `--name` flag (not positional) | Consistent with the issue title. Flags are more self-documenting. |
| shebang line | Makes the file directly executable for local testing. |
| `__name__ == "__main__"` guard | Allows importing from `hello.py` in the future if needed. |
| No `greet()` in `hello.py` | The script is a thin CLI wrapper, not a library. If a caller needs the greet function they import from `greeting.py`. |

### Step 3 — Verify correctness

Run from the repo root:

```bash
cd /private/tmp/test-looper

# Default invocation
python3 hello.py                      # → "Hello, World!"

# Custom name
python3 hello.py --name Alice         # → "Hello, Alice!"

# Name with spaces (quoted)
python3 hello.py --name "Bob Smith"   # → "Hello, Bob Smith!"

# Help text
python3 hello.py --help               # exits 0, describes --name

# Error on unknown flag
python3 hello.py --unknown-flag       # exits non-zero, prints error
```

Five assertions — three positive paths covering the argparse default, short name, and spaced name; one usability check; one error-path check.

### Step 4 — Commit and push

```bash
git add hello.py
git rm hello.py   # only if the old hello.py was tracked
git commit -m "feat: hello.py with argparse --name flag, reusing greet() from greeting.py (#93)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

The commit message follows the repo convention (see `217e6e7` for `greeting.py`): `feat:`, brief description, issue reference with `(#93)`, and the Claude co-author trailer.

## Acceptance Criteria

1. `python3 hello.py` prints `Hello, World!`.
2. `python3 hello.py --name Alice` prints `Hello, Alice!`.
3. `python3 hello.py --name "Bob Smith"` prints `Hello, Bob Smith!`.
4. `python3 hello.py --help` exits 0 and prints help text describing `--name`.
5. `python3 hello.py --unknown-flag` exits non-zero with an error message.
6. `greeting.py` is **not modified** in any way.
7. `python3 -c "from greeting import greet; print(greet())"` still works (import chain intact).
8. `python3 -c "from hello import main"` succeeds (the `__name__` guard enables importability).

## Files Touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **Create** (repo root) | New script importing `greet` from `greeting.py` |
| `hello.py` | **Delete** (if standalone version from #72 exists) | Only if the file has its own `greet()` and `default="Looper"` |
| `greeting.py` | untouched | No changes needed |

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| **Import path confusion** — `from greeting import greet` fails if run outside the repo root | Document that the script must be run from the project root. The commit instructions use absolute paths for clarity. |
| **Default name mismatch** — if `hello.py`'s argparse default doesn't match `greeting.py`'s greet default, bare invocations diverge. | Hard-code `default="World"` to match `greeting.greet()`. |
| **Regressing `greeting.py`** — accidentally modifying the shared function | Verification step #6 checks `greeting.py` is untouched. |
| **Worktree placement** — file lands inside `.looper/worktrees/` and never merges | Create the file at the *repo root* (`/private/tmp/test-looper/hello.py`), not inside the worktree directory. |
