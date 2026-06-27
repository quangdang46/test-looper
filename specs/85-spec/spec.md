# Issue #85: hello.py

---
## Objective

Create `hello.py` at the repository root — a Python CLI script with `argparse`-based `--name` flag support — printing the greeting **"Hello from Looper!"** by default. This implements the original intent of PR #72 (commit `48ed356`) with the correct file location, and is distinct from issues #92/#93 which targeted a `"Hello, World!"` output format aligned with `greeting.py`.

The target output format for this issue is:
- Default (no flag): `Hello from Looper!`
- With `--name Alice`: `Hello from Alice!`

## Implementation Plan

1. **Create `hello.py`** at the repository root with the following structure:
   - Shebang line (`#!/usr/bin/env python3`)
   - Module docstring with a brief description
   - A reusable `greet(name: str) -> str` function returning `f"Hello from {name}!"` (the issue's required output format)
   - An `argparse.ArgumentParser` that exposes `--name` / `-n` with default `"Looper"` and a descriptive help string
   - A `main()` entry point that parses args and prints `greet(args.name)`
   - An `if __name__ == "__main__"` guard
   - Make the file executable (`chmod +x hello.py`)

2. **Verify the script works** from the repo root for all key invocations:
   - `python hello.py` → `Hello from Looper!`
   - `python hello.py --name Alice` → `Hello from Alice!`
   - `python hello.py -n Bob` → `Hello from Bob!`
   - `python hello.py --help` displays usage with `--name` / `-n`

3. **Verify `greeting.py` is untouched** — the two scripts coexist independently with different output formats (`greeting.py` produces `"Hello, World!"` / `"Hello, Alice!"`).

## Files to Change

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **Create** | New script at repo root. Output format: `"Hello from {name}!"`. Default name: `"Looper"`. |
| `README.md` | **Update** (optional) | Add a brief entry referencing `hello.py` alongside `greeting.py` so both are discoverable from the project root readme. |

## Risks

- **Cross-contamination with issues #92/#93:** Those issues planned and/or implemented `hello.py` with a `"Hello, World!"` output format that matches `greeting.py`. Issue #85 requires the different `"Hello from Looper!"` format per its issue body. The implementer must follow **this** spec's format and default, not copy from #92/#93's spec or implementation.
- **Location error from PR #72:** The original attempt (commit `48ed356`) wrote `hello.py` inside a `.looper/worktrees/worker-*/` path rather than the repo root. The implementer must ensure the file is created at the repository root **only**, and that no stale copy or symlink is left in a worktree directory.
- **No regression to `greeting.py`:** `greeting.py` must stay untouched. The two scripts are independent and deliberately use different output formats.
- **Stale worktree draft:** A stale `hello.py` with similar content but `"Hello from Looper!"` format exists at `.looper/worktrees/worker-e93bbd78-b73c-43cc-ab68-9b0d52136fd7/hello.py`. It should NOT be copied into the repo root — write a fresh file to avoid any leftover artifacts.
- **No removal of prior worktree artifacts:** Issues #92/#93 may have left planner/worker branches. This implementation should not delete or modify those — they are separate efforts.

## Acceptance Criteria

1. `python hello.py` prints `Hello from Looper!` (default behaviour).
2. `python hello.py --name Alice` prints `Hello from Alice!`.
3. `python hello.py -n Bob` prints `Hello from Bob!` (short flag works).
4. `python hello.py --help` displays a usage message, mentions `--name` / `-n`, and exits with code 0.
5. `python greeting.py` continues to produce `Hello, World!` — its behaviour is unchanged.
6. The file is executable (`chmod +x hello.py`) and begins with a correct shebang.
7. No stale `hello.py` from a worktree path is symlinked or copied — the only `hello.py` at repo root is the new one.
---

Spec: specs/85-spec/spec.md
