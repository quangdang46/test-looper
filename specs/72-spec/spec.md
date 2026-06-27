# Spec: Add a simple hello.py script

## Objective
Create a standalone `hello.py` script that prints a configurable greeting (defaulting to "Hello from Looper!") via `argparse`, implementing the same function signature as the existing `greeting.py` so both scripts share a common API contract.

## Implementation Plan
1. **Create `hello.py`** — Write a new script at the repo root with:
   - Shebang `#!/usr/env/env python3`
   - Module docstring
   - A `greet(name: str) -> str` function identical in signature and return type to `greeting.py`'s `greet()` (returns `f"Hello, {name}!"`)
   - A `main()` function using `argparse.ArgumentParser` with a `--name` flag (default value `"Looper"`) instead of a positional argument
   - `if __name__ == "__main__"` guard

2. **Verify** — Run `python3 hello.py` and confirm it prints "Hello from Looper!"; run `python3 hello.py --name Alice` and confirm it prints "Hello from Alice!"
3. **Update README** — Add a one-line mention of `hello.py` under the existing "Test Looper" header

## Files to Change
| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **Create** | New script at repo root. Uses `argparse` for `--name` flag (default `"Looper"`). Exports `greet(name: str) -> str` matching `greeting.py`'s signature. |
| `README.md` | **Modify** | Add brief mention of `hello.py` alongside `greeting.py`. |

## Risks
- **Argument inconsistency**: `greeting.py` uses `sys.argv` directly with a positional argument; `hello.py` uses `argparse` with `--name`. Users or scripts calling both must understand the different interfaces. Mark clearly in docstrings.
- **Function name clash**: If both scripts are ever imported in the same Python process, the `greet` function definitions would collide. This is acceptable for scripts intended only for CLI use; if `hello.py` is ever imported as a module, `from hello import greet` would shadow the same import from `greeting.py`.
- **Default value mismatch**: `greeting.py` defaults to `"World"`, `hello.py` defaults to `"Looper"`. Not a bug per issue #72, but callers expecting "World" from a similarly-named function should be aware.
- **No test coverage**: This repo currently has no test suite. Manual verification is sufficient for a trivial script, but if tests are added later, both scripts should share a parametrized test.

## Acceptance Criteria
1. `hello.py` exists at the repo root with a shebang line and is executable (`chmod +x hello.py`)
2. Running `python3 hello.py` (with no arguments) prints `Hello from Looper!` to stdout
3. Running `python3 hello.py --name Alice` prints `Hello from Alice!` to stdout
4. Running `python3 hello.py --help` displays usage information including the `--name` flag and its default value
5. The script defines a `greet(name: str) -> str` function — identical in name, parameter, and return type to `greeting.py`'s `greet()`
6. The `greet` function returns a string; it does not call `print()` (I/O is delegated to `main()`)
7. `README.md` is updated with a brief mention of the new script
8. All existing files (`greeting.py`, `README.md`) are unchanged except for the README update

---

Spec: specs/72-spec/spec.md
