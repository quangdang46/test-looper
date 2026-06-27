# Issue #72: Add a simple hello.py script

**Status:** Planned  
**Author:** quangdang46  
**Labels:** dispatch/implement, looper/planned, looper:implement, looper:plan

---

## Overview

Create a `hello.py` script at the repository root that prints "Hello from Looper!" by default and supports an optional `--name` flag via `argparse` for customizing the greeting.

This is the second Python script in the repo, complementing the existing `greeting.py` (which uses `sys.argv` and prints "Hello, {name}!"). The new script uses `argparse` idiomatic Python and introduces a different default message.

## Requirements

1. **File:** `hello.py` at the repository root.
2. **Shebang:** `#!/usr/bin/env python3`
3. **Default behavior:** Running `python3 hello.py` prints `Hello from Looper!` (with a trailing newline).
4. **`--name` flag:** `python3 hello.py --name Alice` prints `Hello from AliceLooper!`. Wait, that looks wrong. Let me re-read.

Actually, re-reading the issue — the user wants `python3 hello.py --name Alice` to print `Hello from Looper!` with a personalized message that includes the given name.

The exact output for `--name Alice` should be: `Hello Alice from Looper!`

Wait, let me re-read the issue more carefully. "prints 'Hello from Looper!' with argparse --name flag support". This means:
- Default: prints "Hello from Looper!"
- With --name: prints something like "Hello {name} from Looper!" or "Hello from {name}!" or similar.

Let me keep it simple and consistent with `greeting.py`:

- Default: `Hello from Looper!`
- `--name Alice`: `Hello Alice from Looper!`

5. **Use `argparse`** (not `sys.argv`) for argument parsing.
6. **Exit code:** 0 on success.
7. **Style:** Follow the same conventions as `greeting.py` — module docstring, a `greet()` function (returning the string), a `main()` function (accepting CLI args), and `if __name__ == "__main__"` guard.

## Design

### Module structure

```python
#!/usr/bin/env python3
"""A simple hello script for the Looper project."""

import argparse


def greet(name: str = "Looper") -> str:
    """Return a greeting string for the given name."""
    return f"Hello from {name}!"


def main() -> None:
    """Parse command-line arguments and print a greeting."""
    parser = argparse.ArgumentParser(description="Print a greeting from Looper.")
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

### Behavior matrix

| Invocation | Output |
|---|---|
| `python3 hello.py` | `Hello from Looper!` |
| `python3 hello.py --name Alice` | `Hello from Alice!` |
| `python3 hello.py -h` | Usage help with `--name` option |
| `python3 hello.py --name` | Error: argument requires a value |

## Implementation steps

### Step 1 — Create `hello.py`

Write the script as described in **Design** above. Place it at the repository root alongside the existing `greeting.py`, `README.md`, and `.gitignore`.

### Step 2 — Make executable

`chmod +x hello.py` so the shebang is effective.

### Step 3 — Verify manually

Run all four scenarios from the **Behavior matrix** and confirm correct output.

### Step 4 — (Optional) Add to README

If desired, add a short entry to `README.md` documenting the new script (its purpose and usage example). This is optional for closing the issue.

## Files Affected

- **Created:** `hello.py` (new file, repository root)
- **Possibly modified:** `README.md` (optional documentation update)

## Acceptance criteria

- [ ] `hello.py` exists at the repo root with shebang.
- [ ] `python3 hello.py` prints `Hello from Looper!`
- [ ] `python3 hello.py --name Alice` prints `Hello from Alice!`
- [ ] The script uses `argparse`, not `sys.argv`.
- [ ] Exit code is 0 on success.
- [ ] Script is executable (`chmod +x`).

## Related

- Existing `greeting.py` — similar but uses `sys.argv` and defaults to "World" instead of "Looper".
- This is a straightforward, self-contained addition with no dependencies on other modules.
