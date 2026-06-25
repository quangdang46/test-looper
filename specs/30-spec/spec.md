# Spec: feat: add a simple greeting.py script

**Issue:** [#30](https://github.com/quangdang46/test-looper/issues/30)

## Objective

Add a Python script `greeting.py` that prints `Hello from Looper!` to stdout when executed.

## Implementation Plan

1. Create `greeting.py` in the repository root.
2. Add a `print("Hello from Looper!")` statement.
3. Ensure the script is executable standalone (`python greeting.py`).

## Files to Change

| File | Action | Description |
|------|--------|-------------|
| `greeting.py` | Create | New Python script that prints `Hello from Looper!` |

## Risks

- **None significant.** This is a trivial, self-contained addition with no dependencies or side effects.

## Acceptance Criteria

- `greeting.py` exists in the repository root.
- Running `python greeting.py` prints exactly `Hello from Looper!` followed by a newline to stdout.
- The script contains no external dependencies beyond the Python standard library.

Spec: specs/30-spec/spec.md
