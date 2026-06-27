# Spec — Markdown-based To-Do Tracker (`todo.py`)

Issue: [#46](https://github.com/quangdang46/test-looper/issues/46)

## Overview

Build a single-file CLI tool `todo.py` that manages a simple to-do list backed by a
markdown file (`TODO.md`). Tasks are stored as markdown checklist items with numeric IDs.

## File

`todo.py` — a single file at the repository root. No external dependencies; only
Python stdlib (`argparse`, `re`, `pathlib`, `sys`).

## Data Format

`TODO.md` (in the same directory as `todo.py`):

```markdown
# Todo

- [ ] 1. buy milk
- [ ] 2. call mom
- [x] 3. finish homework
```

- The file always starts with the header `# Todo` followed by a blank line.
- Each task line: `- [ ] <id>. <description>` (pending) or `- [x] <id>. <description>` (done).
- Task IDs are positive integers, auto-incremented from 1.
- IDs of deleted tasks are **never reused**.
- The file ends with a single trailing newline.

## CLI Interface

| Command | Example | Behavior |
|---|---|---|
| Show | `python todo.py` or `python todo.py --show` | Print all tasks grouped by status. |
| Add | `python todo.py --add "buy milk"` | Append a new pending task. |
| Done | `python todo.py --done 3` | Mark task 3 as completed (`[ ]` → `[x]`). |
| Remove | `python todo.py --rm 3` | Delete task 3 from file entirely. |
| Clear | `python todo.py --clear` | Remove all completed (done) tasks. |

## Implementation Steps

### Step 1 — Scaffold and data-layer functions

Create `todo.py` with:

- **`TODO_PATH`** — path to `TODO.md` resolved relative to `todo.py`'s directory.
- **`ensure_file()`** — create `TODO.md` with the `# Todo` header if it doesn't exist.
- **`parse_tasks(content: str) -> list[dict]`** — return a list of dicts with keys
  `id`, `desc`, `done`, `raw`. Rejects lines that don't match the task pattern.
- **`serialize_tasks(tasks: list[dict]) -> str`** — convert the task list back to
  markdown text (header + blank line + task lines).
- **`next_id(tasks: list[dict]) -> int`** — return `max(existing ids) + 1` (or `1` if empty).
- **`read_todo() -> list[dict]`** — read+parse `TODO.md`. On missing file, create it
  and return `[]`.
- **`write_todo(tasks: list[dict]) -> None`** — serialize and write `TODO.md`.

All file I/O errors raise `OSError` / `IOError`.

### Step 2 — Command handlers

Implement these free functions, each returning a message string:

- **`cmd_show(tasks)`** — print tasks split into two groups: "Pending" and "Done".
  Each line: `<id>. <description>`. If no tasks exist, print "No tasks." and exit.
- **`cmd_add(tasks, text)`** — create a new pending task with `next_id()`, append,
  write, return `"Added task <id>."`.
- **`cmd_done(tasks, raw_id)`** — look up by id, set `done=True`, write,
  return `"Task <id> marked as done."`. On not-found, print `"Task <id> not found"`
  and exit.
- **`cmd_rm(tasks, raw_id)`** — look up by id, remove the task from the list, write,
  return `"Removed task <id>."`. On not-found, print `"Task <id> not found"` and exit.
- **`cmd_clear(tasks)`** — filter out done tasks, write, return `"Cleared <N> done task(s)."`.
  If none are done, print `"No done tasks to clear."` and exit.

### Step 3 — `__main__` block

```python
if __name__ == "__main__":
    main()
```

### Step 4 — `main()` with argparse

- Use `argparse` for argument parsing.
- Mutually exclusive options `--show`, `--add`, `--done`, `--rm`, `--clear`.
- If no flags given, default to `--show`.
- Call the appropriate handler and print its return value.
- Wrap the handler dispatch in `try/except (OSError, IOError)` to print a user-friendly
  error and `sys.exit(1)`.

### Step 5 — Error handling & edge cases

| Scenario | Behavior |
|---|---|
| `TODO.md` missing | Auto-create with `# Todo` header on first read. |
| Empty file (or `# Todo` with no tasks) | `cmd_show` → `"No tasks."` |
| `--done` / `--rm` with non-existent id | `"Task <id> not found"` then `sys.exit(1)` |
| `--clear` with no done tasks | `"No done tasks to clear."` then `sys.exit(1)` |
| Duplicate task text | Allowed — same text creates a new task with a new id. |
| File write failure | `sys.exit(1)` with the OS error message. |
| Task-id overflow | Not handled in v1 (int is unbounded in Python 3). |
| Blank description (`--add ""`) | Allowed — creates a task with empty description. |

### Step 6 — Docstring & usage

Top-level docstring:

```
"""Markdown-based to-do tracker.

Usage:
    python todo.py                  show tasks (default)
    python todo.py --show           show tasks
    python todo.py --add "text"     add a task
    python todo.py --done <id>      mark task as done
    python todo.py --rm <id>        remove a task
    python todo.py --clear          clear all done tasks
"""
```

## File Dependencies

`todo.py` imports only: `argparse`, `re`, `pathlib`, `sys`.

## Testing Strategy (manual)

After implementation, smoke-test each command:

```bash
# 1. Show (empty, file auto-created)
python todo.py                           # → "No tasks."

# 2. Add tasks
python todo.py --add "buy milk"          # → "Added task 1."
python todo.py --add "call mom"          # → "Added task 2."
python todo.py --add "finish homework"   # → "Added task 3."

# 3. Show (with tasks)
python todo.py                           # → Pending list with 3 items

# 4. Mark done
python todo.py --done 3                  # → "Task 3 marked as done."
python todo.py                           # → 2 pending, 1 done

# 5. Remove
python todo.py --rm 2                    # → "Removed task 2."
python todo.py                           # → 1 pending, 1 done

# 6. Clear
python todo.py --clear                   # → "Cleared 1 done task(s)."
python todo.py                           # → 1 pending, 0 done

# 7. Invalid id
python todo.py --done 99                 # → "Task 99 not found"
python todo.py --rm 99                   # → "Task 99 not found"

# 8. Verify TODO.md format
cat TODO.md
```
