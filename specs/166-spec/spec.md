# Spec: Prime number checker script (`isprime.py`)

Issue: #166
Spec: specs/166-spec/spec.md

---

## Objective

Create a standalone Python script `isprime.py` that checks whether a given integer is a prime number, exposed via a command-line interface using `argparse`.

## Background

The repo currently has utility scripts (`greeting.py`, `hello.py`) that serve as building blocks. Issue #166 extends the collection with a mathematical utility: a prime number checker. This script should be self-contained (no external imports beyond the standard library) and handle the full range of integer inputs, including edge cases like negative numbers, zero, one, and very large numbers.

## Implementation Plan

1. **Create `isprime.py`** — write a new executable Python script at the repo root.
   - Shebang line: `#!/usr/bin/env python3` (project convention).
   - Implement `is_prime(n: int) -> bool` that returns `True` if `n` is prime, `False` otherwise.
   - Handle edge cases:
     - `n <= 1` → `False` (neither prime nor composite).
     - `n == 2` → `True` (smallest prime).
     - Even numbers > 2 → early return `False`.
   - Use an efficient trial-division loop up to `sqrt(n)` (step 2 after checking 2). This handles very large numbers reasonably well.
   - CLI via `argparse` with a required `--number` flag accepting an integer.
   - Implement a `main()` function guarded with `if __name__ == "__main__":`.
   - Output: print `True` or `False` on stdout; exit code 0 on success, non-zero on error (e.g., non-integer input).

2. **Verify correctness** — run the script against known primes and composites, including edge cases.

   ```bash
   python3 isprime.py --number 7    # → True
   python3 isprime.py --number 10   # → False
   python3 isprime.py --number 1    # → False
   python3 isprime.py --number 2    # → True
   python3 isprime.py --number -5   # → False
   python3 isprime.py --number 9999991  # → True
   ```

## Files to Change

| File | Action | Notes |
|---|---|---|
| `isprime.py` | **Create** (at repo root) | New standalone script. Self-contained, stdlib only. Uses `argparse` for CLI. Must be placed at repo root alongside `greeting.py` and `hello.py`. |

## Risks

- **Performance on very large inputs** — trial division up to `sqrt(n)` is `O(√n)`. For cryptographically sized numbers (100+ digits), this is impractical. The spec only requires handling "very large numbers" within reason — inputs up to ~10^12 finish in milliseconds; ~10^18 may take seconds. If the project later requires handling huge primes, a probabilistic test (Miller–Rabin) could replace trial division. For now, the simple algorithm is correct and sufficient.
- **Negative number handling** — the spec explicitly says `n <= 1` returns `False`. The implementation must not crash on negative inputs (e.g., `abs()` in a trial-division upper bound without checking sign first).
- **Non-integer input** — `argparse` with `type=int` rejects non-integer values with a clear error message. No special handling needed.
- **No new dependencies** — the script must only use Python stdlib modules. Avoid `math.isqrt` in Python < 3.8 (the project likely uses 3.9+ so `math.isqrt` is safe, but `int(n**0.5)` is more portable).

## Acceptance Criteria

1. `python3 isprime.py --number 7` prints `True`.
2. `python3 isprime.py --number 10` prints `False`.
3. `python3 isprime.py --number 1` prints `False` (edge case — 1 is not prime).
4. `python3 isprime.py --number 2` prints `True` (edge case — 2 is the smallest prime).
5. `python3 isprime.py --number -5` prints `False` (edge case — negative numbers).
6. `python3 isprime.py --number 0` prints `False` (edge case — zero).
7. `python3 isprime.py --number 9999991` prints `True` (large known prime).
8. `python3 isprime.py --number 9999999` prints `False` (large composite).
9. `python3 isprime.py --help` prints a help message describing the `--number` flag.
10. `python3 isprime.py --unknown-flag` exits with a non-zero exit code and prints an error.
11. No existing files are modified.
12. The script can be imported (`python3 -c "from isprime import is_prime; print(is_prime(5))"`) without side effects.
