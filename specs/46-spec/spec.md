# Issue #46 — Markdown-based To-Do Tracker

## Overview

Build a single-file CLI tool `todo.py` that manages a simple to-do list stored in
`TODO.md`. Tasks are persisted as GitHub-flavoured markdown checkboxes. The tool
uses only Python stdlib (`argparse`, `re`, `pathlib`).

---

## Data model

```text
TODO.md
├── # Todo                     (H1 header)
├── ──────────────────────
├── - [ ] <id>. <text>         (pending task)
├── - [x] <id>. <text>         (completed task)
├── ──────────────────────
└── <!-- last_id: N -->        (hidden comment — highest used id)
```

### Task format

Each line is one task:

```
- [ ] 1. buy milk
- [x] 2. call mom
```

- `- [ ]` / `- [x]` — checkbox state (pending / done).
- `<id>.` — integer id, dot, space, then the description text.
- Ids are **monotonically increasing** (never reused after delete).
- A deleted line is **removed entirely** from the file.

### last_id tracker

An HTML comment on the last line of the file (after a blank separator line)
stores the highest id ever assigned:

```html
<!-- last_id: 5 -->
```

This lets auto-increment survive deletions — new tasks get `last_id + 1`.

---

## CLI interface

```
python todo.py               # show tasks (alias for --show)
python todo.py --show        # show tasks
python todo.py --add <text>  # add a new task
python todo.py --done <id>   # mark a task as completed
python todo.py --rm <id>     # delete a task entirely
python todo.py --clear       # remove all completed tasks
```

All flags are **mutually exclusive** via `argparse` (the `add_mutually_exclusive_group`).

### Output conventions

| Scenario | Output |
|---|---|
| Show, tasks exist | Print each task: `1. [ ] buy milk` / `1. [x] call mom` |
| Show, no tasks | Print `"No tasks"` |
| Show, `# Todo` header missing | Re-create header (see below), then print `"No tasks"` |
| Show, file missing | Create file with header, print `"No tasks"` |
| `--add "text"`, success | Print `"Added task <id>: <text>"` |
| `--add` with empty text | Print `"Error: task text cannot be empty"` to stderr, exit 1 |
| `--done <id>`, success | Print `"Marked task <id> as done"` |
| `--done <id>`, already done | Still print `"Marked task <id> as done"` (idempotent) |
| `--done <id>`, not found | Print `"Error: task <id> not found"` to stderr, exit 1 |
| `--rm <id>`, success | Print `"Removed task <id>"` |
| `--rm <id>`, not found | Print `"Error: task <id> not found"` to stderr, exit 1 |
| `--clear`, no done tasks | Print `"No completed tasks to clear"` |
| `--clear`, some cleared | Print `"Cleared <N> completed task(s)"` |
| File I/O error | Print `"Error: <description>"` to stderr, exit 1 |

---

## Edge cases and error handling

### Missing file
If `TODO.md` does not exist, all commands create it with the header `# Todo`
(and the `<!-- last_id: 0 -->` footer if needed). Show then prints `"No tasks"`.

### Empty / malformed file
If the file exists but has no `# Todo` header, the parser prints `"No tasks"`
and **re-creates** the file with a fresh header (overwriting the corrupt content).
Other mutating commands (`--add`, `--done`, `--rm`, `--clear`) prepend the header
so the file stays valid.

### Invalid task id
`--done` / `--rm` with a non-integer or absent id is caught by `argparse` type
check. An integer id that does not match any task line prints
`"Error: task <id> not found"` to stderr and exits 1.

### Duplicate text
Adding `"buy milk"` twice creates two separate task lines — duplicate text is allowed.

### Empty task text
`--add ""` is rejected with `"Error: task text cannot be empty"` to stderr and exit 1.

### Idempotent done
Marking an already-done task succeeds silently (same success message).

### Deleted ids are not reused
The `<!-- last_id: N -->` comment tracks the highest id ever assigned. New tasks
always get `last_id + 1`, so a deleted id is never reused.

### Concurrency
No locking. Designed for single-user/single-process editing. Concurrent edits
may lose the race — this is acceptable for the scope.

---

## Architecture (single file `todo.py`)

```python
#!/usr/bin/env python3
"""todo.py — Markdown-based to-do list. Usage: python todo.py [--show|--add ...]"""

import argparse
import re
import sys
from pathlib import Path

TODO_FILE = Path("TODO.md")
HEADER = "# Todo"
LAST_ID_RE = re.compile(r"<!--\s*last_id:\s*(\d+)\s*-->")
TASK_LINE_RE = re.compile(r"^- \[([ x])\] (\d+)\.\s+(.*)$")
```

### Function outline

| Function | Purpose |
|---|---|
| `read_todo()` | Parse `TODO.md` → `(tasks: list[dict], last_id: int)` |
| `write_todo(tasks, last_id)` | Serialize tasks + footer back to `TODO.md` |
| `ensure_todo_file()` | Create file with header if missing |
| `cmd_show()` | List tasks or print `"No tasks"` |
| `cmd_add(text)` | Append a new task, increment `last_id` |
| `cmd_done(task_id)` | Flip `- [ ]` to `- [x]` (idempotent) |
| `cmd_rm(task_id)` | Remove the task line entirely |
| `cmd_clear()` | Remove all `done=True` tasks |

### Parser details

**`read_todo()`**:
1. If file missing → return `([], 0)` (caller creates file on mutation).
2. Read all lines.
3. Find the `<!-- last_id: N -->` footer → capture N.
4. Match each line against `TASK_LINE_RE` → extract `(done, id, text)`.
5. Lines that don't match are ignored (comments, blank lines, unknown syntax).
6. Return `(tasks, last_id)`.

**`write_todo(tasks, last_id)`**:
1. Build output: header line, blank line, sorted task lines, blank line, footer.
2. Write atomically: write to `TODO.md.tmp`, then `Path.rename()`.

### `__main__` block

```python
if __name__ == "__main__":
    main()
```

`main()` dispatches via match/case on the selected argparse action.

---

## Implementation steps

1. **Create `todo.py` scaffold** — shebang, docstring, imports, `Path("TODO.md")`,
   regex constants.

2. **Implement `read_todo()` / `write_todo()`** — parse and serialize the file.
   Handle missing file gracefully (return `([], 0)`).

3. **Implement `ensure_todo_file()`** — write header + last_id: 0 if file absent.

4. **Implement `cmd_show()`** — call `read_todo()`, print tasks or `"No tasks"`.

5. **Implement `cmd_add(text)`** — call `ensure_todo_file()` if missing, parse,
   append new task with `last_id + 1`, write back, print confirmation.

6. **Implement `cmd_done(task_id)`** — parse, find task by id, flip checkbox,
   write back, print confirmation. Handle not-found.

7. **Implement `cmd_rm(task_id)`** — parse, find by id, remove from list,
   write back with same `last_id` (do NOT decrement), print confirmation.
   Handle not-found.

8. **Implement `cmd_clear()`** — filter out done tasks, write back, print count.

9. **Build argparse dispatcher** — mutually exclusive group for `--show`
   (default), `--add`, `--done`, `--rm`, `--clear`. Wire each to its `cmd_*`.

10. **Error handling pass** — wrap file I/O in try/except, print to stderr,
    exit 1. Validate empty text for `--add`.

11. **Add docstring usage** at module level.

---

## Acceptance criteria

- `python todo.py` → shows tasks or `"No tasks"`
- `python todo.py --add "buy milk"` → adds task with id 1
- `python todo.py --done 1` → marks task 1 as done
- `python todo.py --rm 1` → removes task 1 entirely
- `python todo.py --clear` → removes all done tasks
- Empty/missing TODO.md → auto-created
- Invalid id → `"Task <id> not found"` on stderr, exit 1
- Deleted ids never reused (verify by adding, removing, adding — third task gets id 2)
- No external dependencies beyond Python stdlib
