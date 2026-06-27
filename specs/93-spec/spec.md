# Issue #93: hello.py

---
## Objective

Add `hello.py` to the repository root — a Python CLI script with `argparse`-based `--name` support — providing a more robust, standardised alternative to the existing `greeting.py` script (which uses raw `sys.argv` parsing).

## Implementation Plan

1. **Create `hello.py`** at the repository root with the following structure:
   - Shebang line (`#!/usr/bin/env python3`)
   - Docstring with a brief description
   - A reusable `greet(name: str) -> str` function (consistent with the signature already used by `greeting.py`)
   - An `argparse.ArgumentParser` that exposes `--name` / `-n` (default: `"World"`)
   - A `main()` entry point that parses args and prints `greet(name)`
   - An `if __name__ == "__main__"` guard
2. **Verify** the script is executable and produces correct output for the default case, a named case, the short flag, and `--help`.
3. **Verify** `greeting.py` continues to work unchanged — the two scripts are independent but share a common `greet` concept.

## Files to Change

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **Create** | New script with argparse `--name` support. Shebang, docstring, `greet()` function, `main()` with `ArgumentParser`, `__main__` guard. |
| `README.md` | **Update** (optional) | Add a brief entry listing `hello.py` alongside `greeting.py` so both scripts are discoverable from the project root readme. |

## Risks

- **Name collision with previous attempt (PR #72):** Commit `48ed356` attempted to create `hello.py` but placed it inside a worker worktree path (`.looper/worktrees/worker-*/hello.py`) rather than the repo root. The implementer must ensure the file lands at the repository root **only**, and that no stale copy remains in a worktree path.
- **No regression to `greeting.py`:** `greeting.py` must stay untouched; the new script lives alongside it.
- **Argparse mismatch with convention:** If surrounding scripts (future) adopt a different CLI style, `hello.py` should remain consistent with *this* spec's stated design. No existing scripts to conflict with at this time.

## Acceptance Criteria

1. `python hello.py` prints `Hello, World!` (default behaviour).
2. `python hello.py --name Alice` prints `Hello, Alice!`.
3. `python hello.py -n Bob` prints `Hello, Bob!` (short flag works).
4. `python hello.py --help` displays a usage message showing `--name` / `-n`.
5. Running `python greeting.py` (the existing script) still produces the same output as before — its behaviour is unchanged.
6. The file is executable (`chmod +x hello.py` and/or proper shebang).
---

Spec: specs/93-spec/spec.md
