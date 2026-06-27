# Issue #85 — Add `hello.py`

## Problem

The repository lacks a `hello.py` script. Issue #85 requests a Python script that prints `"Hello from Looper!"` with an optional `--name` flag. A previous attempt (PR #72) wrote the file into a transient worktree path rather than the repo root, so it was never committed to the main branch.

## Goals

1. Create `hello.py` at the repository root.
2. Support both the default greeting and a customizable `--name` flag.
3. Follow the existing code conventions established by `greeting.py` (the sibling script already in the repo).

## Specification

### File location

- `hello.py` at the repository root (next to `greeting.py` and `README.md`).

### Behaviour

| Invocation | Output |
|---|---|
| `python3 hello.py` | `Hello from Looper!` |
| `python3 hello.py --name Alice` | `Hello from Alice!` |
| `python3 hello.py --name "Bob Smith"` | `Hello from Bob Smith!` |

- The default name is `"Looper"` (matching the issue title).
- The flag is `--name` (not `-n` / short form), consistent with argparse best practices for optional string flags.
- Invalid flags (e.g. `--unknown`) must print a usage error and exit non-zero (argparse default behaviour — no special handling needed).

### Code conventions (match `greeting.py`)

- `#!/usr/bin/env python3` shebang.
- Module-level docstring (`"""…"""`).
- Type-annotated standalone `def greet(name: str = …) -> str:` function returning the greeting string, **not** printing it — keeps the function testable and reusable.
- A `def main() -> None:` entry point that parses arguments, calls `greet()`, and `print()`s the result.
- `if __name__ == "__main__": main()` guard.
- Standard library only (no third-party dependencies); `import argparse`.

### Acceptance criteria

1. `python3 hello.py` prints `Hello from Looper!`.
2. `python3 hello.py --name Alice` prints `Hello from Alice!`.
3. `hello.py` is committed at the repository root and present on the `main` branch.
4. The script passes `python3 -m py_compile hello.py` (no syntax/import errors).
5. The script is executable (`chmod +x hello.py`).

## Implementation steps

### Step 1 — Create `hello.py`

Write the file at the repo root following the specification above. The key design choice is to make `greet()` return a string (pure function) so it can be unit-tested independently, while `main()` handles I/O.

### Step 2 — Mark as executable

```bash
chmod +x hello.py
```

### Step 3 — Verify

Run the three invocation forms from the specification and confirm output. Also run `python3 -m py_compile hello.py` to catch syntax errors.

### Step 4 — Commit

```bash
git add hello.py
git commit -m "feat: add hello.py with argparse --name support (#85)"
```

## Risks and considerations

- **No conflict with `greeting.py`**: The two scripts are independent. `hello.py` uses argparse; `greeting.py` uses `sys.argv`. Both coexist as separate utilities.
- **No test framework**: The repo has no test runner yet. The spec keeps `greet()` side-effect-free for easy future testing.
- **Edge cases**: argparse handles `--name` with multiple words (quoted), empty string (allowed), and missing flag (default used). No input validation beyond argparse is needed.
