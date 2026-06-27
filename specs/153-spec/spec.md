# Spec: Add a simple calculator script (Issue #153)

Issue: #153
Spec: specs/153-spec/spec.md

---

## Objective

Add a `calculator.py` script that performs basic arithmetic operations (`add`, `sub`, `mul`, `div`) on two operands via the CLI, following the same script conventions as the existing `greeting.py` and `hello.py` (shebang, reusable function, `main()` guard, argparse).

## Implementation Plan

1. **Create `calculator.py`** — write a new executable Python script at the repo root.
   - Define a `calculate(a: float, b: float, op: str) -> float` function that dispatches on the operator argument and performs the corresponding arithmetic.
   - Use `argparse.ArgumentParser` to declare `--a`, `--op`, and `--b` flags.
     - `--a` and `--b` are the two numeric operands (`type=float`, `required=True`).
     - `--op` is a required-choice argument (`choices=["add", "sub", "mul", "div"]`).
   - Print the result of `calculate(a, b, op)` rounded to a reasonable precision.
   - Include a `main()` function guarded with `if __name__ == "__main__":`.
   - Use the `#!/usr/bin/env python3` shebang, matching project convention.

2. **Verify correctness** — run the script against all four operators and confirm the output matches expected arithmetic, including edge cases like division by zero, negative numbers, and floating-point results.

## Files to Change

| File | Action | Notes |
|---|---|---|
| `calculator.py` | **Create** (at repo root) | New script. `calculate()` function for reuse; `argparse` CLI for `--a`, `--op`, `--b` flags. |

## Risks

- **Division by zero** — `op=div` with `--b 0` must produce a clear error rather than crashing with a Python traceback. The `calculate()` function should raise a `ValueError` (or return a sentinel), and `main()` should catch it and print a user-friendly message and exit with a non-zero code.
- **Floating-point precision** — operations like `10 / 3` produce repeating decimals. The output should round to a reasonable number of decimal places (e.g., 2 decimal places or use Python's default `str()` on the float). If rounding is applied, the result must be clearly labeled so it's not mistaken for exact arithmetic.
- **Operator naming** — `--op` choices must be unambiguous and intuitive: `add` (a + b), `sub` (a - b), `mul` (a * b), `div` (a / b). Avoid single-letter abbreviations that could be confused.
- **Large numbers** — float overflow is a Python float concern, not something the script needs to guard against. Document that operands are treated as `float`.
- **Existing scripts unchanged** — no modifications to `greeting.py` or `hello.py`.

## Acceptance Criteria

1. `python3 calculator.py --a 2 --op add --b 3` prints `5.0` (or equivalent).
2. `python3 calculator.py --a 10 --op sub --b 4` prints `6.0`.
3. `python3 calculator.py --a 3 --op mul --b 7` prints `21.0`.
4. `python3 calculator.py --a 10 --op div --b 2` prints `5.0`.
5. `python3 calculator.py --a 10 --op div --b 3` prints a value close to `3.333...` (or a rounded variant).
6. `python3 calculator.py --a 5 --op div --b 0` exits with a non-zero exit code and prints a clear division‑by‑zero error message (no raw Python traceback).
7. `python3 calculator.py --help` prints a help message describing all three flags (`--a`, `--op`, `--b`).
8. `python3 calculator.py --a abc --op add --b 1` exits with a non-zero exit code (argparse type error for `--a`).
9. `python3 calculator.py --a 1 --op modulo --b 1` exits with a non-zero exit code (invalid `--op` choice).
10. `python3 -c "from calculator import calculate; print(calculate(2, 3, 'add'))"` returns `5.0` (the function is importable).
11. Neither `greeting.py` nor `hello.py` is modified.
12. All existing scripts continue to run without error.
