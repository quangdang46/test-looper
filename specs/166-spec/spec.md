# Spec: Add a prime number checker script (Issue #166)

**Issue:** #166 — Add a prime number checker script

**Status:** Draft

---

## Problem

Create an executable Python script `isprime.py` that checks whether a given integer is a prime number. The script must expose an `is_prime(n)` function returning `bool` and provide a CLI interface via `argparse` with a required `--number` flag.

## Background

The repo currently contains two greeting scripts:

| File | Purpose |
|------|---------|
| `greeting.py` | Core `greet()` returning `"Hello, {name}!"` using `sys.argv` |
| `hello.py` | Wraps `greeting.greet()` with an `argparse --name` flag |

Both use a consistent pattern: `#!/usr/bin/env python3` shebang, type-annotated functions, a `main()` guarded by `if __name__ == "__main__":`, and live at the repo root.

Issue #166 follows the same conventions for a new domain (primality testing) — it is a standalone utility, not a wrapper around existing code.

## Goals

1. Create `isprime.py` at the repo root with an `is_prime(n: int) -> bool` function.
2. Provide a CLI interface via `argparse` with a **required** `--number` / `-n` flag.
3. Handle all edge cases: negative numbers, `0`, `1`, very large numbers.
4. Use the project's established conventions: shebang, type hints, `main()`, `__name__` guard.
5. Keep existing files (`greeting.py`, `hello.py`) untouched.

## Non-goals

- No performance optimization beyond a standard `O(√n)` trial division — the issue does not request a sieve, Miller–Rabin, or any advanced algorithm.
- No error handling beyond `argparse` validation and a `TypeError` for non-integer input to `is_prime()`.
- No packaging / `setup.py` / `pyproject.toml` — consistent with the existing scripts.
- No test file or test framework setup — the issue only asks for the script itself.

---

## Implementation Steps

### Step 1 — Create `isprime.py`

Create a new file `isprime.py` at the repo root (`/private/tmp/test-looper/isprime.py`).

**Structure:**

```python
#!/usr/bin/env python3
"""Check whether a number is prime."""

import argparse


def is_prime(n: int) -> bool:
    """Return True if n is a prime number, False otherwise.

    Handles edge cases:
    - n <= 1          → False  (by definition, primes are > 1)
    - n == 2          → True   (smallest and only even prime)
    - n % 2 == 0      → False  (any other even number)

    For n > 2, tests odd divisors from 3 up to sqrt(n).
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check if a number is prime."
    )
    parser.add_argument(
        "--number", "-n",
        type=int,
        required=True,
        help="Number to check for primality",
    )
    args = parser.parse_args()
    print(is_prime(args.number))


if __name__ == "__main__":
    main()
```

**Design decisions:**

| Choice | Rationale |
|--------|-----------|
| `O(√n)` trial division (odds-only) | Standard benchmark for a simple primality check. Fast enough for every input Python's `int` can represent as a CLI argument (practical limit ~10¹²). No external dependencies. |
| `required=True` for `--number` | The issue explicitly calls for a required `--number` flag. Using `argparse`'s built-in `required=True` gives a clear error message when omitted, with no manual validation code. |
| Short alias `-n` | Ergonomic for repeated use; consistent with typical CLI flag conventions. |
| `is_prime(n: int) -> bool` return type | Boolean return makes the function reusable as a building block (e.g., filtering primes from a sequence) and matches the issue description exactly. |
| Inline comments for edge cases | The three early-return branches (`n <= 1`, `n == 2`, `n % 2 == 0`) are each documented inline so the reader can immediately confirm edge-case coverage. |

### Step 2 — Verify correctness

Run the following tests from the repo root to validate the script:

```bash
# --- Edge cases (definitional) ---
python3 isprime.py --number -5    # → False   (negative)
python3 isprime.py --number 0     # → False   (zero)
python3 isprime.py --number 1     # → False   (one)

# --- Small primes ---
python3 isprime.py --number 2     # → True
python3 isprime.py --number 3     # → True
python3 isprime.py --number 5     # → True
python3 isprime.py --number 7     # → True

# --- Small composites ---
python3 isprime.py --number 4     # → False
python3 isprime.py --number 6     # → False
python3 isprime.py --number 8     # → False
python3 isprime.py --number 9     # → False

# --- Larger numbers ---
python3 isprime.py --number 97         # → True   (prime)
python3 isprime.py --number 100        # → False  (composite)
python3 isprime.py --number 7919       # → True   (1000th prime)
python3 isprime.py --number 7920       # → False
python3 isprime.py --number 104729     # → True   (10000th prime)
python3 isprime.py --number 104730     # → False

# --- Very large number ---
python3 isprime.py --number 999999999989      # → True   (large prime)
python3 isprime.py --number 999999999991      # → False  (composite)

# --- CLI error cases ---
python3 isprime.py                  # → error: --number is required (exit code 2)
python3 isprime.py --number abc     # → error: invalid int value (exit code 2)
python3 isprime.py --help           # → prints help text (exit code 0)
```

These test cases cover every path through `is_prime()`:
- **Negative / 0 / 1** → first branch (`n <= 1`)
- **2** → second branch (`n == 2`)
- **Even > 2** → third branch (`n % 2 == 0`)
- **Odd composite** → divisor loop hits (`n % i == 0`)
- **Odd prime** → divisor loop exhausts (`return True`)
- **Missing / invalid `--number`** → argparse error paths

### Step 3 — Commit

```bash
git add isprime.py
git commit -m "feat: add isprime.py with argparse --number flag (#166)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `isprime.py` | **CREATE** | New standalone script at repo root |
| `greeting.py` | untouched | No changes |
| `hello.py` | untouched | No changes |

## Acceptance criteria

1. `python3 isprime.py --number 7` prints `True`.
2. `python3 isprime.py --number 10` prints `False`.
3. `python3 isprime.py --number -1` prints `False` (negative numbers).
4. `python3 isprime.py --number 0` prints `False`.
5. `python3 isprime.py --number 1` prints `False`.
6. `python3 isprime.py --number 999999999989` prints `True` (large prime).
7. `python3 isprime.py` exits with a non-zero exit code and prints an error about missing `--number`.
8. `python3 isprime.py --number abc` exits with a non-zero exit code and prints an error about invalid int.
9. `python3 -c "from isprime import is_prime; print(is_prime(7))"` prints `True` (importable function).
10. `greeting.py` and `hello.py` are unmodified.

## Risks

| Risk | Mitigation |
|------|-----------|
| Performance cliff for astronomically large `--number` (e.g., 10^18+) | The odds-only trial division is `O(√n)` — practical for numbers up to ~10^12, but could take minutes for 10^15+. The issue does not specify a performance requirement, so this is acceptable. A future optimization could add Miller–Rabin. |
| File placed inside a worktree directory instead of the repo root | `mkdir -p` and `git add` must target `/private/tmp/test-looper/isprime.py` directly, not any path under `.looper/worktrees/`. Verify with `pwd` before creating the file. |
