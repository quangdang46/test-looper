# Spec: feat: add a simple greeting.py script (Issue #30)

## Objective

Create a new Python script `greeting.py` at the repository root that prints the exact string `Hello from Looper!` to standard output when executed, providing a minimal example of a standalone runnable script in the project.

## Implementation Plan

1. Create `greeting.py` in the repository root with a single `print("Hello from Looper!")` statement.
2. Add a shebang line (`#!/usr/bin/env python3`) and make the file executable (`chmod +x greeting.py`) so it can be run directly on Unix-like systems.
3. Verify the script runs correctly with both `python3 greeting.py` and `./greeting.py`.

## Files to Change

| File | Action | Description |
|---|---|---|
| `greeting.py` | **Create** | New Python script that prints `Hello from Looper!` to stdout. Contains shebang line and a single `print` call. |

## Risks

- **Python version**: The script uses `print()` which works on Python 3. No Python 2 compatibility is targeted; if the environment only has Python 2, it will fail. This is acceptable as Python 2 is EOL.
- **Encoding**: The string `Hello from Looper!` is pure ASCII, so no encoding issues are expected across platforms.
- **Executable bit**: On Windows, the `chmod +x` / shebang approach has no effect, but `python3 greeting.py` still works. No cross-platform risk for the core functionality.

## Acceptance Criteria

1. `greeting.py` exists at the repository root.
2. Running `python3 greeting.py` prints exactly `Hello from Looper!` to stdout (with a trailing newline).
3. Running `./greeting.py` on a Unix-like system also prints exactly `Hello from Looper!` to stdout.
4. The file has no external dependencies beyond the Python 3 standard library.
5. The script contains no logic beyond the `print` statement (shebang + print only).

Spec: specs/30-spec/spec.md
