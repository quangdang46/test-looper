# Spec: hello.py with argparse `--name` flag (Issue #93)

Issue: https://github.com/quangdang46/test-looper/issues/93
Spec: specs/93-spec/spec.md

---

## Objective

Create a new `hello.py` script at the repo root that prints a greeting and accepts a `--name` argument via Python's `argparse` module. The script reuses `greet()` from the existing `greeting.py` to avoid duplicating greeting logic.

## Background

Issue #93 asks for a `hello.py` with a `--name` flag. The repo already has `greeting.py` (issue #37) with a reusable `greet(name: str = "World") -> str` function that returns `f"Hello, {name}!"`.

Previous attempts (#72, #101) created `hello.py` with its own `greet()` function using template `"Hello from {name}!"` inside a git worktree, and those branches were never merged onto `main`. Issue #93 is a fresh attempt to land `hello.py` on `main`.

This spec takes the simpler approach: reuse `greeting.py`'s `greet()` rather than duplicating it. The `--name` argparse default will match `greeting.py`'s `greet()` default of `"World"`, so bare-call behavior is identical.

## Implementation Steps

### Step 1 — Create `hello.py`

Write a new executable script at the repo root (`hello.py`).

**Structure:**

```python
#!/usr/bin/env python3
"""A simple hello script with argparse support, built on greeting.py."""

import argparse
from greeting import greet


def main() -> None:
    """Parse --name argument and print greeting."""
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
| Import `greet` from `greeting.py` | DRY — `greeting.py` already defines the greeting logic. No benefit in duplicating the template string. |
| Default `"World"` | Matches `greeting.py`'s `greet()` default, so `python3 hello.py` behaves identically to `python3 greeting.py`. |
| Shebang `#!/usr/bin/env python3` | Project convention; matches `greeting.py`. |
| `__name__ == "__main__"` guard | Standard Python pattern; keeps `main()` import-safe. |
| `main()` function | Consistent structure with `greeting.py`; testable. |

### Step 2 — Verify correctness

Run from the repo root:

```bash
python3 hello.py                     # → "Hello, World!"
python3 hello.py --name Alice        # → "Hello, Alice!"
python3 hello.py --name "Bob Smith"  # → "Hello, Bob Smith!"
python3 hello.py --help              # shows help text
python3 hello.py --unknown-flag      # exits non-zero, prints error
```

The first three assertions verify the happy path with default, simple override, and quoted multi-word name. `--help` confirms argparse is wired correctly. `--unknown-flag` confirms argparse's built-in error behavior works (non-zero exit, `unrecognized arguments` message).

### Step 3 — Commit

```bash
git add hello.py
git commit -m "feat: create hello.py reusing greet() from greeting.py (#93)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

The commit message follows the repo's `feat:` convention and references the issue.

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **CREATE** (repo root) | Executable Python script. Imports `greet` from `greeting.py`. |
| `greeting.py` | untouched | No changes needed. |

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| **Import path** — `from greeting import greet` fails if `hello.py` is run from outside the repo root | Document that the script must be run from the repo root (where `greeting.py` lives). This is the standard usage in this repo. |
| **Argparse default mismatch** — argparse default doesn't match `greet()` default | Set argparse `default="World"` explicitly, matching `greeting.py`'s `greet(name: str = "World")`. |
| **Regression on greeting.py** — changes break existing behavior | Do not modify `greeting.py` at all. |
| **Worktree placement** — file ends up inside `.looper/` and never lands on `main` | Create the file directly at the repo root (alongside `greeting.py`). `git add` from the repo root. |

## Acceptance criteria

1. `python3 hello.py` prints `Hello, World!` (argparse default).
2. `python3 hello.py --name Alice` prints `Hello, Alice!`.
3. `python3 hello.py --name "Bob Smith"` prints `Hello, Bob Smith!` (quoted names with spaces).
4. `python3 hello.py --help` displays help with `--name` flag documented.
5. `python3 hello.py --unknown-flag` exits non-zero with `unrecognized arguments` error.
6. `greeting.py` is not modified.
7. `python3 greeting.py` still works as before — `Hello, World!`.
8. `python3 -c "from greeting import greet; print(greet())"` still works.
