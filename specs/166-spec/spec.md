# Spec: Add a prime number checker script

Issue: #166
Spec: specs/166-spec/spec.md

---

## Objective

Add a new `prime.py` script that checks whether a given integer is prime (prints `True` or `False`) and, when run without arguments or with `--verbose`, prints a human-readable message. This follows the project convention established by `greeting.py` and `hello.py`: a reusable core function behind a simple `argparse` CLI.

## Implementation Plan

1. **Create `prime.py`** at the repo root (alongside `greeting.py` and `hello.py`).
   - Implement a pure function `is_prime(n: int) -> bool` that returns `True` if `n` is a prime number, `False` otherwise.
     - Handle edge cases: numbers less than 2 are not prime.
     - Optimize: check divisibility only up to `sqrt(n)`, skip even numbers after checking 2.
   - Use `argparse.ArgumentParser` with:
     - A positional integer argument `n` (required).
     - A `--verbose` / `-v` flag that, when set, prints a full sentence (e.g., `"7 is a prime number."` or `"4 is not a prime number."`) instead of just `True` / `False`.
   - Include a `main()` function guarded by `if __name__ == "__main__":`.
   - Use `#!/usr/bin/env python3` shebang and `"""docstring"""` for the module, function, and `main()`.

2. **Verify correctness** — run the script against known primes and composites and confirm output.

## Files to Change

| File | Action | Notes |
|---|---|---|
| `prime.py` | **Create** (at repo root) | New script. Implements `is_prime(n)` and an `argparse`-based CLI. Must be placed at the repo root alongside `greeting.py` and `hello.py`. |

No existing files are modified.

## Risks

- **Negative and zero input** — `is_prime()` must correctly return `False` for `n < 2`, including negative numbers and zero.
- **Large prime input** — checking primality via trial division up to `sqrt(n)` is `O(sqrt(n))`. For very large inputs (e.g., a 10-digit prime) this is fast, but for 15+ digit inputs it may become slow. This is acceptable for a teaching / utility script but should be documented in a comment.
- **Non-integer input** — `argparse` with `type=int` will reject floats and strings with a clear error; no special handling needed.
- **Overflow / very large integers** — Python's `int` is unbounded. Trial division of a 100-digit number could take an unbounded amount of time. This is a known limitation of the simple algorithm; document it rather than handling it.
- **Import path** — `prime.py` depends only on the standard library, so there are no import-path concerns (unlike `hello.py` which imports from `greeting.py`).
- **Conflict with existing files** — verify no file named `prime.py` already exists at the repo root.

## Acceptance Criteria

1. `python3 prime.py 7` prints `True`.
2. `python3 prime.py 1` prints `False`.
3. `python3 prime.py 0` prints `False`.
4. `python3 prime.py -13` prints `False` (negative numbers are not prime).
5. `python3 prime.py --verbose 7` prints `7 is a prime number.`
6. `python3 prime.py --verbose 4` prints `4 is not a prime number.`
7. `python3 prime.py --help` prints a help message describing the positional `n` argument and the `--verbose` flag.
8. `python3 prime.py abc` exits with a non-zero exit code and prints a type error (argparse rejects non-integer input).
9. `python3 -c "from prime import is_prime; print(is_prime(2))"` prints `True` (the function is importable).
10. `python3 -c "from prime import is_prime; print(is_prime(97))"` prints `True`.
11. `python3 -c "from prime import is_prime; print(is_prime(100))"` prints `False`.
12. No existing files (`greeting.py`, `hello.py`, etc.) are modified by this change.
Presented by: Brandon Arbel
