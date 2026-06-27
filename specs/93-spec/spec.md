# Spec: Replace `hello.py` with an import-based version (Issue #93)

Issue: #93
Spec: specs/93-spec/spec.md

---

## Objective

Replace the existing `hello.py` (from issue #72) with a cleaned-up version that reuses the `greet()` function from `greeting.py` via import, rather than defining its own `greet()`. The script should use `argparse` for a `--name` flag and match `greeting.py`'s greeting format (`"Hello, {name}!"`).

## Background

Issue #72 added `hello.py` with its own `greet()` function that produced `"Hello from {name}!"` — a format different from `greeting.py`'s `"Hello, {name}!"`. That version is now on `main` (commit `e26dea2`).

Issue #93 takes a different approach: instead of duplicating the greeting logic, `hello.py` should import `greet()` from `greeting.py`, keeping the single source of truth for greeting templates. This reduces code duplication and makes future greeting format changes consistent across all scripts.

## Implementation Plan

1. **Replace `hello.py`** — overwrite the existing file at the repo root.
   - Import `greet()` from `greeting.py` (instead of defining a local `greet()`).
   - Use `argparse.ArgumentParser` to declare a `--name` flag (default: `"World"`, matching `greeting.py`'s `greet()` default).
   - Print the result of `greet(name)`.
   - Include a `main()` function guarded with `if __name__ == "__main__":`.
   - Keep the `#!/usr/bin/env python3` shebang.

2. **Verify correctness** — run the script with and without `--name` and confirm output matches `greeting.py`'s behavior.

## Files to Change

| File | Action | Notes |
|---|---|---|
| `hello.py` | **Replace** (at repo root) | Overwrite the existing file. Drops the local `greet()` in favor of `from greeting import greet`. |

## Risks

- **Import path** — `from greeting import greet` only works when run from the repo root. Running `python3 path/to/hello.py` from elsewhere will fail with `ModuleNotFoundError`. All usage should be from the project root.
- **Argparse default must match greeting.py** — the `--name` default must be `"World"` so bare `python3 hello.py` behaves identically to `python3 greeting.py`.
- **Regression on greeting.py** — `greeting.py` must remain untouched.
- **Existing hello.py on main** — the file already exists from #72; the replacement is intentional and changes the output format from `"Hello from {name}!"` to `"Hello, {name}!`".

## Acceptance Criteria

1. `python3 hello.py` prints `Hello, World!` (uses argparse default, matching `greeting.py`'s default).
2. `python3 hello.py --name Alice` prints `Hello, Alice!`.
3. `python3 hello.py --name "Bob Smith"` prints `Hello, Bob Smith!` (quoted multi-word names work).
4. `python3 hello.py --help` prints a help message describing the `--name` flag.
5. `python3 hello.py --unknown-flag` exits with a non-zero exit code and prints an error.
6. `greeting.py` is not modified.
7. `python3 -c "from greeting import greet; print(greet())"` still works (no import chain breaks).
