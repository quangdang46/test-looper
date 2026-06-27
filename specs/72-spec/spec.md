# Issue #72 — Add a simple hello.py script

**Date:** 2026-06-27
**Author:** Generated from Issue #72
**Status:** Draft

---

## 1. Summary

Create a new `hello.py` script that prints `"Hello from Looper!"` with an optional `--name` flag powered by `argparse`. This is a companion to the existing `greeting.py` (which uses `sys.argv`) — `hello.py` demonstrates the same concept using the standard-library `argparse` module.

## 2. Requirements

1. **New file:** `hello.py` at the repository root.
2. **Shebang:** `#!/usr/bin/env python3`
3. **Default output:** When run with no arguments, the script prints:
   ```
   Hello from Looper!
   ```
4. **`--name` flag:** When `--name <value>` is passed, the script prints:
   ```
   Hello from <value>!
   ```
   The flag may be specified as `--name` (long), optionally also `-n` (short).
5. **No positional args:** The script should not accept bare positional arguments. Running with extra unknown flags should produce an `argparse` error.
6. **Module-safe:** The script must be runnable as `python3 hello.py` and also safe to import (i.e. the entry point lives under `if __name__ == "__main__":`).
7. **Consistent style:** Must pass `python3 -m py_compile hello.py` and follow PEP 8 conventions (same style as `greeting.py`).

## 3. Implementation Plan

### 3.1 Create `hello.py`

File: `hello.py`

```python
#!/usr/bin/env python3
"""A simple greeting script using argparse."""

import argparse


def greet(name: str = "Looper") -> str:
    """Return a greeting string for the given name."""
    return f"Hello from {name}!"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Print a greeting."
    )
    parser.add_argument(
        "--name", "-n",
        default="Looper",
        help="Who to greet (default: Looper)"
    )
    return parser.parse_args()


def main() -> None:
    """Parse arguments and print the greeting."""
    args = parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
```

### 3.2 Verify (manual test cases)

| Command | Expected output |
|---|---|
| `python3 hello.py` | `Hello from Looper!` |
| `python3 hello.py --name Alice` | `Hello from Alice!` |
| `python3 hello.py -n Alice` | `Hello from Alice!` |
| `python3 hello.py --name` | argparse error (missing argument) |
| `python3 hello.py positional` | argparse error (unrecognized argument) |
| `python3 -m py_compile hello.py` | Exit code 0 (no syntax errors) |

### 3.3 Edge Cases / Considerations

- **Empty string `--name ''`:** Prints `Hello from !` — acceptable, the caller explicitly passed an empty string. Not a bug.
- **Special characters in name:** They are printed verbatim over stdout (e.g. `--name 'He said "hi"'`) — no injection vector exists in this context. No sanitization needed.
- **Importability:** A `from hello import greet` should work without triggering the print. The `main()` call is guarded by `if __name__ == "__main__":`, so this is satisfied.
- **`.gitignore`:** No changes needed — `hello.py` is a committed source file, not a generated artifact.

### 3.4 Relationship to `greeting.py`

`greeting.py` (existing) uses `sys.argv` directly; `hello.py` uses `argparse`. The two files are independent — no code sharing, no deduplication. Both can coexist as simple examples. Future work could factor the shared `greet()`-style helper into a module, but that's out of scope for this issue.

## 4. Open Questions

- Should `--name` also accept a short form `-n`? (Spec says yes — included above.)
- Should a `--help` flag be supported? (`argparse` provides `-h`/`--help` automatically — no extra work.)
- Should this close with a new test file? (Out of scope for this issue — manual verification is sufficient.)
