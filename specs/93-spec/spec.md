# Spec: hello.py with argparse `--name` flag

Issue: #93
Spec: specs/93-spec/spec.md

---

## Objective

Add a new `hello.py` script that prints a greeting and accepts a `--name` argument via Python's `argparse` module, building on the existing `greeting.py` library function. This reuses the `greet()` function from `greeting.py` rather than duplicating the greeting logic.

## Background

A prior attempt (issue #72 / #101) added `hello.py` but the file was created inside a git worktree directory (`.looper/worktrees/worker-*`) and never merged onto `main`. Issue #93 is a fresh attempt to land `hello.py` on `main` with equivalent functionality.

To avoid repeating the same issue, the spec should ensure the file is placed directly in the repo root alongside `greeting.py`, not inside a `.looper` worktree directory.

## Implementation Plan

1. **Create `hello.py`** — write a new executable Python script at the repo root.
   - Reuse `greet()` by importing it from `greeting.py`.
   - Use `argparse.ArgumentParser` to declare a `--name` flag (default: `"World"`).
   - Print the result of `greet(name)`.
   - Include a `main()` function guarded with `if __name__ == "__main__":`.
   - Use the same `#!/usr/bin/env python3` shebang as the project convention.

2. **Verify correctness** — run `python3 hello.py` and `python3 hello.py --name Alice` and confirm the output matches `greeting.py`'s behavior.

## Files to Change

| File | Action | Notes |
|---|---|---|
| `hello.py` | **Create** (at repo root) | New script. Imports `greet` from `greeting.py`; parses `--name` via argparse. Must be placed in the repo root, not inside `.looper/worktrees/`. |

## Risks

- **Import path confusion** — if `hello.py` is run from outside the repo root, the `from greeting import greet` import could fail. Running from the project root (where `greeting.py` lives) avoids this.
- **Argparse default vs script default mismatch** — the argparse default for `--name` must match `greeting.py`'s `greet()` default (`"World"`) so the bare-call behavior is identical.
- **Regression on greeting.py** — the existing `greeting.py` should be left completely unchanged.
- **Worktree placement** — `hello.py` must be created at the repo root (not inside `.looper/worktrees/`) so the file lands on `main` after merging.

## Acceptance Criteria

1. `python3 hello.py` prints `Hello, World!` (uses the argparse default).
2. `python3 hello.py --name Alice` prints `Hello, Alice!`.
3. `python3 hello.py --name "Bob Smith"` prints `Hello, Bob Smith!` (quoted names with spaces work).
4. `python3 hello.py --help` prints a help message describing the `--name` flag.
5. `python3 hello.py --unknown-flag` exits with a non-zero exit code and prints an error.
6. The `greeting.py` file is not modified.
7. `python3 -c "from greeting import greet; print(greet())"` still works (no import chain breaks).
