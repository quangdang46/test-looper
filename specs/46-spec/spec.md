# Issue #46 — Build a Markdown-Based To-Do Tracker

**Design doc** for `todo.py`: a zero-dependency CLI that manages a task list stored in `TODO.md`.

---

## 1. Overview

A single-file Python CLI (`todo.py`) using only `argparse`, `re`, and `pathlib` from the standard library. Reads/writes tasks from/to a `TODO.md` file in the current working directory using GFM checkbox notation.

---

## 2. File Format (`TODO.md`)

```markdown
# Todo

- [ ] 1. buy milk
- [ ] 2. call mom
- [x] 3. finish homework
```

- Header must be exactly `# Todo` (level-1 heading).
- Each task is a checkbox list item: `- [ ] <id>. <description>` (pending) or `- [x] <id>. <description>` (done).
- IDs are integers, auto-incremented, starting at 1.
- Deleted IDs are never reused. New tasks always get `max(existing ids) + 1`.

---

## 3. CLI Interface

All behaviour gated by mutually exclusive flags, with sensible defaults.

| Flag | Alias | Description |
|------|-------|-------------|
| `--show` | *(none)* | Print all tasks grouped by status. **Default** when no flags given. |
| `--add <text>` | *(none)* | Add a new task with the given description. |
| `--done <id>` | *(none)* | Mark task `<id>` as completed. |
| `--rm <id>` | *(none)* | Permanently delete task `<id>` from the file. |
| `--clear` | *(none)* | Remove all completed (`[x]`) tasks. |

---

## 4. Behaviour & Edge Cases

### 4.1 Missing `TODO.md`
If `TODO.md` does not exist, any *write* operation (`--add`, `--done`, `--rm`, `--clear`) creates it with the `# Todo` header automatically. A *read* operation (`--show`, or no flag) prints `"No tasks"`.

### 4.2 Missing `# Todo` header
The file exists but doesn't contain `# Todo` → behaviour is identical to missing file: write ops add the header, read ops print `"No tasks"`.

### 4.3 Empty task list
File has the header but no checkbox items → `--show` prints `"No tasks"`.

### 4.4 Invalid task ID
`--done` or `--rm` with an ID that doesn't exist in the file → prints `"Task <id> not found"` and exits with code 1.

### 4.5 Duplicate text
Adding `"buy milk"` when `"buy milk"` already exists is allowed — same text, new ID. No dedup.

### 4.6 ID reuse
Deleted IDs are **never** reused. New tasks always receive `max(existing_ids) + 1` (or `1` if the file is empty).

### 4.7 Deleted tasks
`--rm` removes the task line from `TODO.md` completely. Remaining tasks keep their original IDs.

### 4.8 File I/O errors
Any file read/write failure (permissions, disk full, etc.) prints a clear error message and exits with code 1.

### 4.9 Mutually exclusive flags
If more than one action flag is given (e.g. `--add x --done 1`), print a usage error and exit with code 2.

---

## 5. Implementation Plan

### Step 1 — Scaffold

Create `todo.py` with:
- shebang `#!/usr/bin/env python3`
- module docstring with usage examples
- `__main__` block
- imports: `argparse`, `re`, `pathlib.Path`

### Step 2 — Argument parser

```python
def parse_args() -> argparse.Namespace
```

- `--show` (store_true, mutually exclusive group)
- `--add` (str)
- `--done` (int)
- `--rm` (int)
- `--clear` (store_true)
- Mutex enforced by `add_mutually_exclusive_group`.

### Step 3 — File helpers

```python
TODO_PATH = Path("TODO.md")
TODO_HEADER = "# Todo"
```

```python
def ensure_file() -> bool
```
- If `TODO.md` doesn't exist, return `False` (caller decides whether to create).
- If it exists but has no `# Todo` header, still return `False` (same behaviour).

```python
def read_tasks() -> list[dict] | None
```
- Reads `TODO.md`, parses header and checkbox items.
- Returns `None` when file/header missing → caller prints `"No tasks"`.
- Returns list of dicts: `{"id": int, "desc": str, "done": bool}`.

```python
def write_tasks(tasks: list[dict]) -> None
```
- Writes `# Todo` header followed by sorted checkbox lines.
- Idempotent — only called after modifications.

### Step 4 — Action functions

```python
def cmd_show(tasks: list[dict]) -> None
```
- Print pending tasks, then done tasks (or one-line summaries).
- If empty list → print `"No tasks"` instead.

```python
def cmd_add(tasks: list[dict], text: str) -> list[dict]
```
- Compute next_id: `max(t["id"] for t in tasks) + 1` (or 1 if empty).
- Append `{"id": next_id, "desc": text, "done": False}`.

```python
def cmd_done(tasks: list[dict], task_id: int) -> list[dict]
```
- Find task by id, set `done = True`.
- If not found → print `"Task {task_id} not found"` and `sys.exit(1)`.

```python
def cmd_rm(tasks: list[dict], task_id: int) -> list[dict]
```
- Remove task with matching id from the list.
- If not found → print `"Task {task_id} not found"` and `sys.exit(1)`.

```python
def cmd_clear(tasks: list[dict]) -> list[dict]
```
- Return only tasks where `done == False`.

### Step 5 — Main dispatch

```python
def main() -> None
```
1. Parse args.
2. Call `ensure_file()` / `read_tasks()`.
3. If read returns `None` and command is read-only → print `"No tasks"`, exit 0.
4. If read returns `None` and command is write → initialise empty task list, proceed.
5. Dispatch to the matching `cmd_*` function.
6. If command modified tasks, call `write_tasks()` with the new list.

### Step 6 — `__main__`

```python
if __name__ == "__main__":
    main()
```

---

## 6. File Structure

```
.
├── specs/
│   └── 46-spec/
│       └── spec.md          ← this file
├── TODO.md                  ← created at runtime by todo.py
├── todo.py                  ← the CLI tool
├── greeting.py              ← existing
└── README.md                ← existing
```

One file `todo.py`, zero runtime dependencies. No tests directory required (the issue doesn't ask for tests, only a spec then implementation).

---

## 7. Error Handling Summary

| Scenario | Behaviour |
|----------|-----------|
| `TODO.md` missing (read) | `"No tasks"`, exit 0 |
| `TODO.md` missing (write) | Create file with header, then operate |
| No `# Todo` header | Treat same as missing |
| Invalid `--done <id>` | `"Task <id> not found"`, exit 1 |
| Invalid `--rm <id>` | `"Task <id> not found"`, exit 1 |
| Conflicting flags | `argparse` error, exit 2 |
| File I/O error | Print error message, exit 1 |

---

## 8. Usage (docstring)

```
Usage:
  python todo.py                    # show all tasks
  python todo.py --show             # show all tasks
  python todo.py --add "buy milk"   # add a new task
  python todo.py --done 1           # mark task 1 as done
  python todo.py --rm 2             # delete task 2
  python todo.py --clear            # remove all done tasks
```
