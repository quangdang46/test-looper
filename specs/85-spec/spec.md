# Issue #85: Add hello.py

## Objective
Add a new `hello.py` script that prints `"Hello from Looper!"` and supports an optional `--name` flag to customize the greeting. This provides a second, independently-running script alongside the existing `greeting.py`, demonstrating a different CLI style (flags via `argparse` vs. positional args via `sys.argv`).

## Implementation Plan
1. **Create `hello.py`** with a `main()` entry point that uses `argparse` to parse an optional `--name` flag, defaulting to `"Looper"`.
2. **Keep existing `greeting.py` untouched** — the two scripts coexist and use different CLI conventions.
3. **Verify** the script is executable and produces correct output for the default case and the `--name` override.

## Files to Change
- **`hello.py`** (create) — New script with `#!/usr/bin/env python3` shebang, `argparse`-based `--name` flag, default message `"Hello from Looper!"`, and a `if __name__ == "__main__": main()` guard.

No other files require modification.

## Risks
- **Naming confusion**: `hello.py` and `greeting.py` serve a similar purpose. Ensure they remain independent rather than one importing the other. If the intent is to eventually replace `greeting.py`, note that in the code review; for now they should coexist.
- **Argument convention mismatch**: `greeting.py` uses positional `sys.argv[1]`; `hello.py` uses `--name` flag. A user expecting one convention from the other script may be briefly surprised, but this is intentional diversity for demonstration.
- **Executable bit**: The file must have the executable permission set (`chmod +x`) to match `greeting.py`'s convention.

## Acceptance Criteria
- [ ] `python hello.py` outputs `"Hello from Looper!"`.
- [ ] `python hello.py --name Alice` outputs `"Hello, Alice!"`.
- [ ] `./hello.py` works (executable bit set) and produces the same output as the `python` invocation.
- [ ] `greeting.py` continues to work exactly as before (regression check: `python greeting.py` → `"Hello, World!"`, `python greeting.py Alice` → `"Hello, Alice!"`).
- [ ] No existing tests break (if any are added in the future, this spec should be revisited to add test entries).

---

Spec: specs/85-spec/spec.md
