# Spec: Add a simple hello.py script

Issue: [#72](https://github.com/quangdang46/test-looper/issues/72)

## Objective

Create a `hello.py` script that prints `"Hello from Looper!"` by default and accepts an optional `--name` flag via `argparse` to customize the greeting. The script demonstrates proper CLI argument parsing using Python's `argparse` module and provides a greeting format distinct from the existing `greeting.py`.

## Context

- Issue #72 requests a `hello.py` script with `argparse` `--name` support.
- Multiple prior attempts have been made to land this file on `main` (commits `48ed356`, `e3ebc3e`, `5b66224`, `3bd67ef`, etc.), but each was committed on branches that never merged with `main`, so `hello.py` still does not exist on `main`.
- The existing `greeting.py` uses `sys.argv` for argument parsing, defaulting to `"World"` with format `"Hello, {name}!"`. The new script intentionally uses a different greeting format (`"Hello from {name}!"`) and default name (`"Looper"`).

## Implementation Plan

1. **Create `hello.py` at the repo root** — Write a new Python 3 script that:
   - Includes a `#!/usr/bin/env python3` shebang and is made executable (`chmod +x`).
   - Defines `greet(name: str = "Looper") -> str` returning `f"Hello from {name}!"`.
   - Uses `argparse.ArgumentParser` to define an optional `--name` / `-n` flag with default `"Looper"`, type `str`, and a descriptive help string.
   - Implements a `main()` entry point that parses args via `parser.parse_args()`, calls `greet(args.name)`, and prints the result.
   - Guards with `if __name__ == "__main__":`.

2. **Verify the script runs correctly** — Execute and confirm:
   - `python3 hello.py` → `Hello from Looper!`
   - `python3 hello.py --name Alice` → `Hello from Alice!`
   - `python3 hello.py -n Bob` → `Hello from Bob!`
   - `python3 hello.py --help` → shows usage with `--name`/`-n` flag and description

3. **Verify no regressions** — Confirm `greeting.py` still works unchanged:
   - `python3 greeting.py` → `Hello, World!`
   - `python3 greeting.py Alice` → `Hello, Alice!`

4. **Create a PR** to merge into `main` with a clear squashed commit message referencing issue #72.

## Files to Change

| File | Action | Description |
|------|--------|-------------|
| `hello.py` | **Create** | New script with argparse `--name` flag, `greet()` function, and `main()` entry point. |
| *(no other files need changes)* | | |

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
10. A PR is created to merge the changes into `main`.

## Risks

- **Naming collision with prior branches**: Multiple prior branches added `hello.py` but none landed on `main`. No conflict in the working tree.
- **Greeting format differs from `greeting.py`**: This is intentional per the issue requirement (`"Hello from Looper!"` vs `"Hello, World!"`). The two scripts serve as distinct examples of CLI argument handling (argparse vs sys.argv).
- **Python 3 availability**: The script requires `python3`. This is consistent with the existing `greeting.py`.
