# Spec: hello.py prints "Hello from Looper!" (Issue #85)

Issue: #85
Spec: specs/85-spec/spec.md

---

## Objective

Modify `hello.py` so that running `python3 hello.py` prints `"Hello from Looper!"` and accepts an optional `--name` flag to customize the greeting. The output format is `"Hello from {name}!"` with a default name of `"Looper"`.

## Background

The repository already has:

- **`greeting.py`** — a standalone script with its own `greet()` returning `"Hello, {name}!"` (default `"World"`). It is independently usable via `python3 greeting.py`.
- **Current `hello.py`** — created by issue #93, it imports `greet()` from `greeting.py`, so it inherits the `"Hello, {name}!"` format and the `"World"` default. Currently `python3 hello.py` prints `"Hello, World!"`.

Issue #85 requests a different output format (`"Hello from Looper!"`) and a different default name (`"Looper"`). Since `greeting.py` is an independent script that should remain unchanged, `hello.py` must define its own `greet()` with the required format.

## Implementation Steps

### Step 1 — Update `hello.py`

Replace the current `hello.py` content with a self-contained version that defines its own `greet()` function.

**Structure:**

```python
#!/usr/bin/env python3
"""A simple hello script that prints 'Hello from {name}!'."""

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

**Rationale for key choices:**

| Choice | Reason |
|--------|--------|
| Own `greet()` (not importing from `greeting.py`) | The issue specifies `"Hello from {name}!"` format with default `"Looper"`, which differs from `greeting.py`'s `"Hello, {name}!"` with default `"World"`. A standalone function avoids coupling the two scripts and keeps `greeting.py` untouched. |
| `default="Looper"` | Matches the issue's requirement: bare invocation prints `"Hello from Looper!"`. |
| `--name` (optional flag, not positional) | Consistent with existing project patterns. |
| `__name__ == "__main__"` guard | Allows `greet()` to be imported in the future if needed. |

### Step 2 — Verify correctness

Run the following tests from the repo root:

```bash
cd /private/tmp/test-looper
python3 hello.py                         # → "Hello from Looper!"
python3 hello.py --name Alice            # → "Hello from Alice!"
python3 hello.py --name "Bob Smith"      # → "Hello from Bob Smith!"
python3 hello.py --help                  # shows help text
python3 hello.py --unknown-flag          # exits with error
```

### Step 3 — Commit

```bash
git add hello.py
git commit -m "feat: hello.py with 'Hello from {name}!' format and --name flag (#85)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Files Changed

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **MODIFY** | Replace imported `greet()` with own version using `"Hello from {name}!"` format; change default name from `"World"` to `"Looper"`; remove `from greeting import greet` import |
| `greeting.py` | untouched | Unchanged — continues to use `"Hello, {name}!"` format independently |

## Risks

- **Import path removal** — `hello.py` no longer imports from `greeting.py`. This is safe because `hello.py` is the only consumer of that import.
- **greeting.py regression** — `greeting.py` is not modified. Verify with `python3 greeting.py` → `"Hello, World!"` and `python3 greeting.py Alice` → `"Hello, Alice!"`.
- **Shell shebang** — The file retains `#!/usr/bin/env python3` for direct execution.

## Acceptance Criteria

1. `python3 hello.py` prints `Hello from Looper!`
2. `python3 hello.py --name Alice` prints `Hello from Alice!`
3. `python3 hello.py --name "Bob Smith"` prints `Hello from Bob Smith!` (quoted names with spaces work)
4. `python3 hello.py --help` prints a help message describing the `--name` flag
5. `python3 hello.py --unknown-flag` exits with non-zero exit code and prints an error
6. `python3 greeting.py` still prints `Hello, World!` (no regressions)
