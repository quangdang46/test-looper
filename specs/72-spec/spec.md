# Issue #72: Add a simple hello.py script

## Summary

Create a `hello.py` script that prints "Hello from Looper!" with an optional `--name` flag for customization, using Python's `argparse` library.

## References

- Issue: [#72](https://github.com/quangdang46/test-looper/issues/72)
- Existing sibling: `greeting.py` (uses `sys.argv` directly; `hello.py` should use `argparse`)

## Requirements

1. Create file `hello.py` at the project root.
2. When run with no arguments, print **`Hello from Looper!`** to stdout.
3. When run with `--name <VALUE>` (or `-n <VALUE>`), print **`Hello from <VALUE>!`** to stdout.
4. Use Python's `argparse` module for argument parsing.
5. Have a module-level function `build_parser() -> argparse.ArgumentParser` — returns the argument parser (testable without executing main).
6. Have a module-level function `main(argv: list[str] | None = None) -> None` — accepts an optional argument list for test injection; defaults to `None` (which `argparse` resolves to `sys.argv[1:]`).
7. The script must be executable via `python hello.py` and also via `chmod +x hello.py && ./hello.py` (include a shebang).
8. Exit with code 0 on success. Document that `argparse` exits with code 2 on bad input (e.g. `--name` without a value).

## Design

### CLI interface

```
usage: hello.py [-h] [--name NAME]

options:
  -h, --help            show this help message and exit
  --name NAME, -n NAME  Who to greet (default: Looper)
```

### File structure

```
hello.py
├── #!/usr/bin/env python3  (shebang)
├── """docstring"""
├── import argparse
├── def build_parser() -> argparse.ArgumentParser   (top‑level, importable)
├── def main(argv: list[str] | None = None) -> None (top‑level, importable)
└── if __name__ == "__main__": main()
```

### Function contract

#### `build_parser() -> argparse.ArgumentParser`

- No arguments.
- Returns an `ArgumentParser` with:
  - Program name: `hello.py` (auto‑derived).
  - Description: `"Print a greeting."` (short, one line).
  - One optional argument:
    - Long flag: `--name`
    - Short flag: `-n`
    - Metavar: `NAME`
    - Default: `"Looper"`
    - Help text: `"Who to greet"`

#### `main(argv: list[str] | None = None) -> None`

- If `argv` is `None`, `parse_args` reads from `sys.argv[1:]` (argparse default).
- Calls `build_parser()`, parses args, prints the greeting string.
- The greeting string follows the format: `"Hello from {name}!"`.

## Test plan

Tests can be run with `python -m doctest hello.py -v` if inline doctests are added, or simply verified manually with the following cases:

| Input | Expected output |
|---|---|
| `python hello.py` | `Hello from Looper!` |
| `python hello.py --name World` | `Hello from World!` |
| `python hello.py -n Alice` | `Hello from Alice!` |
| `python hello.py --name "John Doe"` | `Hello from John Doe!` |
| `python hello.py --name` | Non‑zero exit (2), error to stderr |

## Edge cases

- `--name` supplied multiple times → argparse default behavior (last value wins). Acceptable.
- `--name` with empty string `""` → prints `Hello from !`. Acceptable (user's explicit choice).
- No arguments → default `"Looper"` used.
- Unknown flags (e.g. `--foo`) → argparse exits with code 2 and prints usage to stderr.

## Implementation steps

1. Create `hello.py` with shebang, docstring, and imports.
2. Implement `build_parser()` with `--name`/`-n` flag.
3. Implement `main()` that delegates to `build_parser()` and prints the greeting.
4. Add the `if __name__ == "__main__"` guard calling `main()`.
5. Verify all test cases pass.
6. Commit with message: `feat: add hello.py script with argparse --name support (#72)`
   Footer: `Co-Authored-By: Claude <noreply@anthropic.com>`
