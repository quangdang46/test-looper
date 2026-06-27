# Spec: hello.py — Issue #87

## Objective

Create `hello.py` as a standalone script at the repo root that prints `"Hello from Looper!"` by default, with an optional `--name` flag to customize the greeting. This mirrors the structure of the existing `greeting.py` while introducing proper `argparse` usage.

## Implementation Plan

1. **Create `hello.py`** at the repo root.
   - Shebang (`#!/usr/bin/env python3`), module docstring.
   - `greet(name: str = "Looper") -> str` function returning `f"Hello from {name}!"`.
   - `main()` function:
     - `argparse.ArgumentParser(description="Print a greeting.")`.
     - `--name` argument with `type=str`, `default="Looper"`, help text.
     - `print(greet(args.name))`.
   - `if __name__ == "__main__": main()` guard.

2. **Verify** the script runs correctly in isolation:
   - `python hello.py` → `Hello from Looper!`
   - `python hello.py --name Alice` → `Hello from Alice!`
   - `python hello.py --help` prints the help text.

3. **No other files** need modification — `greeting.py`, `README.md`, and existing tests are unrelated and should not be touched.

## Files to Change

| File | Action | Change |
|------|--------|--------|
| `hello.py` | **Create** | New script with `argparse --name` support, default name "Looper", greeting format `"Hello from {name}!"`. |

## Risks

- **Name collision**: `hello.py` does not exist at the root today, so no collision risk. However, `greeting.py` already exists with a similar purpose. The two scripts should remain independent and not share code to avoid coupling.
- **Existing worker worktree**: A copy of `hello.py` already exists at `.looper/worktrees/worker-e93bbd78-b73c-43cc-ab68-9b0d52136fd7/hello.py` (committed as part of PR #72 but never merged to main). Care must be taken not to treat the worker worktree copy as authoritative — the spec file defines the canonical requirements.
- **Argparse exclusive group**: If `--name` is given an empty string (`--name ""`), the script should print `"Hello from !"` — this is acceptable behavior. No validation beyond `argparse` defaults is required.

## Acceptance Criteria

- [ ] `hello.py` exists at the repo root with `#!/usr/bin/env python3` shebang.
- [ ] `python hello.py` prints `Hello from Looper!` (with a trailing newline).
- [ ] `python hello.py --name Alice` prints `Hello from Alice!`.
- [ ] `python hello.py --name` with no value exits with a `argparse.ArgumentError`-style error message (argparse default behavior).
- [ ] `python hello.py --help` displays the description and `--name` flag with its default and help text.
- [ ] `python hello.py --name "` behaves as argparse normally would (error, no crash).
- [ ] `greeting.py` is completely unchanged.
- [ ] All existing files remain unmodified.

Spec: specs/87-spec/spec.md
