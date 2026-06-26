---
issue: 30
title: "feat: add a simple greeting.py script"
status: draft
---

## Objective

Add a simple, runnable `greeting.py` script to the project that prints a configurable greeting message. The script should accept a name as an optional command-line argument, default to a sensible fallback when none is provided, and follow minimal best practices for a Python CLI script (shebang, `if __name__ == "__main__"` guard, clean exit code).

## Implementation Plan

1. **Create `greeting.py`** at the repository root.
   - Add a `#!/usr/bin/env python3` shebang.
   - Use `argparse` (or `sys.argv`) to accept an optional `--name` argument.
   - Print `"Hello, <name>!"` to stdout when `--name` is provided.
   - Print `"Hello, World!"` as the default when `--name` is omitted.
   - Include an `if __name__ == "__main__"` guard.
   - Exit with code 0 on success.

2. **Make `greeting.py` executable** (`chmod +x greeting.py`).

3. **Verify** the script runs correctly via both `python3 greeting.py` and `./greeting.py`, with and without the `--name` flag.

4. **Commit** the new file with a descriptive commit message referencing issue #30.

## Files to Change

| File | Action | Description |
|------|--------|-------------|
| `greeting.py` | Create | New Python script that prints a configurable greeting. |

## Risks

- **No Python interpreter**: If Python 3 is not installed on the target system, the script will fail with a missing-interpreter error. Mitigation: document the Python 3 requirement in the script's docstring or a README note.
- **Missing shebang**: If the executable bit is set but the shebang is missing, `./greeting.py` will fail on some systems. Mitigation: ensure the shebang is the very first line.
- **Windows compatibility**: On Windows the shebang is ignored and `./greeting.py` won't work directly; users must run `python greeting.py`. Mitigation: out of scope for this issue — document as a known limitation if desired.
- **Argument parsing edge cases**: Empty string `--name ""` should be handled gracefully (print `"Hello, !"` or treat as missing). Fix: argparse's `type=str` handles this by default; no special case needed.
- **File encoding**: Ensure UTF-8 encoding is declared or relied upon for any non-ASCII names. Mitigation: Python 3 defaults to UTF-8; no explicit encoding declaration needed for ASCII-compatible names, but a `# -*- coding: utf-8 -*-` comment can be added proactively.

## Acceptance Criteria

- [ ] `greeting.py` exists at the repository root with a `#!/usr/bin/env python3` shebang.
- [ ] `python3 greeting.py` prints `"Hello, World!"` to stdout and exits with code 0.
- [ ] `python3 greeting.py --name Alice` prints `"Hello, Alice!"` to stdout and exits with code 0.
- [ ] `./greeting.py` (after `chmod +x`) behaves identically to the `python3 greeting.py` invocations above.
- [ ] The file contains an `if __name__ == "__main__"` guard so that importing the module does not trigger the CLI path.
- [ ] The script produces no output on stderr when invoked correctly.
- [ ] No existing files are modified.

---

Spec: specs/30-spec/spec.md
