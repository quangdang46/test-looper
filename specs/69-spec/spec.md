# Spec: Add a simple hello.py script

Issue: #69

---

## Objective

Create a new `hello.py` script that prints a greeting using the project's "Looper" brand name, with `argparse`-based support for an optional `--name` flag. The existing `greeting.py` is left untouched — this is a complementary script, not a replacement.

---

## Implementation Plan

1. **Create `hello.py` in the repo root** with the following structure:
   - Shebang (`#!/usr/bin/env python3`) and docstring.
   - An `argparse.ArgumentParser` that accepts an optional `--name` / `-n` positional-or-keyword argument defaulting to an empty value.
   - A `greet(name: str) -> str` function that returns `"Hello from Looper!"` when `name` is empty/None, or `"Hello from Looper, {name}!"` when a name is supplied.
   - A `main()` entry point that wires argparse to the greet function and prints the result.
   - Standard `if __name__ == "__main__"` guard.

2. **Update `README.md`** (optional but recommended) — add a brief "Usage" section showing the two invocation forms. This step can be deferred or skipped if the reviewer prefers the README remain minimal.

3. **Verify correctness** — run `python hello.py` and `python hello.py --name World` to confirm output matches the spec from the issue.

---

## Files to Change

| File | Action | Notes |
|------|--------|-------|
| `hello.py` | **Create** | New script file in the repo root. Contains the argparse-based greeting logic described above. |
| `README.md` | **Maybe update** | Add a Usage section if desired; otherwise leave as-is. |

No existing files are modified beyond a possible README touch-up. `greeting.py` is not touched.

---

## Risks

- **Name collision with `greeting.py`** — the two scripts serve different purposes, but a reader may wonder why both exist. The internal formatting string is different (`"Hello from Looper"` vs `"Hello, {name}!"`) so there is no functional overlap.
- **`--name` flag accepting zero arguments from the empty default** — argparse defaults can be tricky. If the flag is designed as `--name NAME`, omitting it should produce no name (default to `None`), not an error. Must use `nargs='?'` or a default value to avoid requiring the argument when the flag is absent.
- **Edge case: empty string `--name ''`** — argparse with `nargs='?'` and an empty string on the command line will still pass `""`. The greet function should handle `None` and empty string identically.

---

## Acceptance Criteria

1. `python hello.py` prints `Hello from Looper!` with a trailing newline.
2. `python hello.py --name World` prints `Hello from Looper, World!` with a trailing newline.
3. `python hello.py -n World` (short form) produces the same output as criterion 2.
4. `python hello.py --name` (flag with no value) does **not** error — it treats the name as absent and prints `Hello from Looper!`.
5. The script has no syntax errors and exits with code 0 on success.
6. All existing files (`greeting.py`, `README.md`) remain unchanged (unless README is explicitly updated per the Implementation Plan).

---

Spec: specs/69-spec/spec.md
