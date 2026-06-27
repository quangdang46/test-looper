# Spec: Add a file statistics script

Issue: #164

---

## Objective

Create a new `filestats.py` script that reads a file and reports basic statistics — line count, word count, character count, and byte count — via a clean CLI interface built on `argparse`. The script exposes a reusable `stats()` function that returns a dictionary so callers can integrate it programmatically without going through the CLI.

## Implementation Plan

1. **Create `filestats.py`** at the repo root — a new executable Python script.
   - Add `#!/usr/bin/env python3` shebang, matching the project convention (see `hello.py`, `greeting.py`).
   - Define `stats(filename: str) -> dict[str, int]` that:
     - Opens the file in binary read mode (`"rb"`) to get an accurate byte count.
     - Decodes to text for line/word/char counting.
     - Returns `{"lines": <int>, "words": <int>, "chars": <int>, "bytes": <int>}`.
   - Use `os.path.exists()` (or a `try`/`except FileNotFoundError`) before opening to return a clear error for missing files.
   - Handle empty files correctly — all four statistics should be `0`, not an error.
   - Handle files with a trailing newline — count should match conventional `wc` behavior (last line with no trailing newline still counts as a line).
   - Define `main()` that:
     - Creates an `argparse.ArgumentParser` with description `"Display file statistics."`.
     - Declares `--filename` as a required argument (use `required=True`).
     - Calls `stats(args.filename)` and prints the results in the format shown below.
   - Guard with `if __name__ == "__main__": main()`.
   - Add type annotations consistent with the existing codebase (`def main() -> None`, etc.).

2. **Output format** — after calling `stats()`, print each statistic on its own line:
   ```
   Lines: N
   Words: N
   Characters: N
   Bytes: N
   ```
   The capitalization and spacing match the issue's example exactly.

3. **Verify correctness** — run against `README.md` (repo root), a non-existent file, and an empty file to confirm edge cases.

## Files to Change

| File | Action | Notes |
|---|---|---|
| `filestats.py` | **Create** (at repo root) | New executable script. Defines `stats(filename)` returning a dict and a `main()` CLI entry point using `argparse --filename`. |
| No other files | untouched | `greeting.py`, `hello.py`, `README.md` remain unchanged. |

## Risks

- **Binary vs text mode** — Using text mode then calling `len(text)` for character count is correct, but byte count requires binary mode or `os.stat()`. If the file is opened in text mode and `len()` is used on the text, that gives character count, not byte count — CSV/encoding mismatches could inflate or deflate the byte count. **Mitigation**: open in binary mode (`"rb"`), decode for text counts, use `len(raw_bytes)` for the byte field.
- **Word boundary definition** — Python's `str.split()` splits on any whitespace, which matches the issue's implied `wc`-like behavior. However, if a future requirement asks to match `wc -w` semantics more precisely (e.g., handling punctuation differently), the word-splitting logic would need revisiting. For this issue, `split()` is sufficient.
- **Large files** — The current implementation reads the entire file into memory. For this repo's scale (small scripts, tiny README) this is acceptable. If the script were used on multi-GB files later, a streaming approach would be needed.
- **Trailing newline conventions** — Counting lines by `text.splitlines()` or `text.count("\n")` can disagree by 1 on a file that ends without a newline. The `stats()` function should document its line-counting strategy (e.g., `len(text.splitlines())` counts the last line even without a trailing newline, matching Unix `wc -l` behavior).
- **Argparse required flag** — Using `required=True` on `--filename` is intentional (the issue says "required"), but this is an uncommon argparse pattern — most required arguments are positional. If the user finds this surprising, the flag could be migrated to a positional argument in a follow-up.

## Acceptance Criteria

1. `python3 filestats.py --filename README.md` prints four lines — `Lines:`, `Words:`, `Characters:`, `Bytes:` — with non-negative integer values for README.md.
2. `python3 filestats.py --filename nonexistent-file.txt` exits with a non-zero exit code and prints a clear error message (e.g., `Error: file not found`).
3. `python3 filestats.py --filename /dev/null` (or an empty temp file) prints `Lines: 0`, `Words: 0`, `Characters: 0`, `Bytes: 0`.
4. `python3 filestats.py --help` prints a help message describing the `--filename` flag.
5. `python3 filestats.py --unknown-flag` exits with a non-zero exit code and prints an argparse error.
6. `python3 filestats.py` (without `--filename`) exits with a non-zero exit code and prints an error that `--filename` is required.
7. The `stats()` function can be imported and called directly: `python3 -c "from filestats import stats; print(stats('README.md'))"` prints a dict with the four expected keys.
8. No existing files (`greeting.py`, `hello.py`, `README.md`) are modified.
9. All existing tests for `greeting.py` and `hello.py` still pass.

Spec: specs/164-spec/spec.md
