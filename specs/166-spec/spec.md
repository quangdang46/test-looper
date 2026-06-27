# Spec: Add a Prime Number Checker Script (Issue #166)

## Problem

**Issue #166** asks for an executable `isprime.py` script that checks whether a given integer is a prime number. The script must provide a reusable `is_prime(n)` function and a CLI interface via `argparse` with a required `--number` flag. Edge cases (negative numbers, 0, 1, very large numbers) must be handled correctly.

## Goals

1. Create an executable `isprime.py` at the repo root.
2. Implement a pure `is_prime(n: int) -> bool` function with correct primality logic.
3. Use `argparse` with a required `--number` flag for the CLI interface.
4. Handle edge cases: negative numbers → `False`, 0 → `False`, 1 → `False`, very large numbers efficiently.
5. Follow the project's existing conventions: shebang, `main()` function, `if __name__ == "__main__":` guard.

## Non-goals

- No changes to `greeting.py`, `hello.py`, or any other existing files.
- No packaging / `setup.py` / `pyproject.toml`.
- No import of external libraries beyond Python's standard library.
- No GUI, web server, or interactive read-eval loop — pure CLI.
- No unit test framework integration in this issue; the function signature is designed to be testable.

---

## Implementation Steps

### Step 1 — Create `isprime.py`

Create a new file `isprime.py` at the repo root.

**Structure:**

```python
#!/usr/bin/env python3
"""A prime number checker script."""

import argparse
import math


def is_prime(n: int) -> bool:
    """Return True if n is a prime number, False otherwise.

    Handles edge cases:
    - n <= 1 → False (primes are defined as > 1)
    - n == 2 → True (the only even prime)
    - n is even and > 2 → False
    - Composite odd numbers → False
    - Very large primes → True (tested efficiently up to sqrt(n))
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # Check divisors from 3 up to sqrt(n), stepping by 2 (odd-only)
    limit = int(math.isqrt(n))
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return False
    return True


def main() -> None:
    """Parse command-line arguments and print the primality result."""
    parser = argparse.ArgumentParser(
        description="Check if a number is prime."
    )
    parser.add_argument(
        "--number",
        type=int,
        required=True,
        help="Integer to check for primality",
    )
    args = parser.parse_args()
    print(is_prime(args.number))


if __name__ == "__main__":
    main()
```

**Rationale for key choices:**

| Choice | Reason |
|--------|--------|
| `math.isqrt(n)` for the loop bound | Avoids floating-point precision issues from `math.sqrt(n)` on very large integers. `isqrt` returns the exact integer floor of the square root. |
| Odd-only trial division | After handling 2 separately, only odd candidates need to be checked — halves the search space. |
| `required=True` on `--number` | The issue explicitly says the `--number` flag is required. `argparse` enforces this automatically and prints a clear error + usage message. |
| `type=int` on `--number` | `argparse` validates the input is a valid integer and rejects non-numeric input with a clear error before `main` even calls `is_prime`. |
| Return `False` for `n <= 1` | By definition, primes are integers greater than 1. This correctly covers negative numbers, 0, and 1 in a single condition. |

**Performance characteristics:**

The algorithm is O(√n) trial division restricted to odd numbers. For the expected use cases (CLI invocation), this is more than adequate. A 10-digit prime would complete in microseconds; a 12-digit prime completes in milliseconds. For cryptographic-scale numbers (hundreds of digits) a probabilistic test would be needed, but that is outside the scope of this issue.

### Step 2 — Verify correctness

After writing the file, validate with these test cases:

```bash
cd /private/tmp/test-looper-review/.looper/worktrees/worker-ba6db725-21e3-426a-8490-8841e02f6e70

# Edge cases — all should print False
python3 isprime.py --number -5    # → False (negative)
python3 isprime.py --number 0     # → False (zero)
python3 isprime.py --number 1     # → False (by definition)

# Small primes — should print True
python3 isprime.py --number 2     # → True
python3 isprime.py --number 3     # → True
python3 isprime.py --number 5     # → True
python3 isprime.py --number 7     # → True
python3 isprime.py --number 11    # → True
python3 isprime.py --number 13    # → True

# Small composites — should print False
python3 isprime.py --number 4     # → False
python3 isprime.py --number 6     # → False
python3 isprime.py --number 8     # → False
python3 isprime.py --number 9     # → False
python3 isprime.py --number 10    # → False

# Large prime — should print True
python3 isprime.py --number 104729      # → True (10,000th prime)
python3 isprime.py --number 1299709     # → True (100,000th prime)

# Large composite — should print False
python3 isprime.py --number 104727      # → False (104727 = 3 × 7 × 4987)
python3 isprime.py --number 1000000     # → False (even, > 2)

# Error cases
python3 isprime.py                     # → error: --number is required
python3 isprime.py --number abc        # → error: invalid int value
python3 isprime.py --help              # → shows help text
```

### Step 3 — Commit and push

```bash
git add isprime.py
git commit -m "feat: add isprime.py with is_prime() and argparse --number flag (#166)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

The commit message follows the repo's existing convention (see prior commits for #72 and #93): start with `feat:`, reference the issue with `(#166)`, and include the Claude co-author trailer.

---

## Files touched

| File | Action |
|------|--------|
| `isprime.py` | **CREATE** — executable Python script using shebang |

## Backward compatibility

No breaking changes. All existing files (`greeting.py`, `hello.py`) are untouched and work exactly as before.

## Edge-case reference

| Input | Expected result | Why |
|-------|----------------|-----|
| `-5` | `False` | Negative numbers are not prime |
| `0` | `False` | 0 is not prime (definition requires n > 1) |
| `1` | `False` | 1 is not prime (definition requires n > 1) |
| `2` | `True` | The smallest and only even prime |
| Large prime (e.g. 104729) | `True` | Must handle efficiently via trial division up to √n |
| Large composite (e.g. 1000000) | `False` | Early exit on even check (even > 2 → False) |
