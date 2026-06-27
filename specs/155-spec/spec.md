# Spec: Add a simple Fibonacci script (Issue #155)

Issue: #155
Spec: specs/155-spec/spec.md

---

## Objective

Add a new `fibonacci.py` script that computes and prints Fibonacci numbers. The script provides a reusable `fibonacci(n)` function and a CLI interface via `argparse` with a `--count` flag controlling how many numbers to print.

## Background

The repository currently has two scripts at the repo root: `greeting.py` (issue #37) and `hello.py` (issue #93). Issue #155 asks for a standalone `fibonacci.py` script following the same conventions — shebang, type annotations, `main()` guard, argparse for CLI arguments, and proper edge-case handling.

Unlike `hello.py` (which reuses `greet()` from `greeting.py`), this script is fully self-contained: there is no existing Fibonacci module to import from.

## Implementation Plan

### Step 1 — Create `fibonacci.py`

Create a new file at the repo root (`/private/tmp/test-looper/fibonacci.py`).

**Structure:**

```python
#!/usr/bin/env python3
"""A simple Fibonacci number generator."""

import argparse


def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number (0-indexed).

    Args:
        n: The index of the Fibonacci number to compute.

    Returns:
        The nth Fibonacci number.

    Raises:
        ValueError: If n is negative.

    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(10)
        55
    """
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def main() -> None:
    """Parse command-line arguments and print Fibonacci numbers."""
    parser = argparse.ArgumentParser(
        description="Print Fibonacci numbers."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="How many Fibonacci numbers to print (default: 10)",
    )
    args = parser.parse_args()
    if args.count < 0:
        parser.error("--count must be non-negative")
    for i in range(args.count):
        print(fibonacci(i))


if __name__ == "__main__":
    main()
```

**Rationale for key choices:**

| Choice | Reason |
|--------|--------|
| `fibonacci(n: int) -> int` signature | Matches the issue's requirement for "a function that returns the nth Fibonacci number." |
| 0-indexed (`fibonacci(0) → 0`, `fibonacci(1) → 1`) | The standard mathematical convention — F(0)=0, F(1)=1. Works naturally with `range(count)` in the CLI loop. |
| Iterative loop (not recursion) | O(n) time, O(1) space. Recursion would be O(2^n) and risk `RecursionError` for larger n. |
| `ValueError` for negative n | Clear error message; consistent with Python's `math` module conventions. |
| `--count` (not positional, not `-n`) | Consistent with `hello.py`'s pattern of named flags. `--count` is self-documenting and avoids confusion with `-n` (negative numbers). |
| Negative `--count` handled by `parser.error()` | argparse exits with a non-zero exit code and prints the error, consistent with how `hello.py --unknown-flag` behaves. No separate check needed. |
| shebang line | Makes the file directly executable (`./fibonacci.py`) for local testing. |
| `__name__ == "__main__"` guard | Allows `fibonacci()` to be imported from other scripts in the future (e.g., a test script or another module). |

### Step 2 — Verify correctness

After writing the file, validate:

```bash
cd /private/tmp/test-looper

# Default invocation (first 10 Fibonacci numbers)
python3 fibonacci.py
# Expected output:
# 0
# 1
# 1
# 2
# 3
# 5
# 8
# 13
# 21
# 34

# Custom count
python3 fibonacci.py --count 5
# Expected:
# 0
# 1
# 1
# 2
# 3

# --count 0 should print nothing
python3 fibonacci.py --count 0
# Expected: (no output)

# --count 1 should print just fibonacci(0)
python3 fibonacci.py --count 1
# Expected:
# 0

# --help flag
python3 fibonacci.py --help
# Expected: shows usage and description

# Negative --count should error
python3 fibonacci.py --count -1
# Expected: exits with non-zero, prints error about --count

# Negative n in fibonacci() via import
python3 -c "from fibonacci import fibonacci; print(fibonacci(-1))"
# Expected: ValueError
```

### Step 3 — Commit and push

```bash
git add fibonacci.py
git commit -m "feat: add fibonacci.py with argparse --count support (#155)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

The commit message follows the repo's existing convention: start with `feat:`, reference the issue with `(#155)`, and include the Claude co-author trailer.

## Files to Change

| File | Action | Notes |
|---|---|---|
| `fibonacci.py` | **Create** (at repo root) | New standalone script with `fibonacci(n)` function and argparse `--count` CLI. |

All other files (`greeting.py`, `hello.py`, `README.md`) remain untouched.

## Acceptance Criteria

1. `python3 fibonacci.py` prints the first 10 Fibonacci numbers (0 through 34), one per line.
2. `python3 fibonacci.py --count 5` prints the first 5 Fibonacci numbers.
3. `python3 fibonacci.py --count 0` prints nothing and exits successfully.
4. `python3 fibonacci.py --count 1` prints `0`.
5. `python3 fibonacci.py --help` prints usage information describing the `--count` flag.
6. `python3 fibonacci.py --count -1` exits with a non-zero exit code and prints a meaningful error.
7. `python3 -c "from fibonacci import fibonacci; print(fibonacci(10))"` outputs `55` (import works, function returns correct value).
8. `python3 -c "from fibonacci import fibonacci; fibonacci(-1)"` raises `ValueError`.
9. Existing scripts (`greeting.py`, `hello.py`) are not modified and continue to work.

## Risks

- **Large `--count` values** — the iterative O(n) loop is fast for reasonable values. For `--count` in the millions, computation will take noticeable time and the output will be very large. This is acceptable for a simple script; no upper bound is enforced.
- **`fibonacci(0)` vs `fibonacci(1)` convention** — some Fibonacci implementations start with `1, 1` (1-indexed). This spec uses the standard 0-indexed convention (`0, 1, 1, 2, ...`) matching the mathematical definition where F(0)=0.
- **No existing test infrastructure** — unlike a project with pytest setup, verification is manual. The acceptance criteria serve as the test suite.
