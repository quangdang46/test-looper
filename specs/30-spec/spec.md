# Spec: feat: add a simple greeting.py script

**Issue**: #30
**Author**: @quangdang46
**Date**: 2026-06-25

---

## Objective

Add a Python script `greeting.py` to the repository root that prints `Hello from Looper!` to stdout when executed.

## Implementation Plan

1. **Create `greeting.py`** at the repository root with a single `print()` statement outputting `Hello from Looper!`.
2. **Verify** the script runs correctly with `python greeting.py`.

## Files to Change

| File | Action | Description |
|------|--------|-------------|
| `greeting.py` | **Create** | New Python script that prints `Hello from Looper!` |

## Risks

- **Python version ambiguity**: The script uses only a plain `print()` call, which works on Python 2.7+ and 3.x. No version-specific risk.
- **Execution permissions**: No need to add a shebang or `chmod +x` unless explicitly requested; the spec calls for execution via `python greeting.py`.

## Acceptance Criteria

- `greeting.py` exists at the repository root.
- Running `python greeting.py` prints exactly `Hello from Looper!` to stdout with a trailing newline and exits with code 0.
- No other files are modified or created.

---

Spec: specs/30-spec/spec.md
