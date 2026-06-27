# Spec: hello.py with argparse `--name` support

Issue: #90

## Objective

Create a standalone `hello.py` script that uses Python's `argparse` module to accept a `--name` flag (defaulting to `"World"`), prints a greeting to stdout, and serves as an idiomatic example of argparse-based CLI input in the project. The existing `greeting.py` achieves the same output via `sys.argv`; `hello.py` should demonstrate the more robust argparse approach while maintaining identical greeting behavior.

## Implementation Plan

1. **Create `hello.py`** — Write a new Python 3 script in the repo root that:
   - Defines `greet(name: str) -> str` returning `f"Hello, {name}!"` (same signature and contract as `greeting.py`).
   - Uses `argparse.ArgumentParser` to define a single optional positional-or-flag argument `--name` with default `"World"`, short alias `-n`, and a help string.
   - Implements a `main()` entry point that parses the args, calls `greet()`, and prints the result.
   - Guards with `if __name__ == "__main__"`.
2. **Verify the script runs** — Execute `python3 hello.py` (prints `Hello, World!`) and `python3 hello.py --name Alice` (prints `Hello, Alice!`).
3. **Run all existing tests** — Confirm no regressions (there are no test files in the repo currently, so this is a manual smoke check against `greeting.py`).

## Files to Change

| File | Action | Description |
|------|--------|-------------|
| `hello.py` | **Create** | New script with argparse `--name` flag, `greet()` function, and `main()` entry point. Uses `argparse` exclusively (no `sys.argv` access). |
| *(no other files need changes)* | | |

## Risks

- **Naming collision with prior commit**: Commit `48ed356` (`feat: add hello.py with argparse --name support (#72)`) declared a file at the same path, but that file is not present in the current working tree. Creating `hello.py` again is safe, but care must be taken that the implementation is correct and complete.
- **Argument semantics**: The `--name` flag should accept a single string value. If positional arguments are also supported, ensure `--name` takes precedence or the two don't conflict. The spec prefers `--name` as an optional flag with `-n` shorthand, rather than a positional argument, to match how `--flags` work in larger CLI tools.
- **Python shebang**: The script should include a `#!/usr/bin/env python3` shebang for direct execution.
- **Cross-script consistency**: `greeting.py` and `hello.py` should produce identical output for the same input (e.g., both output `Hello, World!` and `Hello, Alice!`) so they remain interchangeable.

## Acceptance Criteria

1. `hello.py` exists at the repo root with a `#!/usr/bin/env python3` shebang.
2. `hello.py` defines a `greet(name: str) -> str` function that returns `f"Hello, {name}!"`.
3. `hello.py` uses `argparse.ArgumentParser` to define a `--name`/`-n` flag defaulting to `"World"`.
4. Running `python3 hello.py` prints `Hello, World!`.
5. Running `python3 hello.py --name Alice` prints `Hello, Alice!`.
6. Running `python3 hello.py -n Bob` prints `Hello, Bob!`.
7. Running `python3 hello.py --help` shows usage information including the `--name`/`-n` flag.
8. `greeting.py` continues to work unchanged.
9. The script is executable (`chmod +x hello.py`).

Spec: specs/90-spec/spec.md
