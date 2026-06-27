# Issue #46 — Build a Markdown-Based To-Do Tracker

## Overview

Create a single-file CLI tool `todo.py` that manages a simple to-do list stored in a markdown
file (`TODO.md`). Tasks are represented as checkboxes (`- [ ]` for pending, `- [x]` for done)
with auto-incrementing integer IDs.

---

## 1. File & Dependencies

- **File**: `todo.py` at the repository root.
- **Dependencies**: Python stdlib only — `argparse`, `re`, `pathlib`. No pip packages.

---

## 2. Data Format (`TODO.md`)

```markdown
# Todo

- [ ] 1. buy milk
- [ ] 2. call mom
- [x] 3. finish homework
```

- The file **always** starts with a `# Todo` header, followed by a blank line, then task lines.
- Each task line follows the regex: `- [ ] <id>. <description>` or `- [x] <id>. <description>`.
- IDs are positive integers, assigned monotonically (never reused after deletion).
- The file lives in the CWD where `todo.py` is invoked.

---

## 3. CLI Interface

All operations are single-run (no persistent server). The script inspects/modifies `TODO.md`
in the current directory and exits.

| Command                         | Action                              |
|---------------------------------|-------------------------------------|
| `python todo.py`                | Show all tasks (alias for `--show`) |
| `python todo.py --show`         | Show all tasks                      |
| `python todo.py --add "buy milk"` | Add a new pending task            |
| `python todo.py --done 3`       | Mark task `3` as done               |
| `python todo.py --rm 2`         | Remove task `2` from the file       |
| `python todo.py --clear`        | Remove all completed tasks          |

Use `argparse` with mutually exclusive flags.

---

## 4. Behaviour & Edge Cases

### 4.1 Empty / Missing TODO.md
- **Missing file**: create it automatically with the `# Todo` header (and trailing blank line).
- **File exists but has no `# Todo` header — or contains only the header and no tasks**: print
  `"No tasks"` when showing. Add/done/rm/clear still attempt to operate on the parsed content.

### 4.2 Adding tasks (`--add`)
- Assign the next available ID:
  - Scan existing tasks for the largest id; new id = max_id + 1.
  - If the file is empty (header only, no tasks), start at `1`.
- Append the new task line after any existing tasks.
- Duplicate text is allowed — every `--add` creates a separate entry.

### 4.3 Completing tasks (`--done`)
- Change `- [ ]` to `- [x]` for the matching task id.
- **Invalid id**: print `"Task <id> not found"` and exit with code 1.

### 4.4 Removing tasks (`--rm`)
- Delete the entire line for the matching task id.
- Remaining lines keep their ids intact (no renumbering).
- **Invalid id**: print `"Task <id> not found"` and exit with code 1.

### 4.5 Clearing done tasks (`--clear`)
- Delete every line where the status is `[x]`.
- If no tasks are done, do nothing (exit cleanly).

### 4.6 Showing tasks (`--show` / default)
- Print each task line in order, prefixed with `"  "` so it looks tidy.
- If no tasks exist (header only), print `"No tasks"`.

---

## 5. Error Handling

- **File I/O errors** (permission denied, unwritable directory): catch `OSError` / `PermissionError`,
  print a descriptive message, and exit with code 1.
- **Invalid `--done` / `--rm` id** (non-integer, negative): argparse `type=int` handles this,
  producing a standard usage error.
- **Conflicting flags**: argparse `add_mutually_exclusive_group` ensures only one action per
  invocation.

---

## 6. Implementation Plan

### Step 1 — Create `todo.py` with docstring and `__main__` block
- Shebang `#!/usr/bin/env python3`
- Module-level docstring with usage examples.
- Guard: `if __name__ == "__main__": main()`

### Step 2 — Parse CLI with `argparse`
- One optional positional (no-argument → `--show`).
- Mutually exclusive group for `--show`, `--add`, `--done`, `--rm`, `--clear`.

### Step 3 — File helper functions
- `todo_path()` → `Path("TODO.md")`.
- `ensure_header()` → create file with header if missing.
- `parse_tasks(content: str)` → return list of `(id, status, description)` tuples.
- `render_tasks(tasks)` → produce valid TODO.md content.
- `max_id(tasks)` → largest id (0 if empty).

### Step 4 — Implement operations
- `cmd_show()` — parse and print, or "No tasks".
- `cmd_add(text)` — parse → max_id+1 → append.
- `cmd_done(task_id)` — parse → find → toggle status → rewrite.
- `cmd_rm(task_id)` — parse → find → remove line → rewrite.
- `cmd_clear()` — parse → filter out done → rewrite.

### Step 5 — Handle edge cases
- Missing → auto-create per **4.1**.
- Invalid id → `"Task <id> not found"` + exit 1 per **4.3**, **4.4**.
- I/O errors → catch and report per **5**.

---

## 7. Testing (manual / smoke)

1. Run `python todo.py` on a missing file → creates `TODO.md`, prints "No tasks".
2. `python todo.py --add "first task"` → file has `- [ ] 1. first task`.
3. `python todo.py --add "second"` → line for id 2 appended.
4. `python todo.py --show` → both lines printed.
5. `python todo.py --done 1` → first line becomes `[x]`.
6. `python todo.py --rm 999` → prints "Task 999 not found", exits 1.
7. `python todo.py --clear` → removes the done line, only id 2 remains.
8. `python todo.py` → shows `- [ ] 2. second`.
9. `python todo.py --done a` → argparse rejects non-integer.
10. `python todo.py --add ""` → adds task with empty description.
