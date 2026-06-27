# Spec: Add hello.py (Issue #85)

## Objective

Create `hello.py` that prints a greeting message with optional `--name` flag, reusing the existing `greet()` function from `greeting.py`.

## Requirements

1. **File**: `hello.py` at the project root.
2. **Behavior**:
   - When run with no arguments, print `Hello, Looper!`
   - When run with `--name Alice`, print `Hello, Alice!`
3. **Implementation pattern**:
   - Import and call `greet()` from `greeting.py` (do not duplicate the greeting logic).
   - Use `argparse` for argument parsing (consistent with prior hello.py implementations #72, #93).
   - Default value for `--name` is `"Looper"`.
   - Include a `main()` function guarded by `if __name__ == "__main__"`.
4. **Style**: Follow the existing conventions in `greeting.py`:
   - Module-level docstring.
   - Type hints on function signatures.
   - Clean, minimal formatting.

## Details

```python
# hello.py — expected structure
#!/usr/bin/env python3
"""...docstring..."""

import argparse
from greeting import greet


def main() -> None:
    """Parse --name and print the greeting."""
    parser = argparse.ArgumentParser(...)
    parser.add_argument("--name", default="Looper", ...)
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
```

## Rationale

- **Reuse `greet()`**: `greeting.py` already provides the canonical greeting function. Duplicating its format string or logic would create a maintenance hazard.
- **argparse over sys.argv**: The last two merged hello.py implementations (#72, #93) both used `argparse`. Consistent CLI UX across the repo.
- **Default "Looper"**: Matches the issue description's "Hello from Looper!" theme while using the existing `greet()` format string `"Hello, {name}!"` which yields `"Hello, Looper!"`.

## Implementation Steps

1. Create `hello.py` at the project root with `argparse`-based `main()`.
2. Import `greet` from `greeting` module.
3. Add `--name` argument with default `"Looper"`.
4. Print `greet(args.name)` from `main()`.
5. Ensure the script is executable (`chmod +x`), matching `greeting.py`'s shebang.
6. Verify: run `python3 hello.py` → `Hello, Looper!`; run `python3 hello.py --name Alice` → `Hello, Alice!`.

## Files Changed

| File | Action |
|------|--------|
| `hello.py` | **Create** — 15–20 lines |
