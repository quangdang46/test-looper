# Spec: Add `hello.py` (Issue #85)

Issue: #85
Spec: `specs/85-spec/spec.md`

---

## Objective

Create an executable `hello.py` script at the repo root that prints `"Hello from Looper!"` by default and accepts an optional `--name` flag to customize the greeting.

Note: A prior implementation of `hello.py` exists on this branch (landed via issue #72 / PR #101). The goal of issue #85 is to **confirm** the file meets all stated requirements — verification is the primary deliverable here; if the existing file fully matches the spec, the spec serves as the validation record.

## Requirements

1. `hello.py` must be executable and placed at the repo root.
2. When run with no arguments, it must print `Hello from Looper!`.
3. When run with `--name <VALUE>`, it must print `Hello from <VALUE>!`.
4. It must use `argparse` for CLI argument parsing.
5. Default value for `--name` must be `"Looper"`.
6. Must include a shebang line (`#!/usr/bin/env python3`).
7. Must include `main()` guarded by `if __name__ == "__main__":`.

## Implementation Steps

### Step 1 — Verify `hello.py` exists and meets requirements

The file may already exist at the repo root. Verify:

| Check | Command | Expected output |
|-------|---------|----------------|
| No-args invocation | `python3 hello.py` | `Hello from Looper!` |
| With `--name` flag | `python3 hello.py --name Alice` | `Hello from Alice!` |
| With quoted name | `python3 hello.py --name "Bob Dole"` | `Hello from Bob Dole!` |
| Help output | `python3 hello.py --help` | Shows usage and `--name` description |
| Error on unknown flag | `python3 hello.py --bogus` | Non-zero exit + error message |

### Step 2 — If missing, create `hello.py`

If `hello.py` does not exist, create it with the following structure:

```python
#!/usr/bin/env python3
"""A simple hello script with argparse support."""

import argparse


def greet(name: str = "Looper") -> str:
    """Return a greeting string for the given name."""
    return f"Hello from {name}!"


def main() -> None:
    """Parse command-line arguments and print a greeting."""
    parser = argparse.ArgumentParser(description="Print a greeting.")
    parser.add_argument(
        "--name",
        type=str,
        default="Looper",
        help="Name to greet (default: Looper)",
    )
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
```

**Key design choices:**

| Choice | Reason |
|--------|--------|
| Own `greet()` function | The `"Hello from {name}!"` format is distinct from `greeting.py`'s `"Hello, {name}!"`. A standalone function avoids coupling the two scripts. |
| `default="Looper"` | Bare invocation must print `"Hello from Looper!"` per the issue. |
| `--name` flag (not positional) | Flags are self-documenting and the standard argparse pattern for optional named arguments. |
| Shebang line | Makes the file directly executable (`./hello.py`). |
| `__name__ == "__main__"` guard | Allows `greet()` to be imported from other modules in the future. |

### Step 3 — If file already exists, verify content matches

Compare the existing file against the structure above. It should:

- [ ] Use `#!/usr/bin/env python3` shebang.
- [ ] Define `greet(name: str = "Looper") -> str` returning `f"Hello from {name}!"`.
- [ ] Define `main()` with `ArgumentParser`, `--name` flag (`default="Looper"`).
- [ ] Call `main()` under `if __name__ == "__main__":`.

If one or more of these checks fail, **edit** the file to match. If all pass, the implementation is already complete.

### Step 4 — (If modified) Commit and push

```bash
cd /private/tmp/test-looper
git add hello.py
git commit -m "feat: add hello.py with argparse --name support (#85)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

Only run this step if `hello.py` was created or modified. If the file already existed and passed all checks, no commit is needed.

---

## Files touched

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **CREATE** (if missing) or **VERIFY** (if existing) | Executable Python script at repo root |
| `greeting.py` | untouched | No changes to existing `greeting.py` |

## Acceptance criteria

1. `python3 hello.py` → `Hello from Looper!`
2. `python3 hello.py --name Alice` → `Hello from Alice!`
3. `python3 hello.py --name "Bob Smith"` → `Hello from Bob Smith!`
4. `python3 hello.py --help` → shows usage text
5. `python3 hello.py --bogus` → exits non-zero with error
6. `greeting.py` is not modified
7. `python3 greeting.py` still prints `Hello, World!`

## Backward compatibility

No breaking changes. `greeting.py` continues to work exactly as before. `hello.py` is an independent script with no import dependency on `greeting.py`.
