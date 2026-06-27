# Spec: Test middleware chain

Issue: #168
Spec: specs/168-spec/spec.md

---

## Objective

Add test coverage that validates the import and function-call chain (`hello.py → greeting.greet()`) end-to-end, while also serving as a live exercise of the Looper daemon's middleware pipeline (quality gate → outcome recorder → patrol). The tests verify that arguments are correctly forwarded across the module boundary, return values propagate, and both scripts produce consistent output — proving the full processing chain works from CLI invocation through library call to printed result.

## Implementation Plan

1. **Create `tests/` package** — add `tests/__init__.py` (empty) to establish the repo's first test directory so `python3 -m pytest` can auto-discover tests.

2. **Create `tests/test_greeting.py`** — unit tests for `greeting.py`:
   - Test `greet()` with no argument (default `"World"`).
   - Test `greet()` with explicit names: simple (`"Alice"`), multi-word (`"Bob Smith"`), special chars (`"Jean-Luc"`).
   - Test `greeting.main()` via `sys.argv` mocking, capturing stdout to verify printed output.

3. **Create `tests/test_hello.py`** — integration / chain tests for `hello.py`:
   - Test that `hello.main()` (which imports and delegates to `greeting.greet()`) produces correct output for the same `--name` value. This validates the import dependency is resolved and the argument is correctly forwarded.
   - Test `hello.main()` with `--name Alice` → stdout is `Hello, Alice!`.
   - Test `hello.main()` with no args → stdout is `Hello, World!` (argparse default matching `greeting.py`'s function default).
   - Test `hello.main()` with `--name ""` → stdout is `Hello, !` (edge case: empty string for name).
   - Test `hello.main()` with `--name "Bob Smith"` (quoted multi-word name).
   - Verify `python3 hello.py` and `python3 -c "from greeting import greet; print(greet())"` still work (no import chain breakage).

4. **Create `pytest.ini`** — minimal pytest configuration:
   - `testpaths = tests`
   - `python_files = test_*.py`
   - This is a convenience; the tests also work without it (pytest defaults will still discover `tests/test_*.py`).

5. **Verify end-to-end** — run all tests and confirm 100% pass rate.

## Files to Change

| File | Action | Notes |
|---|---|---|
| `tests/__init__.py` | **Create** | Empty init file to make `tests/` a Python package discoverable by pytest. |
| `tests/test_greeting.py` | **Create** | Unit tests for `greeting.py`: `greet()` function (boundary cases) and `main()` CLI via mocked `sys.argv`. |
| `tests/test_hello.py` | **Create** | Chain/integration tests for `hello.py`: validates correct import resolution, argument forwarding, and output consistency with `greeting.greet()`. Also tests argparse edge cases (`--help`, unknown flags). |
| `pytest.ini` | **Create** | Minimal pytest config: `testpaths = tests`, `python_files = test_*.py`. |
| *(no changes to `greeting.py` or `hello.py`)* | — | Existing source files must remain unmodified. |

## Risks

- **Import path errors** — `from greeting import greet` in both `hello.py` and the test files assumes the working directory is the repo root. If tests are run from elsewhere, the import will fail. Document this requirement in a test comment. Pytest recommends running from the repo root anyway.
- **sys.argv pollution** — `greeting.main()` and `hello.main()` both read `sys.argv` directly. Tests that call `main()` directly must save and restore `sys.argv` to prevent cross-test interference. Use a pytest fixture with `yield` teardown.
- **Default value mismatch** — `hello.py`'s argparse default for `--name` is `"World"` (matching `greeting.py`'s `greet()` default). If these diverge in the future, the bare-invocation behavior of `hello.py` and `greeting.py` will differ. Tests should explicitly assert the default-chain behavior.
- **Test subject ambiguity** — this is a test-project for the Looper daemon. The same issue (#168) exercises Looper's own middleware pipeline (quality gate → outcome recorder → patrol). Changes to the Looper daemon's pipeline could affect how this issue is processed. The Python tests must remain standalone (run via `pytest`, not via Looper).
- **pytest not installed** — the CI/testing environment may not have `pytest` installed. The acceptance criteria should include explicit installation instructions or a `requirements.txt`/`dev-dependencies` step. For this repo, `python3 -m pytest` works if pytest is available in the environment.
- **Pre-existing test directory** — the repo currently has no `tests/` directory. Creating one assumes no other test layout exists or is planned. This is safe for a small repo with only two Python modules.

## Acceptance Criteria

1. `python3 -m pytest tests/` passes — all tests green, no errors or warnings.
2. `python3 -m pytest tests/test_greeting.py` runs the greeting unit tests and passes:
   - `greeting.greet()` default returns `Hello, World!`.
   - `greeting.greet("Alice")` returns `Hello, Alice!`.
   - `greeting.greet("Bob Smith")` returns `Hello, Bob Smith!`.
   - `greeting.greet("Jean-Luc")` returns `Hello, Jean-Luc!`.
   - `greeting.main()` with mocked `sys.argv` prints the correct greeting.
3. `python3 -m pytest tests/test_hello.py` runs the hello integration tests and passes:
   - `hello.main()` with no args prints `Hello, World!` (argparse default → `greeting.greet()` default).
   - `hello.main()` with `--name Alice` prints `Hello, Alice!`.
   - `hello.main()` with `--name ""` prints `Hello, !`.
   - `hello.main()` with `--name "Bob Smith"` prints `Hello, Bob Smith!`.
4. Test isolation: calling `main()` with mocked `sys.argv` in one test does not affect subsequent tests (verified by running full test suite).
5. `greeting.py` and `hello.py` are not modified.
6. `python3 greeting.py` and `python3 greeting.py Alice` still print `Hello, World!` and `Hello, Alice!` respectively.
7. `python3 hello.py` and `python3 hello.py --name Alice` still print `Hello, World!` and `Hello, Alice!` respectively.
