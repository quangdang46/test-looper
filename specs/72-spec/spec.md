# Issue #72 — Add a simple hello.py script

## Objective
Create a new `hello.py` script at the repository root that prints `"Hello from Looper!"` and supports an optional `--name` flag via `argparse` for customizing the greeting target. This script complements the existing `greeting.py` by demonstrating argparse-based argument handling (as opposed to `sys.argv`).

## Issue Description
> Create a `hello.py` script that prints "Hello from Looper!" with argparse --name flag support.

## Background

The repository currently contains:
- `greeting.py` — A simple script that takes a positional name argument via `sys.argv` and prints `"Hello, {name}!"` (default: `"World"`).
- `README.md` — Minimal file with just `# Test Looper`.

A prior attempt (issue #74 on branch `planner/6c879ac5-…`) produced a spec but the implementation was not completed on `main`. Issue #72 is the successor with a slightly different design: argparse-based flags vs. positional arguments.

## Implementation Plan

### 1. Create `hello.py`

Write a new Python script with the following structure:

- **Shebang**: `#!/usr/bin/env python3`
- **Module-level docstring**: Describe the script's purpose — a greeting script with argparse support.
- **`greet(name: str) -> str` function**: Return a greeting string for the given name. The default greeting is `"Hello from Looper!"`, and when `--name` is provided, it becomes `"Hello from Looper, {name}!"`.
- **`main()` entry point**:
  - Use `argparse.ArgumentParser` with a `--name` / `-n` optional flag (type `str`, default `None`).
  - If `--name` is provided, call `greet(name)` which includes the name in the greeting.
  - If `--name` is omitted, call `greet()` which returns the default `"Hello from Looper!"`.
  - Print the result to stdout.
- **`if __name__ == "__main__"` guard** calling `main()`.

The script should be made executable (`chmod +x hello.py`) and must validate cleanly with both `python3 -m py_compile hello.py` and `flake8` (or the repo's lint tool) if available.

### 2. Update `README.md`

Append a `## Scripts` section that lists both executable scripts with a one-line description of each:

```markdown
## Scripts

- `greeting.py` — Prints "Hello, {name}!" using a positional sys.argv argument (defaults to "World").
- `hello.py` — Prints "Hello from Looper!" with an optional `--name` flag via argparse.
```

### 3. Verify existing functionality is unbroken

Confirm that `greeting.py` still works after the change:
- `python3 greeting.py` → `Hello, World!`
- `python3 greeting.py Alice` → `Hello, Alice!`

## Files to Change

| File | Action | Description |
|------|--------|-------------|
| `hello.py` | **Create** | New argparse-based greeting script. |
| `README.md` | **Modify** | Add a `## Scripts` section listing both scripts. |

## Key Design Decisions

1. **argparse over sys.argv** — The issue explicitly requests `argparse --name` flag support. This contrasts with `greeting.py` which uses raw `sys.argv`. The two scripts serve as parallel examples of different argument-parsing approaches, which is valuable for a test/example repo.

2. **Default message** — `"Hello from Looper!"` when `--name` is not provided; `"Hello from Looper, {name}!"` when `--name` is set. The "from Looper" phrase is the distinctive identifier per the issue.

3. **No shared utility module** — Unlike the prior spec (issue #74), this issue's script has a distinctly different message and argument structure. The overlap is minimal (both print hello-format strings), so extracting shared logic would add complexity without proportional benefit.

## Acceptance Criteria

1. `hello.py` exists at the repository root.
2. `hello.py` is executable (`chmod +x hello.py`).
3. Running `python3 hello.py` prints `Hello from Looper!` to stdout.
4. Running `python3 hello.py --name Alice` prints `Hello from Looper, Alice!` to stdout.
5. Running `python3 hello.py -n Bob` prints `Hello from Looper, Bob!` to stdout (short flag works).
6. `README.md` includes a `## Scripts` section referencing both `greeting.py` and `hello.py`.
7. `greeting.py` still works unchanged — `python3 greeting.py` outputs `Hello, World!`.
8. `python3 -m py_compile hello.py` exits with code 0.

## Risks

- **argparse availability** — `argparse` is part of Python 3's standard library, so this should not be an issue in any modern Python 3 environment. Not relevant for Python 2 (not used by this project).
- **Naming collision** — There should be no existing `hello.py` on `main`. The prior work (issue #74) only landed a spec file, not the script itself. Verify the file does not exist before creating.
- **Shebang portability** — `#!/usr/bin/env python3` assumes `python3` is on `PATH`. This is standard across macOS and Linux.

---

Spec: specs/72-spec/spec.md
