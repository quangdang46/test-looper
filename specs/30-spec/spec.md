# Spec: feat: add a simple greeting.py script (#30)

## Objective

Add a Python script `greeting.py` to the repository root that prints `Hello from Looper!` when executed. This provides a minimal executable script to verify the repository's Python workflow and serve as a starting point for further development.

## Implementation Plan

1. **Create `greeting.py`** at the repository root with a single `print("Hello from Looper!")` statement.
2. **Make the script executable** by setting the file mode to `755` and including a `#!/usr/bin/env python3` shebang line.
3. **Verify execution** by running `python3 greeting.py` and confirming the output is exactly `Hello from Looper!`.

## Files to Change

| File | Action | Description |
|------|--------|-------------|
| `greeting.py` | Create | New Python script that prints `Hello from Looper!` when executed. Includes shebang line and the print statement. |

## Risks

- **Encoding issues**: If the file is saved with a BOM or non-UTF-8 encoding, the shebang line may not be recognized on some systems. Ensure the file is plain UTF-8 without BOM.
- **Trailing newline**: A missing trailing newline could cause a warning on some linters or produce inconsistent behavior across shells. The file should end with a single newline.
- **Python version ambiguity**: Using `python3` in the shebang ensures compatibility. Using bare `python` would fail on systems where only `python3` is installed.

## Acceptance Criteria

1. `greeting.py` exists at the repository root.
2. Running `python3 greeting.py` prints exactly `Hello from Looper!` to stdout (no extra whitespace or blank lines before/after).
3. The file contains a `#!/usr/bin/env python3` shebang line.
4. The file is syntactically valid Python (no syntax errors).
5. No existing files are modified or deleted.

---
Spec: specs/30-spec/spec.md
specPath: specs/30-spec/spec.md
