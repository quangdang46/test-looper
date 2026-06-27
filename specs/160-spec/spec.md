# Spec: Add a temperature converter script (Issue #160)

---
## Objective

Create a new Python CLI script `tempconv.py` that converts temperatures between Celsius and Fahrenheit. The script exposes two conversion functions (`celsius_to_fahrenheit` and `fahrenheit_to_celsius`) and a dual-flag `argparse` CLI so users can convert in either direction or see both conversions at once, following the existing project conventions (shebang, `main()` guard, type hints).

## Implementation Plan

1. **Create `tempconv.py` at the repo root** — write a new executable Python script following the project's established patterns (shebang, docstring, type-annotated functions, `main()` guarded by `if __name__`).

2. **Implement the two core conversion functions**:
   - `celsius_to_fahrenheit(c: float) -> float` — returns `(c * 9/5) + 32`
   - `fahrenheit_to_celsius(f: float) -> float` — returns `(f - 32) * 5/9`
   
   Each function has a single responsibility, is stateless, and is trivially testable in isolation (importable from other scripts).

3. **Build the CLI with `argparse`**:
   - Declare two mutually exclusive optional flags: `--celsius` and `--fahrenheit`, each taking a `float` argument.
   - When `--celsius C` is provided: compute both `f = celsius_to_fahrenheit(C)` and display `C°C = f°F`.
   - When `--fahrenheit F` is provided: compute both `c = fahrenheit_to_celsius(F)` and display `F°F = c°C`.
   - When **both** flags are provided (the issue says "Provide both flags shows both conversions"): interpret one as input, compute the other, and show both lines. The most natural reading is: run both conversions and show their respective outputs. Showing:
     ```
     {celsius}°C = {fahrenheit}°F
     {fahrenheit}°F = {celsius}°C
     ```
   - When neither flag is provided: print a usage hint and exit with a non-zero code.

4. **Handle non-numeric input gracefully**:
   - `argparse` natively rejects non-float input when `type=float`, printing an error and exiting non-zero. This covers the most common case ("abc", "1.2.3").
   - Additionally, wrap the flag value parsing in a `try` block or rely on argparse's built-in error handling. The spec recommends using argparse's `type=float` which already rejects bad input with a clear message.
   - For extra robustness, the `main()` function can catch `argparse.ArgumentError` or simply let argparse handle it (it already prints a helpful message to stderr and calls `sys.exit(2)`).

5. **Verify correctness** — after writing, run the examples from the issue and a handful of edge cases (see Acceptance Criteria).

## Files to Change

| File | Action | Notes |
|---|---|---|
| `tempconv.py` | **Create** (at repo root) | New script with two conversion functions and a dual-flag argparse CLI. Must be placed in the repo root, alongside `greeting.py` and `hello.py`. |
| All other files | **Unchanged** | No existing files are modified. |

## Risks

- **Precision / floating-point drift** — conversions like `celsius_to_fahrenheit(celsius_to_fahrenheit(0))` may not return exactly `0` due to floating-point representation (`0°C → 32°F → 0°C` is exact because 5/9 * 32 is exactly representable, but round-trips through non-integer values may accumulate small errors). Acceptable for a CLI tool; document that results are approximate.
- **Both-flag ambiguity** — the issue says "Provide both flags shows both conversions." The natural behavior given `--celsius 100 --fahrenheit 212` is to show both lines (input is consistent), but `--celsius 100 --fahrenheit 50` is contradictory. Follow the simplest interpretation: treat each flag independently and compute the counterpart for each.
- **argparse `type=float` locale handling** — `type=float` uses Python's `float()`, which always expects a dot as decimal separator regardless of locale; this is correct for the CLI use case.
- **argparse `type=float` error message quality** — argparse's built-in error for a non-float value says `argument --celsius: invalid float value: 'abc'`. This is clear enough; no custom error wrapping needed.
- **Negative temperatures** — `--celsius -10` may be parsed by argparse as a flag `10` with value `-10` if the user does not use `=` syntax. On most shells, `--celsius -10` works (argparse reads `-10` as the value), but `--celsius=-10` is unambiguous. Document this in the help text or accept either syntax (which argparse handles automatically).
- **No coverage of existing code** — no existing file is touched, so no regression risk for the project. Simple unit test in docstring or separate test file is low cost.

## Acceptance Criteria

1. `python3 tempconv.py --celsius 100` prints `100.0°C = 212.0°F` (or equivalent formatting).
2. `python3 tempconv.py --fahrenheit 32` prints `32.0°F = 0.0°C`.
3. `python3 tempconv.py --celsius 0 --fahrenheit 32` prints both conversion lines:
   - `0.0°C = 32.0°F`
   - `32.0°F = 0.0°C`
4. `python3 tempconv.py` (no flags) exits with a non-zero exit code and prints a usage or error message.
5. `python3 tempconv.py --celsius abc` exits with a non-zero exit code and prints an error about invalid float value.
6. `python3 tempconv.py --help` prints a complete help message describing both `--celsius` and `--fahrenheit` flags.
7. `python3 -c "from tempconv import celsius_to_fahrenheit; print(celsius_to_fahrenheit(0))"` prints `32.0` (import works, function is correct).
8. `python3 -c "from tempconv import fahrenheit_to_celsius; print(fahrenheit_to_celsius(212))"` prints `100.0`.
9. The script is executable with a shebang (`./tempconv.py --celsius 100` works after `chmod +x`).
10. No existing file in the repo is modified.

---
Spec: specs/160-spec/spec.md
