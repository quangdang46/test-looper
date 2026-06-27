# Spec: Add a prime number checker script (Issue #166)

**Issue:** [#166](https://github.com/quangdang46/test-looper/issues/166) — Add a prime number checker script

**Created:** 2026-06-27
**Status:** Planned

---

## Problem

Create a Python script `isprime.py` that checks whether a given integer is a prime number. The script must expose an `is_prime(n: int) -> bool` function and provide a CLI interface via `argparse` with a required `--number` flag. It must handle edge cases (negative numbers, 0, 1, very large numbers) and follow the same project conventions as the existing `greeting.py` and `hello.py`.

## Background

The repo currently contains two Python scripts:

| File | Purpose |
|------|---------|
| `greeting.py` | Core `greet()` returning `"Hello, {name}!"` using `sys.argv` |
| `hello.py` | Wraps `greeting.greet()` with an `argparse --name` flag |

Both share a pattern: `#!/usr/bin/env python3` shebang, type-annotated functions, a `main()` guarded by `if __name__ == "__main__":`, and file placement at the repo root.

Issue #166 follows the same conventions for primality checking — a standalone utility with no dependencies on other project files.

### Prior attempts

Several commits have attempted to land `isprime.py` in this repo (most recently `83faa69`, `c8fe2ed`, `7d6d58b`). None were merged onto `main`. This spec takes the lessons from those attempts to produce a definitive implementation that avoids the following issues:

- **`math.isqrt` vs `while i*i`**: The `c8fe2ed` version uses `math.isqrt` (requires an import), while `8f8b8bf` uses `while i*i <= n` (no import needed). The latter is simpler and avoids a module import for a single call — prefer it for a small standalone script.
- **Verification coverage**: Prior specs had overlapping or ambiguous test assertions. This spec defines explicit, non-overlapping test paths.
- **Worktree placement**: The file must be created at the repo root, not inside `.looper/worktrees/`.

## Goals

1. Create an executable `isprime.py` at the repo root.
2. Implement `is_prime(n: int) -> bool` with odds-only trial division up to `√n`.
3. Provide a CLI interface via `argparse` with a **required** `--number` flag.
4. Handle all edge cases: negative numbers, `0`, `1` → `False`.
5. Handle very large numbers (up to Python's arbitrary-precision ints).
6. Use project conventions: shebang `#!/usr/bin/env python3`, type hints, `main()`, `if __name__ == "__main__"`.
7. Keep existing files (`greeting.py`, `hello.py`) untouched.

## Non-goals

- No performance optimization beyond standard `O(√n)` trial division — the issue does not request a sieve, Miller–Rabin, or any advanced algorithm.
- No error handling beyond `argparse` validation (non-integer input, missing flag).
- No packaging / `setup.py` / `pyproject.toml` — consistent with existing scripts.
- No test file or test framework.

---

## Implementation Steps

### Step 1 — Create `isprime.py`

Create a new file `isprime.py` at the repo root (the working directory of this session).

**Structure:**

```python
#!/usr/bin/env python3
"""Check whether a number is prime."""

import argparse


def is_prime(n: int) -> bool:
    """Return True if n is prime, False otherwise.

    Handles edge cases:
    - n <= 1          → False  (by definition, primes are > 1)
    - n == 2          → True   (smallest and only even prime)
    - n % 2 == 0      → False  (any other even number)

    For n > 2, tests odd divisors from 3 up to sqrt(n).
    The loop exits immediately when i*i exceeds n, i.e. when no divisor
    was found below sqrt(n).
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
    """Parse CLI arguments and print primality result."""
    parser = argparse.ArgumentParser(
        description="Check if a number is prime.",
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

**Design decisions:**

| Choice | Rationale |
|--------|-----------|
| `required=True` on `--number` | The issue explicitly calls for a required `--number` flag. Using `argparse`'s built-in `required=True` gives a clear error message when omitted, with no manual validation code. |
| `type=int` | `argparse` converts the string to an `int`, rejecting non-integer input automatically. |
| No `-n` short alias | Avoids collision with `-n` conventions in other tools; long-form-only keeps the interface self-documenting. The issue only specifies `--number`. |
| `n <= 1` as first guard | Negative numbers, 0, and 1 all return `False` by definition — a single check covers all three edge cases from the spec. |
| `while i * i <= n` (not `math.isqrt`) | Avoids an extra module import for a single function call. The multiplication per iteration is cheap, and the loop termination is equivalent to `sqrt(n)` boundary. For large n near Python's `sys.maxsize`, `i * i` overflows to a long but the comparison remains correct — it just takes the loop one extra iteration. This is simpler and self-contained. |
| `i += 2` step (odds only) | After the initial even check, only odd divisors need to be tested — roughly halves the iteration count. |
| No `sys` import | Unlike `greeting.py`, `isprime.py` has no need for `sys.argv` since argparse handles all argument parsing. |
| `print(is_prime(args.number))` prints `True`/`False` | Matches the issue's example output exactly (literal Python `bool` string representation). |
| Inline docstring with bullet list | Documents all early-return branches at a glance so the reader can immediately confirm edge-case coverage. |

#### Rationale: Odds-only trial division

The algorithm is the simplest deterministic primality test:

1. **Immediate rejection**: numbers ≤ 1 (by definition), even numbers > 2.
2. **Trial division**: test divisibility by odd integers from 3 up to √n.
3. **Performance**: `O(√n)` — for n ≈ 10⁶, the loop runs ~500 iterations; for n ≈ 10¹², ~500,000 iterations. Well within interactive CLI latency.

This is the same algorithm used in all prior implementation attempts for this issue, confirming it meets the requirements.

### Step 2 — Verify correctness

Run the following from the repo root:

```bash
# --- Edge cases (definitional: n <= 1 returns False) ---
python3 isprime.py --number -5    # → False   (negative number)
python3 isprime.py --number 0     # → False   (zero)
python3 isprime.py --number 1     # → False   (one is not prime)

# --- Smallest primes ---
python3 isprime.py --number 2     # → True    (smallest and only even prime)
python3 isprime.py --number 3     # → True
python3 isprime.py --number 7     # → True    (example from issue)

# --- Even composites ---
python3 isprime.py --number 4     # → False   (smallest even composite)
python3 isprime.py --number 8     # → False
python3 isprime.py --number 100   # → False

# --- Odd composites ---
python3 isprime.py --number 9     # → False   (first odd composite; enters loop at i=3)
python3 isprime.py --number 15    # → False

# --- Larger primes ---
python3 isprime.py --number 97         # → True   (100th prime-ish)
python3 isprime.py --number 7919       # → True   (1000th prime)
python3 isprime.py --number 104729     # → True   (10000th prime)

# --- Larger composites ---
python3 isprime.py --number 1000       # → False
python3 isprime.py --number 104730     # → False  (just past the 10000th prime)

# --- Very large numbers ---
python3 isprime.py --number 999999999989      # → True   (large prime ~ 10¹²)
python3 isprime.py --number 999999999991      # → False  (composite ~ 10¹²)

# --- CLI error cases ---
python3 isprime.py                         # → error: --number is required (exit code 2)
python3 isprime.py --number abc            # → error: invalid int value  (exit code 2)
python3 isprime.py --help                  # → prints help text         (exit code 0)
```

**Why these test cases are sufficient:**

| Category | Cases | Path exercised in `is_prime()` |
|---|---|---|
| Negative / 0 / 1 | `-5`, `0`, `1` | First branch: `n <= 1` → `False` |
| Prime 2 | `2` | Second branch: `n == 2` → `True` |
| Even > 2 | `4`, `8`, `100` | Third branch: `n % 2 == 0` → `False` |
| Odd composite | `9`, `15`, `104730` | Loop body: `n % i == 0` → `False` |
| Odd prime | `3`, `7`, `97`, `7919`, `104729` | Loop exhausts → `True` |
| Large number | `999999999989`, `999999999991` | Verifies loop correctness and performance with big ints |
| Missing arg | bare call | `argparse` error: `--number` required |
| Invalid arg | `abc` | `argparse` error: `invalid int value` |
| Help | `--help` | `argparse` prints usage |

Every branch in `is_prime()` is exercised by at least one test, and the two CLI error conditions cover the only failure modes argparse can produce for this interface.

### Step 3 — Commit

```bash
cd /private/tmp/test-looper-review/.looper/worktrees/worker-abc7b885-9249-4b44-8e11-1cd4dcb56459
git add isprime.py
git commit -m "feat: add isprime.py with is_prime() and argparse --number flag (#166)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

The commit message follows the repo's existing convention: `feat:` prefix, issue reference `(#166)`, and Claude co-author trailer.

---

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `isprime.py` | **CREATE** | Executable Python script at repo root. Standalone — imports only `argparse`. |
| `greeting.py` | untouched | No changes. |
| `hello.py` | untouched | No changes. |

## Acceptance criteria

1. `python3 isprime.py --number 7` prints `True`.
2. `python3 isprime.py --number 10` prints `False`.
3. `python3 isprime.py --number -1` prints `False` (negative).
4. `python3 isprime.py --number 0` prints `False`.
5. `python3 isprime.py --number 1` prints `False`.
6. `python3 isprime.py --number 2` prints `True` (smallest prime).
7. `python3 isprime.py --number 999999999989` prints `True` (large prime).
8. `python3 isprime.py` exits non-zero with error about missing `--number`.
9. `python3 isprime.py --number abc` exits non-zero with error about invalid int.
10. `python3 isprime.py --help` prints help text and exits 0.
11. `python3 -c "from isprime import is_prime; print(is_prime(7))"` prints `True` (function is importable).
12. `greeting.py` and `hello.py` are unmodified (git status shows only `isprime.py`).

## Risks

| Risk | Mitigation |
|------|-----------|
| **Worktree placement** — the file is created inside `.looper/worktrees/` instead of the actual repo root | The file must be created in the session's working directory (`/tmp/test-looper-review/.looper/worktrees/worker-abc7b885-...`). Since this is a git worktree of `test-looper`, it **is** the repo root for this branch — `git add` from here targets the correct branch. Verify `git status` shows the new file at the top level before committing. |
| **Performance cliff** for astronomically large numbers (e.g., 10^18+) | Odds-only trial division is `O(√n)` — practical up to ~10¹². A 10^15 input could take minutes. The issue does not specify a performance requirement; this is acceptable. Future work could add Miller–Rabin. |
| **Import path breakage** if `isprime.py` is invoked from outside its directory | `from isprime import is_prime` requires running Python from the directory containing `isprime.py` (the repo root). This is the same limitation as `from greeting import greet` in `hello.py`. |
