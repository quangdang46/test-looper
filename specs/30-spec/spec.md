# Issue #30 — Add a simple greeting.py script

## Objective

Create a standalone `greeting.py` script that prints a configurable greeting message. The script should accept a name as an optional command-line argument, default to `"World"` when none is provided, and follow Python best practices (shebang, `if __name__ == "__main__"` guard, clean exit code).

## Implementation Plan

1. **Create `greeting.py`** — Write the script at the repo root with:
   - A `#!/usr/bin/env python3` shebang.
   - A `def greet(name: str = "World") -> str` function that returns the formatted greeting string `"Hello, {name}!"`.
   - An `if __name__ == "__main__"` block that parses the first CLI argument via `sys.argv` (or `argparse` for extensibility) and prints the result of `greet(...)`.
   - Exit code 0 on success.

2. **Make the script executable** — Run `chmod +x greeting.py` so it can be invoked directly as `./greeting.py`.

3. **Verify with a quick smoke test** — Confirm that:
   - `python greeting.py` prints `Hello, World!`.
   - `python greeting.py Alice` prints `Hello, Alice!`.

## Files to Change

| File | Action | Notes |
|------|--------|-------|
| `greeting.py` | **Create** | New Python script with `greet()` function and CLI entry point. |

No other files need modification. The existing `README.md` is left untouched; `greeting.py` documents itself through its code.

## Risks

- **Python version mismatch**: The script uses type hints (`str`), which require Python 3.5+. This is acceptable for any modern Python 3 installation, but should be noted if the project targets Python 2.
- **Name collision**: `greeting.py` is a reasonably generic name; unlikely to collide with existing project files, but worth checking before creating.
- **Edge cases**: Empty string `""` or strings with special characters (spaces, Unicode) as the name argument. The implementation should handle these gracefully — spaces work natively with `sys.argv`, and the template string `f"Hello, {name}!"` handles any string content. No sanitization is needed for a simple greeting.

## Acceptance Criteria

- [ ] `greeting.py` exists and is executable (`chmod +x`).
- [ ] Running `./greeting.py` (or `python greeting.py`) outputs `Hello, World!` to stdout and exits with code 0.
- [ ] Running `./greeting.py Alice` outputs `Hello, Alice!` to stdout and exits with code 0.
- [ ] Running `./greeting.py ""` outputs `Hello, !` (empty name is treated as-is, no crash).
- [ ] The `greet()` function is importable from other Python modules (e.g., `from greeting import greet`).
- [ ] The script raises no unhandled exceptions for any number of CLI arguments (0, 1, or many — extra arguments beyond the first are ignored).

---

Spec: specs/30-spec/spec.md
