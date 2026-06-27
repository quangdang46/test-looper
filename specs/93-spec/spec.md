# Issue #93: Create `hello.py` with `--name` flag

## Objective

Create `hello.py` at the repository root — a Python CLI script using `argparse` with a `--name`/`-n` flag — providing a robust, standardised alternative to the existing `greeting.py` (which uses raw `sys.argv` parsing).

## Background

- The repo contains `greeting.py` (a minimal `sys.argv`-based CLI).
- Commit `48ed356` ("feat: add hello.py with argparse --name support (#72)") attempted to create `hello.py` but landed the file **inside** `.looper/worktrees/worker-*/hello.py` rather than the repo root, making it unreachable via `python hello.py` from the project root.
- That previous version also used a different `greet` signature (`"Hello from {name}!"` with default `"Looper"`) that is inconsistent with `greeting.py`'s `"Hello, {name}!"` / default `"World"`.
- Issue #93 calls for a correct version at the repository root.

## Implementation Plan

### 1. Create `hello.py` at the repository root

Structure:
- Shebang: `#!/usr/bin/env python3`
- Module docstring describing the script
- Function `greet(name: str = "World") -> str` — returns `f"Hello, {name}!"`
- Function `main() -> None` — uses `argparse.ArgumentParser` to define:
  - `parser.add_argument("--name", "-n", default="World", help="Name to greet")`
- Guard: `if __name__ == "__main__": main()`

### 2. Make `hello.py` executable

Run `chmod +x hello.py`.

### 3. Verify the script

| Command | Expected output |
|---------|----------------|
| `python hello.py` | `Hello, World!` |
| `python hello.py --name Alice` | `Hello, Alice!` |
| `python hello.py -n Bob` | `Hello, Bob!` |
| `python hello.py --help` | usage including `--name` / `-n` |

### 4. Regression check

`python greeting.py` must continue to work unchanged.

## Files to Change

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **Create** | New argparse-based CLI script at repo root. |
| `README.md` | **Update** (optional) | Add `hello.py` alongside `greeting.py` for discoverability. |

## Acceptance Criteria

1. `python hello.py` prints `Hello, World!`
2. `python hello.py --name Alice` prints `Hello, Alice!`
3. `python hello.py -n Bob` prints `Hello, Bob!`
4. `python hello.py --help` displays usage showing `--name` / `-n`
5. File has proper shebang and `__main__` guard
6. `python greeting.py` still works identically
