# Spec: Markdown-Based To-Do Tracker

**Issue:** [#46](https://github.com/quangdang46/test-looper/issues/46)
**File:** `todo.py`
**Date:** 2026-06-27

## 1. Overview

Build a single-file Python CLI (`todo.py`) that manages a task list stored in a
markdown file (`TODO.md`). Use only the Python standard library — zero external
dependencies.

---

## 2. Interface (CLI)

| Command | Description |
|---------|-------------|
| `python todo.py [--show]` | Print all tasks |
| `python todo.py --add "buy milk"` | Append a new task |
| `python todo.py --done <id>` | Mark task as completed (`- [x]`) |
| `python todo.py --rm <id>` | Delete a task entirely |
| `python todo.py --clear` | Remove all completed tasks |

Arguments are mutually exclusive (except `--show` is the default if no flag is
given). The program exits with a non-zero code on error and zero on success.

---

## 3. File Format (`TODO.md`)

```
# Todo

- [ ] 1. buy milk
- [ ] 2. call mom
- [x] 3. finish homework
```

- The file always begins with `# Todo` followed by a blank line.
- Each task is `- [ ] <id>. <description>` (pending) or `- [x] <id>. <description>` (done).
- Ids are **consecutive integers** that start at 1 and never get reused.
- Ids are assigned at creation time as `max(existing ids) + 1`, or `1` for an
  empty list.

---

## 4. Module Structure

All logic lives in one file, `todo.py`. Internal decomposition:

```
todo.py
├── FILE = Path("TODO.md")           # markdown storage file
├── HEADER = "# Todo\n\n"            # file header template
├── TASK_RE = re.compile(...)        # compile regex once at module scope
├── parse_tasks(text)                # str -> list[dict]
│   Parses raw file text into structured task dicts.
│   Returns list of {id: int, desc: str, done: bool}.
│   If no tasks, returns [].
│
├── format_tasks(tasks)              # list[dict] -> str
│   Formats task list back into markdown string.
│   Prepends HEADER + blank line.
│
├── load_tasks()                     # -> list[dict]
│   Reads TODO.md from disk.
│   If missing → creates file with HEADER → returns [].
│   If file exists but has no content or no header → returns [].
│
├── write_tasks(tasks)               # None
│   Formats and writes TODO.md to disk.
│
├── show_tasks(tasks)                # None
│   Pretty-prints tasks to stdout.
│   Empty list → prints "No tasks".
│
├── add_task(tasks, desc)            # list[dict]
│   Appends new task with next id.
│   Id = max(existing ids, 0) + 1.
│
├── done_task(tasks, task_id)        # list[dict]
│   Sets done=True for matching id.
│   Raises LookupError("Task <id> not found") on mismatch.
│
├── remove_task(tasks, task_id)      # list[dict]
│   Removes the dict from the list entirely.
│   Raises LookupError("Task <id> not found") on mismatch.
│
├── clear_done(tasks)                # list[dict]
│   Filters out all tasks where done == True.
│
└── if __name__ == "__main__":       # main()
    Argparse setup, dispatch via if/elif chain, error handler.
```

---

## 5. Data Flow

```
User CLI input
  │
  ▼
argparse (parse args, enforce mutual exclusion)
  │
  ▼
load_tasks()     ────  file missing?  ──►  create TODO.md with header
  │
  ▼
dispatch via if/elif:
  ┌────────────┬───────────────┬────────────────────────────┐
  │ --show     │ show_tasks()  │ print tasks to stdout      │
  │ --add      │ add_task()    │ write_tasks(), print added │
  │ --done     │ done_task()   │ write_tasks(), print done  │
  │ --rm       │ remove_task() │ write_tasks(), print rm    │
  │ --clear    │ clear_done()  │ write_tasks(), print count │
  └────────────┴───────────────┴────────────────────────────┘
                │
                ▼
           sys.exit(0) or sys.exit(1) on error
```

---

## 6. Edge Cases & Error Handling

| Scenario | Behavior |
|----------|----------|
| `TODO.md` does not exist | `load_tasks()` creates it with `# Todo\n\n`. No error. |
| `TODO.md` exists but is empty | Treat as no tasks — prints "No tasks" on show. |
| `TODO.md` has no `# Todo` header | Treat as no tasks (same as empty). |
| Stale task ids after deletion | Ids are *never* reused. Next id = `max(remaining_ids, 0) + 1`. |
| `--done` / `--rm` with nonexistent id | Print `"Task <id> not found"` to stderr, exit 1. |
| `--add` with empty/blank description | Print error to stderr — "Task description cannot be empty", exit 1. |
| I/O error (permissions, disk full) | Catch `OSError` / `PermissionError`, print message to stderr, exit 1. |
| No arguments given | Default to `--show` behavior. |
| Duplicate task text | Allowed — same text gets a new id. |
| Malformed task line in TODO.md | Skip lines that don't match `- [ ]` or `- [x]` pattern (preserves them). |

---

## 7. Task Parsing Regex

```python
TASK_RE = re.compile(r'^- \[([ x])\] (\d+)\.\s*(.+)$', re.MULTILINE)
```

- Group 1: ` ` (pending) or `x` (done)
- Group 2: numeric id
- Group 3: description

---

## 8. Implementation Order

1. **Module scaffold** — argparse setup with `--show`, `--add`, `--done`, `--rm`,
   `--clear`, and mutual-exclusion group.
2. **`parse_tasks` / `format_tasks`** — the two core serialization functions.
3. **`load_tasks` / `write_tasks`** — file I/O with create-if-missing logic.
4. **`show_tasks`** — print logic with "No tasks" fallback.
5. **`add_task`** — append, auto-increment id.
6. **`done_task`** — mark done, error on missing id.
7. **`remove_task`** — delete entry, error on missing id.
8. **`clear_done`** — filter out completed tasks.
9. **`__main__` dispatch** — wire argparse to handlers with try/except.
10. **Docstring & usage** — module docstring with CLI examples.
11. **One manual smoke test** — run each flag once to confirm.
