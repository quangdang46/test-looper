# Spec: Add a simple fibonacci script

Issue: #155
Spec: specs/155-spec/spec.md

---

## Objective

Create a new `fibonacci.py` script in the repo root that computes and prints Fibonacci numbers. The script exposes a `fibonacci(n)` function and a CLI interface via `argparse` with a `--count` flag to control how many numbers to print.

## Implementation Plan

1. **Create `fibonacci.py`** — write a new executable Python script at the repo root.
   - Implement a `fibonacci(n: int) -> int` function that returns the nth Fibonacci number (0-indexed: `fibonacci(0) → 0`, `fibonacci(1) → 1`, `fibonacci(2) → 1`, `fibonacci(3) → 2`, etc.).
   - Use an iterative approach (not recursion) to avoid stack overflow for larger `n`.
   - Handle edge cases:
     - `n == 0` → return `0`
     - `n == 1` → return `1`
     - `n < 0` → raise `ValueError` with a descriptive message
   - Add a `main()` function guarded with `if __name__ == "__main__":`.
   - Use `argparse.ArgumentParser` with a `--count` flag (type `int`, default `10`, help describing that it controls the number of Fibonacci numbers to print).
   - The CLI should print the first `--count` Fibonacci numbers, one per line or space-separated.
   - Use the same `#!/usr/bin/env python3` shebang as the project convention.

2. **Verify correctness** — run the script with various arguments and confirm:
   - Default invocation prints the first 10 Fibonacci numbers.
   - `--count 5` prints the first 5.
   - `--count 0` prints nothing (or just `0` depending on interpretation; edge case).
   - `--count 1` prints `0`.
   - Negative `--count` either prints nothing or errors gracefully.
   - `--help` displays argument documentation.
   - `fibonacci(-1)` raises `ValueError`.

## Files to Change

| File | Action | Notes |
|---|---|---|
| `fibonacci.py` | **Create** (at repo root) | New script. Contains `fibonacci(n)` function and argparse CLI with `--count` flag. Must be placed in the repo root. |

No existing files are modified.

## Risks

- **0-indexing confusion** — the issue says "nth Fibonacci number" but doesn't specify whether the sequence is 1-indexed or 0-indexed. The spec uses 0-indexing (`fibonacci(0) = 0`, `fibonacci(1) = 1`) because it matches the standard mathematical definition. The `--count` option prints from index 0 through `count - 1`.
- **Large values of `--count`** — an iterative approach handles large-ish n, but extremely large values (e.g., `--count 100000`) could take noticeable time. The function uses Python integers (unbounded) so it won't overflow, but performance degrades for huge counts. Not a concern for typical use (default 10).
- **Negative `--count`** — `argparse` doesn't by default forbid negative integers. The script should handle this: either print nothing (empty output), or raise an error. The implementation plan should choose one behavior explicitly.
- **Shebang convention** — keep the `#!/usr/bin/env python3` shebang consistent with the existing `greeting.py` and `hello.py` scripts.
- **Import path safety** — if run from outside the repo root, standalone execution works fine (no cross-file imports), but if `fibonacci()` is imported elsewhere, the import must work from the repo root.

## Acceptance Criteria

1. `python3 fibonacci.py` prints the first 10 Fibonacci numbers: `0 1 1 2 3 5 8 13 21 34` (one per line or space-separated).
2. `python3 fibonacci.py --count 5` prints `0 1 1 2 3`.
3. `python3 fibonacci.py --count 1` prints `0`.
4. `python3 fibonacci.py --count 0` prints nothing (empty output).
5. `python3 fibonacci.py --count -1` either prints nothing or prints an error message (no crash).
6. `python3 fibonacci.py --help` prints a help message describing the `--count` flag.
7. `python3 fibonacci.py --unknown-flag` exits with a non-zero exit code and prints an error.
8. `python3 -c "from fibonacci import fibonacci; print(fibonacci(0))"` prints `0`.
9. `python3 -c "from fibonacci import fibonacci; print(fibonacci(1))"` prints `1`.
10. `python3 -c "from fibonacci import fibonacci; print(fibonacci(10))"` prints `55`.
11. `python3 -c "from fibonacci import fibonacci; fibonacci(-1)"` raises `ValueError`.
12. No existing files (`greeting.py`, `hello.py`, `README.md`) are modified.
