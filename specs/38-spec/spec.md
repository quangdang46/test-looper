---
issue: 38
title: "feat: add a goodbye.py script"
status: draft
---

## Objective

Add a simple, runnable `goodbye.py` script to the project that prints a "Goodbye from Looper!" message when executed. The script should follow the same pattern as the existing `greeting.py` script and comply with Python CLI best practices (shebang, `if __name__ == "__main__"` guard, clean exit code). It should accept a custom name as an optional argument for personalization.

## Implementation Plan

1. **Create `goodbye.py`** at the repository root.
   - Add a `#!/usr/bin/env python3` shebang.
   - Use `sys.argv` to accept an optional `--name` or positional argument.
   - Print `"Goodbye from <name>!"` when `--name` is provided.
   - Print `"Goodbye from Looper!"` as the default when no name is provided.
   - Include an `if __name__ == "__main__"` guard.
   - Exit with code 0 on success.

2. **Make `goodbye.py` executable** (`chmod +x goodbye.py`).

3. **Verify** the script runs correctly via both `python3 goodbye.py` and `./goodbye.py`, with and without the name argument.

4. **Commit** the new file with a descriptive commit message referencing issue #38.

## Files to Change

| File | Action | Description |
|------|--------|-------------|
| `goodbye.py` | Create | New Python script that prints "Goodbye from Looper!" by default. |

## Risks

- **No Python interpreter**: If Python 3 is not installed on the target system, the script will fail with a missing-interpreter error. Mitigation: include the shebang and ensure the file is executable; document Python 3 requirement in the docstring.
- **Missing shebang**: Without the shebang, `./goodbye.py` will fail on Unix-like systems. Mitigation: ensure the shebang is the first line.
- **Argument parsing issues**: Empty string `--name ""` should be handled gracefully (prints "Goodbye from !" or falls back to default). Mitigation: add validation in the argument parsing logic.
- **File encoding**: Ensure UTF-8 encoding for any non-ASCII names. Mitigation: rely on Python 3's default UTF-8 support.
- **Permissions**: If `chmod +x` fails or the file permissions are incorrect, users must run via `python3 goodbye.py`. Mitigation: document both execution methods.

## Acceptance Criteria

- [ ] `goodbye.py` exists at the repository root with a `#!/usr/bin/env python3` shebang.
- [ ] `python3 goodbye.py` prints `"Goodbye from Looper!"` to stdout and exits with code 0.
- [ ] `python3 goodbye.py --name Alice` prints `"Goodbye from Alice!"` to stdout and exits with code 0.
- [ ] `./goodbye.py` (after `chmod +x`) behaves identically to the `python3 goodbye.py` invocations above.
- [ ] The file contains an `if __name__ == "__main__"` guard so that importing the module does not trigger the CLI path.
- [ ] The script produces no output on stderr when invoked correctly.
- [ ] No existing files are modified.

---

Spec: specs/38-spec/spec.md