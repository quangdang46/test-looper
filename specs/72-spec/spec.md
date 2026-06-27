# Spec: Add a simple hello.py script

**Issue:** [#72](https://github.com/quangdang46/test-looper/issues/72)
**Status:** Draft

---

## 1. Summary

Create `hello.py` at the repo root with argparse `--name` flag support, producing output `"Hello from {name}!"`. The greeting flows from the greeting → hello transition and mirrors the existing `greeting.py` in style and placement.

## 2. Requirements

1. A new file `hello.py` at the repository root.
2. Must contain a `greet(name: str) -> str` function returning `f"Hello from {name}!"`.
3. Must use `argparse` to accept a `--name` flag:
   - `--name` is a string argument with default `"Looper"`.
   - CLI prints the result of `greet()`.
4. Executable entry point under `if __name__ == "__main__": main()`.
5. Shebang `#!/usr/bin/env python3` at the top.
6. Previous attempt (commit `48ed356`) placed the file **inside a worktree path** (`.looper/worktrees/worker-…/hello.py`) rather than at the repo root. This spec must place `hello.py` at the **repo root** (`/tmp/test-looper/hello.py`), consistent with `greeting.py`.

## 3. Design

### 3.1 File structure

```
test-looper/
├── README.md
├── greeting.py        # existing
└── hello.py           # new — this spec
```

### 3.2 `hello.py` body

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

### 3.3 Invocation examples

```
$ python3 hello.py
Hello from Looper!

$ python3 hello.py --name Alice
Hello from Alice!
```

## 4. Implementation steps

| Step | Action |
|------|--------|
| 1 | Create `hello.py` at repo root with the code above. |
| 2 | Run `python3 hello.py` — verify default output `"Hello from Looper!"`. |
| 3 | Run `python3 hello.py --name Alice` — verify `"Hello from Alice!"`. |
| 4 | Run `python3 hello.py --name` without a value — verify argparse error message. |
| 5 | Commit with message `feat: add hello.py with argparse --name support (#72)`. |

## 5. Acceptance criteria

- [ ] `hello.py` exists at the repo root (not inside any `.looper/worktrees/` directory).
- [ ] Running with no flags prints `"Hello from Looper!"`.
- [ ] Running with `--name Alice` prints `"Hello from Alice!"`.
- [ ] Code uses argparse, not manual `sys.argv` parsing.
- [ ] Code style matches `greeting.py` (type hints, `main()` guard, shebang).
