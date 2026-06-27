# Spec: Markdown-based To-Do Tracker (`todo.py`)

**Issue:** #46 — Build a markdown-based to-do tracker  
**File:** `todo.py` (single file, no external dependencies)  
**Storage:** `TODO.md` in the working directory

---

## 1. Overview

A CLI tool that manages a simple to-do list stored entirely in a markdown file (`TODO.md`). Tasks are rendered as markdown checkboxes (`- [ ]` pending, `- [x]` done) with auto-incrementing integer IDs. The tool uses only Python stdlib (`argparse`, `re`, `pathlib`).

---

## 2. CLI Interface

| Command | Example | Behaviour |
|---|---|---|
| (no flags) | `python todo.py` | Show all tasks (same as `--show`) |
| `--show` | `python todo.py --show` | List pending + completed tasks with their IDs |
| `--add <text>` | `python todo.py --add "buy milk"` | Append a new pending task |
| `--done <id>` | `python todo.py --done 2` | Mark task `<id>` as completed (`- [x]`) |
| `--rm <id>` | `python todo.py --rm 1` | Remove task `<id>` from the file entirely |
| `--clear` | `python todo.py --clear` | Remove all completed tasks |

Only one action flag may be used per invocation. If none is given, default to `--show`.

---

## 3. `TODO.md` File Format

```markdown
# Todo

- [ ] 1. buy milk
- [ ] 2. call mom
- [x] 3. finish homework
```

- **Header:** The first line is `# Todo` (with trailing newline).
- **Tasks:** One task per line as a markdown list item.
  - Pending: `- [ ] <id>. <description>`
  - Done:   `- [x] <id>. <description>`
- IDs are integers, strictly auto-incrementing from 1.
- Deleted IDs are **never reused** — deletion removes the line and the remaining IDs stay intact.
- The file always ends with a trailing newline.

---

## 4. Internal Design

### 4.1 Data structures

```python
@dataclass
class Task:
    task_id: int
    description: str
    done: bool
```

### 4.2 Functions

| Function | Signature | Purpose |
|---|---|---|
| `load_tasks(path)` | `(Path) -> list[Task]` | Parse `TODO.md`, return ordered list of tasks. Returns `[]` if file missing (don't error). |
| `save_tasks(path, tasks)` | `(Path, list[Task]) -> None` | Serialize tasks back to `TODO.md` with `# Todo` header. |
| `next_task_id(tasks)` | `(list[Task]) -> int` | Largest existing ID + 1 (or `1` if empty). |
| `show_tasks(tasks)` | `(list[Task]) -> str` | Format tasks for display; returns a string. |
| `add_task(tasks, text)` | `(list[Task], str) -> list[Task]` | Append a new pending task with `next_task_id`. |
| `mark_done(tasks, task_id)` | `(list[Task], int) -> list[Task]` | Set `done=True`. Raises `ValueError` on bad ID. |
| `remove_task(tasks, task_id)` | `(list[Task], int) -> list[Task]` | Drop task from list. Raises `ValueError` on bad ID. |
| `clear_done(tasks)` | `(list[Task]) -> list[Task]` | Filter out all done tasks. |
| `main()` | `() -> None` | Parse args, dispatch to action, print output. |

### 4.3 Parsing regex

Each task line: `^- \[( |x)\] (\d+)\.\s*(.+)$`

Match groups: `state` (` ` or `x`), `id`, `description`.

---

## 5. Edge Cases & Error Handling

| Scenario | Behaviour |
|---|---|
| `TODO.md` does not exist | `load_tasks` returns `[]`; `save_tasks` creates the file with header. |
| `TODO.md` is empty | `load_tasks` returns `[]`. |
| `TODO.md` exists but has no `# Todo` header | Accept gracefully — treat missing-header file as empty (header not required for parse). If no lines match the task regex, return `[]`. |
| `--done <id>` with non-existent ID | Print `"Task <id> not found"` to stderr, exit code 1. |
| `--rm <id>` with non-existent ID | Print `"Task <id> not found"` to stderr, exit code 1. |
| `--add` with empty string | Treat as valid task with empty description (`- [ ] N.`). |
| `--done` / `--rm` with non-integer | `argparse` type=int handles this — exits with usage error. |
| No tasks to show | Print `"No tasks"`. |
| `--clear` with no done tasks | No-op (file unchanged). |
| File I/O error (`PermissionError`, etc.) | Catch, print error message to stderr, exit code 1. |
| Multiple action flags (`--add` + `--done`) | Print error and exit code 1. |
| `--done` on already-done task | Allowed (idempotent) — no error, no change. |

---

## 6. Display Output Format

### With tasks:
```
Pending:
  - [ ] 1. buy milk
  - [ ] 2. call mom

Done:
  - [x] 3. finish homework
```

### Without tasks:
```
No tasks
```

---

## 7. `__main__` Block

```python
if __name__ == "__main__":
    main()
```

---

## 8. Implementation Steps (in order)

1. **Create `todo.py`** — scaffold with functions stubs, `argparse` setup, `__main__` block.
2. **Implement `load_tasks` / `save_tasks`** — regular expression parsing, `Path` I/O.
3. **Implement `next_task_id`** — linear scan for max ID.
4. **Implement `show_tasks`** — format pending/done sections.
5. **Implement `add_task` / `mark_done` / `remove_task` / `clear_done`** — list operations.
6. **Implement `main()` dispatch** — wire CLI flags to action functions, error handling for invalid IDs, multiple flags, I/O failures.
7. **Test manually** — run the script against all commands on a fresh `TODO.md`.
8. **Commit** — `todo.py` + `specs/46-spec/spec.md` on a branch for issue #46.
