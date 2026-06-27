# Spec: Markdown-Based To-Do Tracker (#46)

## Overview

Create a single-file CLI tool `todo.py` that manages a simple to-do list stored in a
markdown file (`TODO.md`). Tasks use the GitHub-Flavored Markdown checklist syntax
(`- [ ]` / `- [x]`).

## File Location

`todo.py` at the repository root (sibling of `greeting.py`).

## Dependencies

Python stdlib only:
- `argparse` — argument parsing
- `re` — regex for parsing tasks from markdown
- `pathlib` — file path management

Zero external packages.

## Data File: `TODO.md`

Stored as a flat markdown file in the same directory as `todo.py`.

```markdown
# Todo

- [ ] 1. buy milk
- [ ] 2. call mom
- [x] 3. finish homework
```

Each task checkbox is prefixed with `<task-id>. <description>`.

## CLI Interface

| Command | Behaviour |
|---|---|
| `python todo.py` or `python todo.py --show` | Print all tasks grouped as Pending / Done |
| `python todo.py --add "buy milk"` | Append a new pending task with next available id |
| `python todo.py --done <id>` | Mark task `<id>` as `- [x]` (done) |
| `python todo.py --rm <id>` | Remove the task line entirely |
| `python todo.py --clear` | Remove all done (`- [x]`) lines, keep pending tasks |

## Module Structure

```
todo.py
├── _TODO_FILE: Path            — constant for TODO.md location
├── Task(NamedTuple)            — id: int, description: str, done: bool
│
├── load_tasks() -> list[Task]  — parse TODO.md into Task objects
│   ├── file missing → create with "# Todo" header → return []
│   ├── no "# Todo" header → print "No tasks" → return []
│   └── regex: r'^- \[([ x])\] (\d+)\. (.+)$' per line
│
├── save_tasks(tasks) -> None   — write Task list back to TODO.md
│
├── show_tasks(tasks) -> None   — print grouped view
│   ├── "No tasks" if empty
│   ├── "### Pending" section → pending tasks listed by id
│   └── "### Done" section → done tasks listed by id
│
├── add_task(tasks, text) -> None   — load → append → save
│
├── done_task(task_id) -> None       — load → find → flip → save
│   ├── Invalid id → "Task <id> not found"
│   └── Already done → no-op (stays done)
│
├── rm_task(task_id) -> None         — load → find → remove line → save
│   └── Invalid id → "Task <id> not found"
│
├── clear_done() -> None             — load → filter done → save
│   └── No done tasks → print "No done tasks to clear"
│
├── parse_args(argv) -> Namespace   — argparse setup
│
├── main() -> None                  — dispatch
│
└── __main__ block
```

## Edge Cases & Design Decisions

1. **Missing TODO.md** — auto-create with `# Todo` header on first access.
2. **Missing `# Todo` header** — treat as empty, print "No tasks".
3. **Invalid task id** — print `Task <id> not found"` to stderr.
4. **Task id assignment** — auto-incrementing integers starting from 1.
   When adding, scan all existing ids and pick `max(existing_ids) + 1`.
   Deleted ids are never reused.
5. **Duplicate text** — allowed; same description gets a new id.
6. **Deleted tasks** — line is fully removed from TODO.md.
   Remaining task ids are kept intact (not renumbered).
7. **Already-done on `--done`** — idempotent (stays done, no error).
8. **Clear on empty done list** — print "No done tasks to clear".
9. **File I/O errors** — print descriptive message to stderr, exit 1.
10. **`--show` with no tasks** — print "No tasks".

## Error Handling

All errors exit with `sys.exit(1)` and an error message to stderr:
- File read/write failures → `"Error: <description>"`
- Invalid task id → `"Task <id> not found"`
- Unknown arguments → argparse handles automatically

## Implementation Order

1. Create `todo.py` with full module skeleton and `parse_args()`
2. Implement `load_tasks()` and `save_tasks()`
3. Implement `add_task()`
4. Implement `show_tasks()`
5. Implement `done_task()`
6. Implement `rm_task()`
7. Implement `clear_done()`
8. Verify manually: run each command variant
9. Update `README.md` with usage section
