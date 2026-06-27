# Issue #92: hello.py

---
## Objective

Create `hello.py` at the repository root — a Python CLI script with `argparse`-based `--name` flag support — providing a robust, standardised alternative to the existing `greeting.py` (which uses raw `sys.argv` parsing). This re-does PR #72's intent, which placed the file inside `.looper/worktrees/worker-*/hello.py` instead of the repo root.

## Implementation Plan

1. **Create `hello.py`** at the repository root with the following structure:
   - Shebang line (`#!/usr/bin/env python3`)
   - Module docstring with a brief description
   - A reusable `greet(name: str) -> str` function returning `f"Hello, {name}!"` (same signature and output format as `greeting.py`)
   - An `argparse.ArgumentParser` that exposes `--name` / `-n` with default `"World"` and a descriptive help string
   - A `main()` entry point that parses args and prints `greet(args.name)`
   - An `if __name__ == "__main__"` guard
2. **Verify the script works** from the repo root for all key invocations (default, named, short flag, `--help`).
3. **Verify `greeting.py` is untouched** — the two scripts coexist independently.

## Files to Change

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **Create** | New script at repo root. Shebang, docstring, `greet()` function, `main()` with `ArgumentParser`, `__main__` guard. |
| `README.md` | **Update** (optional) | Add a short entry referencing `hello.py` alongside `greeting.py` so both are discoverable from the project root readme. |

## Risks

- **Location error from PR #72:** The previous attempt (commit `48ed356`) wrote the file into `.looper/worktrees/worker-e93bbd78-*/hello.py` rather than the repo root. The implementer must ensure the file is created at the repository root **only**, and that no stale copy or symlink is left in a worktree directory.
- **No regression to `greeting.py`:** `greeting.py` must stay untouched. The two scripts are independent but share a common `greet` signature — changes to one must not affect the other.
- **Default name consistency:** The existing worker-worktree draft from PR #72 uses `"Looper"` as the default and `"Hello from {name}!"` as the format. This spec requires `"World"` and `"Hello, {name}!"` to match `greeting.py`'s contract. The implementer should follow the spec, not the stale draft.
- **Short flag ambiguity:** If a future script also uses `-n`, there could be confusion — currently no other script does, so `-n` is safe.

## Acceptance Criteria

1. `python hello.py` prints `Hello, World!` (default behaviour).
2. `python hello.py --name Alice` prints `Hello, Alice!`.
3. `python hello.py -n Bob` prints `Hello, Bob!` (short flag works).
4. `python hello.py --help` displays a usage message, mentions `--name` / `-n`, and exits with code 0.
5. `python hello.py --name` with no argument reports an error (argparse expects a value after `--name`).
6. `python greeting.py` continues to produce the same output as before — its behaviour is unchanged.
7. The file is executable (`chmod +x hello.py`) and begins with a correct shebang.
8. No file named `hello.py` exists anywhere inside `.looper/worktrees/` after the change.
---

Spec: specs/92-spec/spec.md
