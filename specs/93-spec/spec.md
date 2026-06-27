# Spec: Refactor `hello.py` to Reuse `greeting.py`'s `greet()` (Issue #93)

Issue: #93
Spec: `specs/93-spec/spec.md`

---

## Objective

Refactor the existing `hello.py` to import and reuse the `greet()` function from `greeting.py` instead of defining its own. This eliminates code duplication, aligns with the project's single-responsibility pattern, and makes `hello.py`'s output format consistent with `greeting.py`.

## Current State

The repository already has two Python scripts at the root:

| File | Role | `greet()` definition | Template | Default name |
|---|---|---|---|---|
| `greeting.py` | **Library** — defines `greet()` and provides a minimal CLI via `sys.argv` | ✅ Yes | `"Hello, {name}!"` | `"World"` |
| `hello.py` | **CLI** — currently defines its own `greet()` and provides a rich CLI via `argparse` | ✅ Yes (redundant) | `"Hello from {name}!"` | `"Looper"` |

Both files define their own `greet()` — a code duplication. Issue #93 asks `hello.py` to defer to `greeting.py` for the greeting logic.

## Implementation Plan

### Step 1 — Modify `hello.py`

Change the existing `hello.py` to:

1. **Replace its own `greet()` definition** with an import from `greeting.py`: `from greeting import greet`
2. **Update the `--name` default** from `"Looper"` to `"World"` to match `greeting.py`'s `greet()` default parameter
3. **Update the `--help` text** to reflect the new default
4. **Keep the `main()` function and argparse boilerplate** unchanged — those are `hello.py`'s unique value (argparse-based CLI) and should stay

**Resulting `hello.py`:**

```python
#!/usr/bin/env python3
"""A simple hello script with argparse support."""

import argparse
from greeting import greet


def main() -> None:
    """Parse command-line arguments and print a greeting."""
    parser = argparse.ArgumentParser(description="Print a greeting.")
    parser.add_argument(
        "--name",
        type=str,
        default="World",
        help="Name to greet (default: World)",
    )
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
```

**Rationale for key choices:**

| Choice | Reason |
|---|---|
| `from greeting import greet` | Eliminates code duplication. `greeting.py` is the canonical home for the `greet()` function. Future template changes only need to happen in one place. |
| `default="World"` | Must match `greeting.py`'s `greet(name: str = "World")` default so bare `python3 hello.py` and bare `python3 greeting.py` produce the same output. |
| Keep `main()` + argparse unchanged | `hello.py`'s value is the richer CLI (named `--name` flag, auto-generated `--help`). That code should not move into `greeting.py` to avoid coupling the library to argparse. |
| No shebang change | `hello.py` already has `#!/usr/bin/env python3`. Keep it. |
| No changes to `greeting.py` | `greeting.py` is the upstream library. Issue #93 only concerns `hello.py`. |

### Step 2 — Verify correctness

Run from the repo root:

```bash
cd /private/tmp/test-looper

# Default name (matches greeting.py's default)
python3 hello.py
# Expected: Hello, World!

# Custom name via --name flag
python3 hello.py --name Alice
# Expected: Hello, Alice!

# Multi-word quoted name
python3 hello.py --name "Bob Smith"
# Expected: Hello, Bob Smith!

# Help output
python3 hello.py --help
# Expected: shows "usage:" line and describes --name flag

# Error on unknown flag
python3 hello.py --unknown-flag
# Expected: exits non-zero, prints error like "unrecognized arguments: --unknown-flag"
echo $?
# Expected: 2 (argparse's standard exit code for unknown args)

# greeting.py still works unchanged
python3 greeting.py
# Expected: Hello, World!
python3 greeting.py Alice
# Expected: Hello, Alice!

# Standalone import of greet from greeting still works
python3 -c "from greeting import greet; print(greet())"
# Expected: Hello, World!
```

### Step 3 — Validate import safety

Confirm the import chain is clean and `hello.py` does not introduce circular dependencies or side effects:

```bash
# Import hello's main module without executing it (no __name__ guard issues)
python3 -c "import hello; print(hello.main.__doc__)"
# Expected: prints the docstring of main() — proves the import succeeded

# greeting.py's module-level scope is clean
python3 -c "from greeting import greet; print(greet('Test'))"
# Expected: Hello, Test!
```

## Files to Change

| File | Action | Notes |
|---|---|---|
| `hello.py` | **Modify** | Remove own `greet()`, add `from greeting import greet`, change default to `"World"`. |
| `greeting.py` | **Untouched** | No changes needed — it already exports `greet()` correctly. |
| `specs/93-spec/spec.md` | **Create** (this file) | Implementation plan for issue #93. |

## Backward Compatibility

| Scenario | Before #93 | After #93 | Breaking? |
|---|---|---|---|
| `python3 hello.py` | `Hello from Looper!` | `Hello, World!` | **Yes** — intentional; bare output changes. |
| `python3 hello.py --name Alice` | `Hello from Alice!` | `Hello, Alice!` | **Yes** — intentional; output format aligned with `greeting.py`. |
| `python3 hello.py --help` | Shows default `Looper` | Shows default `World` | Minor — help text changed. |
| `python3 greeting.py` | `Hello, World!` | `Hello, World!` | No. |
| `python3 -c "from greeting import greet"` | Works | Works | No. |
| `python3 -c "from hello import greet"` | Works (own greet) | **Fails** (`ImportError`) | **Yes** — `hello.py` no longer defines `greet()`. If any importers depend on `from hello import greet`, they must switch to `from greeting import greet`. |

**Mitigation for breaking changes:** Since this is an early-stage project with no published API contract and no other importers visible in the repo, the breakage is acceptable. The commit message should clearly state the change so any downstream consumers can adapt.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Import error if CWD is not repo root** | Medium | High | Ensure `hello.py` is run from the repo root. Document this requirement. |
| **Import path works in worktree but not on main** | Low | High | The `from greeting import greet` relative import works because both files are at the same directory level in the repo root. Test in the worktree before merging. |
| **Someone expects old `"Hello from {name}!"` format** | Medium | Low | This is a planned, intentional change driven by the issue specification. The commit message and PR description should explain the rationale. |
| **Circular import risk** | Very Low | High | `hello.py` imports from `greeting.py`; `greeting.py` does not import from `hello.py`. No circular dependency. |
| **Argparse default drifts from greet() default** | Low | Medium | If `greeting.py`'s `greet()` default changes to something other than `"World"`, `hello.py`'s argparse default must be updated in tandem. Add a comment in `hello.py` referencing the coupling. |

## Acceptance Criteria

1. `python3 hello.py` prints `Hello, World!` (reuses `greet()` from `greeting.py` with default name).
2. `python3 hello.py --name Alice` prints `Hello, Alice!`.
3. `python3 hello.py --name "Bob Smith"` prints `Hello, Bob Smith!` (spaces handled).
4. `python3 hello.py --help` prints a help message describing the `--name` flag with default `"World"`.
5. `python3 hello.py --unknown-flag` exits with non-zero exit code and prints an error.
6. `python3 greeting.py` still prints `Hello, World!` (unchanged).
7. `python3 -c "from greeting import greet; print(greet())"` still works (no import chain broken).
8. `hello.py` no longer defines its own `greet()` — the function comes from `greeting.py`.

## Future Considerations

- If `greeting.py` grows additional utility functions, `hello.py` can import them selectively the same way.
- If the project later adds a `pyproject.toml` or package structure, these imports would switch from sibling-path to package-relative imports, but the logical reuse pattern stays the same.
- Consider adding a comment in `hello.py` like `# greet() sourced from greeting.py — keep default in sync` to prevent silent drift.
