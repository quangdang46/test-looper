# Spec: Add a prime number checker script (Issue #166)

**Issue:** #166
**Created:** 2026-06-27
**Status:** Planned

---

## Problem

**Issue #166** asks for a new Python script `isprime.py` that checks whether a given number is prime. The script should be CLI-driven via `argparse` with a `--number` flag, handle edge cases (negative numbers, 0, 1, very large numbers), and follow the same project conventions as the existing `greeting.py` and `hello.py`.

## Goals

1. Create an executable `isprime.py` at the repo root.
2. Implement `is_prime(n: int) -> bool` returning `True` if `n` is prime, `False` otherwise.
3. Use `argparse` for CLI parsing with a required `--number` flag.
4. Handle edge cases properly: negative numbers, 0, and 1 all return `False`.
5. Handle very large numbers (up to Python's arbitrary integer precision) efficiently using trial division up to `sqrt(n)`.
6. Include a `main()` function with `if __name__ == "__main__"` guard and shebang.
7. Keep existing files (`greeting.py`, `hello.py`) unchanged.

## Non-goals

- No changes to `greeting.py`, `hello.py`, or any other existing files.
- No Sieve of Eratosthenes or advanced primality tests — trial division up to `√n` is sufficient for this issue.
- No packaging / `setup.py` / `pyproject.toml`.
- No input validation beyond what `argparse` provides for `--number` (accepts any integer).

---

## Implementation Steps

### Step 1 — Create `isprime.py`

Create a new file `isprime.py` at the repo root.

**Structure:**

```python
#!/usr/bin/env python3
"""A prime number checker."""

import argparse
import math


def is_prime(n: int) -> bool:
    """Return True if n is a prime number, False otherwise.

    Handles edge cases: negative numbers, 0, and 1 all return False.
    Uses trial division up to sqrt(n) for efficiency with large numbers.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = int(math.isqrt(n))
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return False
    return True


def main() -> None:
    """Parse command-line arguments and print whether the number is prime."""
    parser = argparse.ArgumentParser(
        description="Check if a number is prime."
    )
    parser.add_argument(
        "--number",
        type=int,
        required=True,
        help="Number to check for primality",
    )
    args = parser.parse_args()
    print(is_prime(args.number))


if __name__ == "__main__":
    main()
```

**Rationale for key choices:**

| Choice | Reason |
|--------|--------|
| `required=True` on `--number` | Issue #166 says the `--number` flag is required. Makes the contract explicit — no silent default. |
| `type=int` | `argparse` converts the string to an `int`, rejecting non-integer input automatically. |
| `n < 2` as first guard | Negative numbers, 0, and 1 are all composite by definition — one check covers all edge cases from the spec. |
| Early even-number return `n % 2 == 0` | Immediately excludes all even numbers > 2, roughly halving the trial-division loop work. |
| `math.isqrt(n)` | Integer square root avoids floating-point precision issues for very large numbers (bigger than 2⁵³ where `math.sqrt` loses precision). |
| `range(3, limit + 1, 2)` | Steps by 2 — only checks odd divisors after the initial even check. |
| shebang line | Makes the file directly executable (`./isprime.py`), matching project conventions. |
| `__name__ == "__main__"` guard | Allows `is_prime()` to be imported from other scripts or tests if needed. |

### Step 2 — Verify correctness

After writing the file, validate with the following test cases:

```bash
cd /private/tmp/test-looper-review

# Edge cases — all should print False
python3 isprime.py --number -5    # → False (negative)
python3 isprime.py --number 0     # → False
python3 isprime.py --number 1     # → False

# Non-prime small numbers
python3 isprime.py --number 4     # → False (even)
python3 isprime.py --number 9     # → False (odd composite)
python3 isprime.py --number 100   # → False

# Prime small numbers
python3 isprime.py --number 2     # → True (smallest prime)
python3 isprime.py --number 3     # → True
python3 isprime.py --number 7     # → True
python3 isprime.py --number 11    # → True

# Large prime (should not be too slow with trial division)
python3 isprime.py --number 104729    # → True (10000th prime)
python3 isprime.py --number 104743    # → True (10001st prime)

# Very large number (tests isqrt precision for big ints)
python3 isprime.py --number 982451653    # → True (50 millionth prime)
python3 isprime.py --number 982451651    # → False (nearby composite)

# Help
python3 isprime.py --help
```

**Why these test cases:**
- Negative, 0, 1 — the three edge cases from the issue requirements, each hitting `n < 2` return path.
- 2 — the smallest prime and the only even prime (early `n == 2` return).
- 4 — first even composite (early `n % 2 == 0` return).
- 9 — first odd composite (enters the trial loop at `i=3` then `9 % 3 == 0`).
- 7 — the example from the issue (`--number 7` → `True`).
- 104729 — moderately large prime to verify loop correctness.
- 982451653 — 50 millionth prime, tests that `math.isqrt` works correctly for large integers.

### Step 3 — Commit and push

```bash
cd /private/tmp/test-looper-review
git add isprime.py
git commit -m "feat: add isprime.py with is_prime() and argparse --number flag (#166)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

The commit message follows the repo's existing convention: `feat:` prefix, issue reference with `(#166)`, and Claude co-author trailer.

---

## Files Touched

| File | Action | Notes |
|------|--------|-------|
| `isprime.py` | **CREATE** (at repo root) | Executable Python script. Implements `is_prime()` with trial division up to `√n`. Uses `argparse` with required `--number` flag. |

## Backward Compatibility

No breaking changes. `greeting.py`, `hello.py`, and any other existing files are untouched. The new `isprime.py` is a standalone script with no dependencies on other project files.

## Performance Notes

The trial-division algorithm runs in O(√n) time. For `n ≈ 10⁶` this is at most ~500 iterations; for `n ≈ 10¹²` it's at most ~500,000 iterations — well within reasonable CLI latency. For cryptographic-sized numbers (hundreds of digits), a probabilistic test (Miller–Rabin) would be needed, but that is explicitly out of scope for this issue.
