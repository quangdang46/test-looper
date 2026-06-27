# Spec: Add `hello.py` with argparse `--name` support

**Issue**: #72 | **Repository**: quangdang46/test-looper | **Status**: `planning`

---

## Objective

Create a standalone `hello.py` script at the repo root that prints `"Hello from Looper!"` by default and accepts an optional `--name` / `-n` flag via `argparse` to customize the greeting. This script serves as a second CLI argument-parsing example alongside the existing `greeting.py`, demonstrating Python's `argparse` module with a different greeting format and default name.

## Context

- **Issue #72** requests: *"Create a `hello.py` script that prints 'Hello from Looper!' with argparse --name flag support."*
- **Existing `greeting.py`** (commit `217e6e7`) uses `sys.argv` for argument parsing with default `"World"` and format `"Hello, {name}!"`.
- **Prior attempt** — Commit `48ed356` (`feat: add hello.py with argparse --name support (#72)`) added `hello.py` but committed it inside a worktree subdirectory (`.looper/worktrees/.../hello.py`), not the repo root. The file no longer exists on `main`. This spec ensures `hello.py` lands at the correct path.
- The greeting format `"Hello from {name}!"` distinguishes this script from `greeting.py` (`"Hello, {name}!"`), per the issue requirement.

## Implementation Plan

### Step 1: Create `hello.py`

Write a new Python 3 script in the repo root with the following structure:

- **Shebang**: `#!/usr/bin/env python3`
- **Docstring**: Module-level docstring describing the script.
- **`greet(name: str = "Looper") -> str`**: Returns `f"Hello from {name}!"`.
- **`main() -> None`**: Uses `argparse.ArgumentParser` to define:
  - Optional `--name` / `-n` flag with default `"Looper"` and help text `"Name to greet (default: Looper)"`.
  - Parses args, calls `greet(args.name)`, prints the result.
- **Entry guard**: `if __name__ == "__main__": main()`.
- **File mode**: Make the script executable (`chmod +x hello.py`).

### Step 2: Verify `hello.py` behavior

Run the following checks in the repo root:

| Command | Expected output |
|---------|----------------|
| `python3 hello.py` | `Hello from Looper!` |
| `python3 hello.py --name Alice` | `Hello from Alice!` |
| `python3 hello.py -n Bob` | `Hello from Bob!` |
| `python3 hello.py --help` | Usage including `--name`/`-n` flag description |

### Step 3: Verify no regressions

Confirm `greeting.py` still works unchanged:

| Command | Expected output |
|---------|----------------|
| `python3 greeting.py` | `Hello, World!` |
| `python3 greeting.py Alice` | `Hello, Alice!` |

### Step 4: Commit and push

- `git add hello.py`
- `git commit -m "feat: add hello.py with argparse --name support (#72)"`
- `git push`

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `hello.py` | **Create** | New script with argparse `--name`/`-n` flag, `greet()` function returning `"Hello from {name}!"` with default `"Looper"`, and `main()` entry point. |
| *(no other files)* | — | All changes isolated to the new file. |

## Acceptance Criteria

1. `hello.py` exists at the repo root with a `#!/usr/bin/env python3` shebang.
2. `hello.py` is executable (`chmod +x hello.py`).
3. `hello.py` defines `greet(name: str = "Looper") -> str` returning `f"Hello from {name}!"`.
4. `hello.py` uses `argparse.ArgumentParser` to define a `--name` / `-n` flag defaulting to `"Looper"`.
5. Running `python3 hello.py` prints `Hello from Looper!`.
6. Running `python3 hello.py --name Alice` prints `Hello from Alice!`.
7. Running `python3 hello.py -n Bob` prints `Hello from Bob!`.
8. Running `python3 hello.py --help` shows usage information including the `--name` / `-n` flag.
9. `greeting.py` continues to work unchanged (default: `Hello, World!`, with positional arg: `Hello, Alice!`).

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| **Naming collision** — Commit `48ed356` previously created `hello.py` in a worktree path. | The file was never merged into `main` at the repo root. No conflict. |
| **Greeting format confusion** — `"Hello from {name}!"` differs from `greeting.py`'s `"Hello, {name}!"`. | This is intentional per the issue. The two scripts serve as distinct CLI argument-parsing examples. |
| **Python 3 availability** — Script requires `python3`. | Consistent with `greeting.py`'s requirements. CI/development environments already have `python3`. |
| **Overlap with existing scripts** — `hello.py` name is generic and could conflict with other project scripts. | No other files named `hello.py` exist in the repo. The name matches the issue title. |
