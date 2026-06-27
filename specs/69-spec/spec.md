# Spec: Add `hello.py` script

## Objective
Create a standalone `hello.py` script at the repository root that prints a friendly greeting to stdout. The script follows the same patterns established by the existing `greeting.py` (single-file layout, `if __name__ == "__main__"` guard, simple CLI argument handling) but lives as an independent entry point rather than an alias or wrapper.

## Implementation Plan

1. **Create `hello.py`** at the repository root.
   - Define a `greet(name: str = "World") -> str` function that returns `f"Hello, {name}!"` — intentionally identical in signature and behavior to the one in `greeting.py` so callers get the same result regardless of which module they import.
   - Define a `main() -> None` function that reads an optional command-line name from `sys.argv` and prints the greeting.
   - Guard entry via `if __name__ == "__main__": main()`.
   - Include a shebang (`#!/usr/bin/env python3`) and a module-level docstring.

2. **No changes to `greeting.py` or `README.md`** — this is a greenfield addition only.
   - The two scripts are independent; `hello.py` does not import from `greeting.py`.

3. **Verify the script works.**
   - `python hello.py` → `Hello, World!`
   - `python hello.py Claude` → `Hello, Claude!`

## Files to Change

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **Create** | New 15–20 line Python script at the repo root (see Implementation Plan #1 for exact contents). |

No other files are modified.

## Risks

| Risk | Mitigation |
|------|------------|
| **Fingerprint collision with `greeting.py`** — tests, linters, or other tooling that matches on function name or output string may accidentally pick up `hello.py` instead of `greeting.py` (or vice versa). | Keep `hello.py` self-contained and independent. Neither script imports from the other. |
| **Shebang portability** — `#!/usr/bin/env python3` fails on systems where `python3` is not on `PATH` or does not exist (e.g., minimal containers, Windows without the launcher). | Acceptable for this project; `greeting.py` already uses the same shebang and sets the precedent. |
| **No argument validation** — passing multiple positional args is silently ignored (only `sys.argv[1]` is read). | Acceptable for a simple script; `greeting.py` behaves the same way. |

## Acceptance Criteria

1. **File exists** — `hello.py` is present at the repository root.
2. **Correct default output** — Running `python hello.py` (with no arguments) prints `Hello, World!` followed by a newline, and exits with status 0.
3. **Custom name** — Running `python hello.py Alice` prints `Hello, Alice!` and exits with status 0.
4. **Executable** — The file has a `#!/usr/bin/env python3` shebang and is executable (`chmod +x`).
5. **No side effects** — The existing `greeting.py` is untouched and still passes its own equivalent tests.
6. **Clean import** — `from hello import greet; greet("test")` succeeds and returns `"Hello, test!"`.
7. **All existing tests pass** — Any pre-existing test suite continues to pass (N/A if no suite exists yet).

Spec: specs/69-spec/spec.md
