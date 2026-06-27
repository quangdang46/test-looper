# Spec: Add a simple fibonacci script (Issue #155)

## Problem

**Issue #155** asks for a new `fibonacci.py` script that computes and prints Fibonacci numbers. The script should provide:
- A `fibonacci(n)` function that returns the nth Fibonacci number
- A CLI interface via `argparse` with a `--count` flag (default: 10) that controls how many numbers to print
- Edge-case handling for `n=0`, `n=1`, and negative inputs
- A `--help` flag (provided automatically by `argparse`)

The repository already contains `greeting.py` (PR #37) and `hello.py` (PR #93) — both serve as reference for the project's Python script conventions (shebang, `main()` guard, `argparse` pattern, repo-root placement).

## Goals

1. Create an executable `fibonacci.py` at the repo root.
2. Implement a standalone, importable `fibonacci(n: int) -> int` function.
3. Use `argparse` for CLI argument parsing with a `--count` flag.
4. Handle edge cases correctly: `n=0`, `n=1`, and negative inputs.
5. Default `--count` value is `10` (print the first 10 Fibonacci numbers).
6. Keep `greeting.py` and `hello.py` unchanged.

## Non-goals

- No changes to `greeting.py`, `hello.py`, or any existing file.
- No packaging / `setup.py` / `pyproject.toml` — the script runs as `python3 fibonacci.py`.
- No caching or memoization — the scope of the issue does not require performance optimization.
- No file I/O or network access — pure CLI output to stdout.

## Fibonacci definition

The canonical Fibonacci sequence:

```
F(0) = 0
F(1) = 1
F(n) = F(n-1) + F(n-2)   for n >= 2
```

Thus the first 10 numbers (indices 0 through 9) are:
`0, 1, 1, 2, 3, 5, 8, 13, 21, 34`

---

## Implementation Steps

### Step 1 — Create `fibonacci.py`

Create a new file `fibonacci.py` at the repo root.

**Structure:**

```python
#!/usr/bin/env python3
"""A simple Fibonacci number script."""


def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number.

    Args:
        n: The index in the Fibonacci sequence (non-negative integer).

    Returns:
        The nth Fibonacci number.

    Raises:
        ValueError: If n is negative.
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
    import argparse

    parser = argparse.ArgumentParser(
        description="Print the first N Fibonacci numbers."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of Fibonacci numbers to print (default: 10)",
    )
    args = parser.parse_args()

    for i in range(args.count):
        try:
            val = fibonacci(i)
            print(f"F({i}) = {val}")
        except ValueError as e:
            print(f"Error: {e}")
            return


if __name__ == "__main__":
    main()
```

**Rationale for key choices:**

| Choice | Reason |
|--------|--------|
| `fibonacci(n: int) -> int` | Self-contained, importable function with type hints. No external dependencies. |
| Iterative loop (not recursion) | Linear O(n) time, O(1) space. Avoids Python's recursion limit and stack overflow for large n. |
| `raise ValueError` for negative n | Follows Python convention for invalid arguments. The CLI catches it and prints a user-friendly error. |
| `--count` (not positional) | Consistent with `hello.py`'s `--name` flag pattern. Named flags are more self-documenting. |
| `default=10` | Matches the issue specification. |
| Output format `F(i) = <value>` | Clear labeling shows the index alongside each Fibonacci number, making the output self-explanatory. |
| shebang line | Makes the file directly executable (`./fibonacci.py`). |
| `__name__ == "__main__"` guard | Allows `fibonacci()` to be imported from other scripts or test files. |
| `import argparse` inside `main()` | Keeps the import local to the CLI entry point, so `from fibonacci import fibonacci` doesn't pull in argparse at module level. |

### Step 2 — Verify correctness

After writing the file, validate:

```bash
cd /private/tmp/test-looper

# Default behavior (first 10 numbers)
python3 fibonacci.py
# Expected output:
# F(0) = 0
# F(1) = 1
# F(2) = 1
# F(3) = 2
# F(4) = 3
# F(5) = 5
# F(6) = 8
# F(7) = 13
# F(8) = 21
# F(9) = 34

# Custom count
python3 fibonacci.py --count 5
# Expected output:
# F(0) = 0
# F(1) = 1
# F(2) = 1
# F(3) = 2
# F(4) = 3

# Edge case: count=0 (prints nothing)
python3 fibonacci.py --count 0
# Expected output: (empty, no output)

# Custom count (alias)
python3 fibonacci.py --count 1
# Expected: F(0) = 0

# --help flag
python3 fibonacci.py --help
# Expected: prints help message with --count flag described

# Invalid: negative count
python3 fibonacci.py --count -1
# Expected: error message about negative n

# Unimportable flag
python3 fibonacci.py --unknown-flag
# Expected: exits with non-zero, prints argparse error
```

**Edge case matrix tested:**

| Input | Expected behavior |
|-------|------------------|
| `--count 0` | Empty output (no numbers printed) |
| `--count 1` | Prints only `F(0) = 0` (the loop runs for `i=0` only) |
| `--count 2` | Prints `F(0) = 0` and `F(1) = 1` (covers the two base cases) |
| `--count 10` (default) | Prints the full sequence as defined above |
| `--count -1` | Error: invalid input (negative n) |
| `--unknown-flag` | Argparse error + non-zero exit |

### Step 3 — Optional: verify importability

```bash
python3 -c "from fibonacci import fibonacci; print(fibonacci(10))"  # → 55
python3 -c "from fibonacci import fibonacci; print(fibonacci(0))"   # → 0
python3 -c "from fibonacci import fibonacci; print(fibonacci(1))"   # → 1
```

These verify that `fibonacci()` is importable from other modules without triggering CLI execution.

### Step 4 — Commit and push

Working from the main repo at `/private/tmp/test-looper`:

```bash
git add fibonacci.py
git commit -m "feat: add fibonacci.py with --count flag (#155)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

The commit message follows the repo's existing convention (see `6afb126`, `48ed356`, `217e6e7`): start with `feat:`, reference the issue with `(#155)`, single-line subject followed by a blank line and optional body, and include the Claude co-author trailer.

---

## Files touched

| File | Action |
|------|--------|
| `fibonacci.py` | **CREATE** — executable Python script using shebang, with importable `fibonacci()` function |
| `greeting.py` | untouched |
| `hello.py` | untouched |

## Backward compatibility

No breaking changes. Both `greeting.py` and `hello.py` work exactly as before. `fibonacci.py` is a new addition that does not modify any existing behavior.

## Acceptance criteria

1. `python3 fibonacci.py` prints the first 10 Fibonacci numbers (indices 0–9).
2. `python3 fibonacci.py --count 5` prints the first 5 Fibonacci numbers.
3. `python3 fibonacci.py --count 0` produces no output (empty).
4. `python3 fibonacci.py --count 1` prints only `F(0) = 0`.
5. `python3 fibonacci.py --count -1` prints an error message about negative input.
6. `python3 fibonacci.py --help` prints a help message describing the `--count` flag.
7. `python3 fibonacci.py --unknown-flag` exits with a non-zero exit code.
8. `from fibonacci import fibonacci; fibonacci(10)` returns `55`.
9. `from fibonacci import fibonacci; fibonacci(0)` returns `0`.
10. `from fibonacci import fibonacci; fibonacci(1)` returns `1`.
11. `from fibonacci import fibonacci; fibonacci(-1)` raises `ValueError`.
12. `greeting.py` and `hello.py` are not modified.
