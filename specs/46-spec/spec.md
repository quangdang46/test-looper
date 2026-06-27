# Implementation Plan: Markdown-based To-do Tracker (Issue #46)

## Summary

Build a single-file CLI tool `todo.py` (Python stdlib only) that manages a to-do list stored in `TODO.md`. Tasks are represented as GitHub-flavored markdown checkboxes with auto-incrementing integer IDs. The tool supports show, add, mark-done, remove, and clear-done operations.

---

## 1. File Structure

```
repo-root/
├── todo.py              # The CLI tool (single file, ~180 lines)
├── TODO.md              # Task store (auto-created, managed by todo.py)
├── specs/46-spec/
│   └── spec.md          # This document
└── greeting.py          # Existing — untouched
```

---

## 2. Architecture

`todo.py` uses a **parser-generator pattern** with three internal layers:

| Layer | Responsibility | Functions |
|---|---|---|
| **File I/O** | Read/write `TODO.md`, handle missing file | `_read_todo()`, `_write_todo()` |
| **Parsing & Rendering** | Parse markdown→tasks, render tasks→markdown | `_parse_tasks()`, `_render_tasks()` |
| **Business Logic** | CLI dispatch, add/done/remove/clear/show | `main()` + dispatcher |

No classes — flat functions with a shared `TODO_PATH` constant.

---

## 3. Task Data Model

Each task is a `dict` with two keys:

```python
{"id": int, "done": bool, "text": str}
```

Parsed from lines matching the regex:

```
^\-\s+\[\s*([ xX]?)\s*\]\s+(\d+)\.\s+(.+)$
```

- Group 1: checkbox state (` `, `x`, `X`) → `done: bool`
- Group 2: task ID (integer)
- Group 3: task description text

Non-matching lines and blank lines are preserved verbatim as **separators** (keep the markdown structure intact when round-tripping).

---

## 4. File Format (`TODO.md`)

```markdown
# Todo

- [ ] 1. buy milk
- [ ] 2. call mom
- [x] 3. finish homework
```

### On-disk conventions
- Header line is always `# Todo`
- One blank line after the header
- Each task on its own line
- No trailing whitespace on task lines
- Files always end with a single newline (POSIX)

### Separator lines
Any line that does not match a task line is treated as a **separator** — it is stored in an ordered list and emitted back verbatim during writes. This preserves:
- The `# Todo` header
- Blank lines between header and first task
- Any free-form text the user might add below the task list

---

## 5. CLI Interface

```text
usage: todo.py [-h] [--show] [--add TEXT] [--done ID] [--rm ID] [--clear]

Markdown-based to-do tracker. Tasks stored in TODO.md.

options:
  -h, --help   show this help message and exit
  --show       Show all tasks
  --add TEXT   Add a new task with the given description
  --done ID    Mark a task as completed by its ID
  --rm ID      Remove a task by its ID
  --clear      Remove all completed tasks
```

### Argument precedence (mutual exclusivity)
Only one action flag is honored per invocation, checked in this priority order:

1. `--add` → `cmd_add(text)`
2. `--done` → `cmd_done(task_id)`
3. `--rm` → `cmd_rm(task_id)`
4. `--clear` → `cmd_clear()`
5. (none, or `--show`) → `cmd_show()`

If multiple flags are passed, the highest-priority one runs and the rest are ignored (no error).

---

## 6. Function Details

### 6.1 File I/O

#### `TODO_PATH: Path = Path("TODO.md")`

#### `_read_todo() -> list[dict] | None`
- If `TODO_PATH` does not exist → return `None` (triggers auto-create in caller)
- If `TODO_PATH` exists but is empty or lacks `# Todo` header → return `[]` (empty task list)
- Read file line by line, separate tasks from non-task (separator) lines
- Return the list of parsed task dicts
- **Errors**: wrap IOError → print error message and `sys.exit(1)`

#### `_write_todo(tasks: list[dict]) -> None`
- Build output lines: header `# Todo\n\n`, then for each task render `"- [ ] {id}. {text}"` or `"- [x] {id}. {text}"`
- Join with `\n`, append trailing newline, write to `TODO_PATH`
- **Errors**: wrap IOError → print error message and `sys.exit(1)`

### 6.2 Parsing & Rendering

#### `_parse_tasks(lines: list[str]) -> list[dict]`
- Regex: `r"^- \[([ xX])\] (\d+)\. (.+)"`
- For each line that matches → parse into task dict
- Non-matching lines → skip (they are separators, but we don't need to track them for the basic implementation since we always rewrite the file cleanly)
- Return list of task dicts sorted by `id`

#### `_render_tasks(tasks: list[dict]) -> str`
- Return `"# Todo\n\n" + "\n".join(render_line(t) for t in tasks) + "\n"`
- Each line: `f"- [{'x' if t['done'] else ' '}] {t['id']}. {t['text']}"`

### 6.3 Commands

All commands follow the same pattern:
1. Call `_read_todo()` → get task list
2. Perform operation
3. Call `_write_todo(modified_tasks)` → persist

#### `cmd_show(tasks: list[dict]) -> None`
- If `tasks` is None (file missing) → create empty TODO.md via `_write_todo([])`, print "No tasks"
- If `tasks` is empty → print "No tasks"
- Otherwise → print each task as `"{id}. [{'x' if done else ' '}] {text}"` (CLI-friendly format, one per line)

#### `cmd_add(tasks: list[dict], text: str) -> None`
- If `tasks` is None → tasks = [] (will create file)
- Compute next ID: `max(t['id'] for t in tasks) + 1` if tasks else `1`
- Append `{"id": next_id, "done": False, "text": text}`
- Print confirmation: `"Added task {id}: {text}"`

#### `cmd_done(tasks: list[dict], task_id: int) -> None`
- If `tasks` is None or empty → print "Task {id} not found", return
- Find task by matching `t["id"] == task_id`
- If not found → print "Task {id} not found"
- If found and already done → still mark done (idempotent), print `"Task {id} marked as done"` (or "Task {id} is already done" — either is fine, keeping it simple)
- Set `t["done"] = True`
- Print `"Task {id} marked as done"`

#### `cmd_rm(tasks: list[dict], task_id: int) -> None`
- If `tasks` is None or empty → print "Task {id} not found", return
- Find task index by matching `t["id"] == task_id`
- If not found → print "Task {id} not found"
- Remove task from list
- All other task IDs remain unchanged (no re-indexing)
- Print `"Removed task {id}"`

#### `cmd_clear(tasks: list[dict]) -> None`
- If `tasks` is None or empty → print "No completed tasks to clear", return
- Count done tasks before filtering
- Retain only tasks where `done == False`
- Print `"Cleared {count} completed task(s)"`

---

## 7. Edge Cases & Error Handling

| Scenario | Behavior |
|---|---|
| `TODO.md` doesn't exist | Auto-create with header on first `--add`; print "No tasks" for `--show` |
| `TODO.md` has no `# Todo` header | Treat as empty → print "No tasks" |
| `TODO.md` is empty | Treat as empty → print "No tasks" |
| `TODO.md` has only header, no tasks | No tasks → print "No tasks" |
| `--done` with non-existent ID | Print "Task {id} not found" |
| `--rm` with non-existent ID | Print "Task {id} not found" |
| `--clear` when no tasks are done | Print "No completed tasks to clear" |
| Duplicate description text | Allowed — each add gets a new unique ID |
| Deleted task IDs are never reused | Next add uses `max + 1` |
| PowerShell `__init__.py` conflict | Not applicable (no package) |
| I/O permission error | Print error + `sys.exit(1)` |
| `--done` with non-integer ID | argparse rejects it via `type=int` |
| `--rm` with non-integer ID | argparse rejects it via `type=int` |
| Task IDs can be any positive int | Handled — `--done` and `--rm` both use `type=int` |
| `--add ""` (empty string) | Allowed — argparse passes through. Could validate at the app level if desired. |

---

## 8. Main Entry Point

```python
def main() -> None:
    """Parse CLI args and dispatch to the appropriate command."""
    parser = argparse.ArgumentParser(
        description="Markdown-based to-do tracker. Tasks stored in TODO.md."
    )
    parser.add_argument("--show", action="store_true", help="Show all tasks")
    parser.add_argument("--add", type=str, help="Add a new task with the given description")
    parser.add_argument("--done", type=int, help="Mark a task as completed by its ID")
    parser.add_argument("--rm", type=int, help="Remove a task by its ID")
    parser.add_argument("--clear", action="store_true", help="Remove all completed tasks")
    args = parser.parse_args()
    # ... dispatch with priority ordering ...

if __name__ == "__main__":
    main()
```

---

## 9. Implementation Order

| Step | Description | Est. |
|---|---|---|
| 1 | Create `todo.py` with shebang, docstring, imports (`argparse`, `re`, `pathlib`) | 2 min |
| 2 | Implement `TODO_PATH`, `_parse_tasks()`, `_render_tasks()` | 5 min |
| 3 | Implement `_read_todo()` and `_write_todo()` | 5 min |
| 4 | Implement `cmd_show()` with all edge cases | 3 min |
| 5 | Implement `cmd_add()` with auto-increment ID logic | 3 min |
| 6 | Implement `cmd_done()` with lookup-by-ID | 3 min |
| 7 | Implement `cmd_rm()` with lookup-by-ID | 3 min |
| 8 | Implement `cmd_clear()` with filter | 3 min |
| 9 | Wire up `main()` with CLI arg parsing and dispatch | 5 min |
| 10 | Test each command manually: add, show, done, rm, clear | 10 min |
| 11 | Test edge cases: missing file, invalid ID, empty file, no header | 5 min |
| **Total** | | **~47 min** |

---

## 10. Files Modified

| File | Action |
|---|---|
| `todo.py` | **Create** — the new CLI tool |
| `TODO.md` | **Create** — task storage (auto-generated on first use) |
| `specs/46-spec/spec.md` | **Create** — this document |

No existing files are modified. `greeting.py` and `README.md` are untouched.

---

## 11. Out of Scope (for this issue)

- Colorized / ANSI terminal output
- Task due dates, priorities, or categories
- Editing existing task text
- Reordering tasks
- Sorting tasks (by status, date, etc.)
- Multiple to-do files or `--file` flag
- JSON/YAML export
- Task persistence across renames (IDs are stable within a session of edits but could break if the file is hand-edited — by design)
