# Issue #74 — Add hello.py script

## Objective
Introduce a new `hello.py` script that serves as a simple, standalone entry point for printing a greeting. The script should mirror the structure of the existing `greeting.py` for consistency, and be wired into the project so it is visible in the repository's file listing and documentation.

## Implementation Plan

1. **Create `hello.py`** — Write a new Python script with the same structure as `greeting.py`:
   - Shebang line: `#!/usr/bin/env python3`
   - Module-level docstring describing the script's purpose.
   - A `greet(name: str) -> str` function (or equivalent) extracted to avoid duplicating logic if feasible; otherwise define a standalone `hello()` function.
   - A `main()` entry point that reads an optional name from `sys.argv` (defaulting to `"World"`) and prints the greeting.
   - An `if __name__ == "__main__"` guard.

2. **Consolidate shared logic (recommended)** — If `greeting.py` and `hello.py` share the core greeting logic, extract the `greet()` function into a shared utility module (e.g., `greet_utils.py`) so both scripts import from it. If the team prefers each script be fully self-contained (for pedagogical reasons), skip this step and document the intentional duplication in each script's docstring.

3. **Update `README.md`** — Add a "Scripts" section that lists both `greeting.py` and `hello.py` with a one-line description of each.

4. **Add basic tests (if test infrastructure exists)** — If the project has a `tests/` directory or a `test_*.py` convention, add a test that invokes `hello.py --name "Alice"` and asserts `"Hello, Alice!"` in stdout.

## Files to Change

| File | Action | Description |
|------|--------|-------------|
| `hello.py` | **Create** | New script with a `main()` entry point that prints a greeting. Follow the conventions of `greeting.py`. |
| `README.md` | **Modify** | Append a "Scripts" section listing both executable scripts. |
| `greeting.py` | **(Optional)** | No changes unless extracting shared logic into a utility module. |

## Risks

- **Duplication drift** — If `hello.py` and `greeting.py` each define their own `greet()` function, a future change to the greeting format will need to update both files. Mitigate by extracting shared logic into a utility module, or call this out as an intentional design choice.
- **Naming confusion** — Having both `greeting.py` and `hello.py` in the same repo may confuse newcomers about which script to use. Mitigate by making `hello.py` a genuine alternative with a slightly different behavior (e.g., default salutation vs. fully customizable), or by documenting the intended use case of each.
- **Shebang portability** — The shebang `#!/usr/bin/env python3` assumes `python3` is on `PATH`. This is standard, but worth verifying on Windows (via WSL) and macOS.

## Acceptance Criteria

1. `hello.py` exists in the repository root and is executable (`chmod +x hello.py`).
2. Running `python3 hello.py` prints `Hello, World!` to stdout.
3. Running `python3 hello.py Alice` prints `Hello, Alice!` to stdout.
4. `README.md` includes a reference to `hello.py` in a "Scripts" section.
5. No existing functionality (`greeting.py`) is broken — running `python3 greeting.py` still produces the same output as before.
6. All existing tests (if any) continue to pass.

---

Spec: specs/74-spec/spec.md
