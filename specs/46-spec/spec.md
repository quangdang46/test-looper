# Spec: Markdown-based To-Do Tracker (`todo.py`)

**Issue:** [#46](https://github.com/quangdang46/test-looper/issues/46)  
**Status:** Draft  
**Date:** 2026-06-27

---

## 1. Overview

Build a zero-dependency CLI tool `todo.py` that stores a simple task list in a markdown file (`TODO.md`). Tasks are rendered as checkboxes (`- [ ]` / `- [x]`) with auto-incrementing integer IDs. The tool must handle all CRUD operations against the file on disk using only the Python standard library.

---

## 2. Requirements Recap

### Commands (CLI interface via `argparse`)

| Flag          | Argument      | Description                                    |
|---------------|---------------|------------------------------------------------|
| `--show`      | *(none)*      | Print all tasks grouped by status              |
| `--add`       | `<text>`      | Append a new task                              |
| `--done`      | `<task-id>`   | Mark a task as completed (`- [ ]` → `- [x]`)   |
| `--rm`        | `<task-id>`   | Delete a task entirely from the file           |
| `--clear`     | *(none)*      | Remove all completed tasks                     |

### File format

```markdown
# Todo

- [ ] 1. buy milk
- [ ] 2. call mom
- [x] 3. finish homework
```

### Edge cases (from issue)

Handled explicitly — see §4 Edge Cases.

---

## 3. Design Decisions

### 3.1 Single file, stdlib only

`todo.py` is the only source file. Dependencies:
- `argparse` — CLI argument parsing
- `re` — regex for pattern-matching task lines
- `pathlib` — cross-platform file path handling
- `sys` — exit codes

No `pip install` or external packages.

### 3.2 Task representation

Each task line follows a strict regex pattern:

```
^-\s+\[([ x])\]\s+(\d+)\.\s+(.+)$
```

Captures:
1. **Status character** — `" "` (pending) or `"x"` (done)
2. **Task ID** — integer; auto-incrementing, never reused after deletion
3. **Description** — the rest of the line

Internally each task is a `dataclass` (or a simple NamedTuple) with `id: int`, `description: str`, `done: bool`.

### 3.3 File lifecycle

| Scenario                | Behavior                                   |
|-------------------------|--------------------------------------------|
| `TODO.md` missing       | Created automatically with the `# Todo` header on the first `--add` |
| `TODO.md` exists, empty | Treated as empty — next `--add` writes header + task |
| `TODO.md` has no header | The `# Todo` header is prepended when first task is added |

### 3.4 ID management

- IDs are assigned sequentially starting at 1.
- Deleted tasks are physically removed from the file.
- New tasks receive `max(remaining IDs) + 1` — never reuse.
- When the file is empty (no tasks), next ID resets to `1`.

### 3.5 Output format

- `--show` with no tasks → prints "No tasks" to stdout.
- `--show` with tasks → prints all lines grouped as pending (visible) then done, each prefixed with status (`[ ]` or `[x]`) and ID.
- Success exit code `0`.
- Error exit code `1` for user-facing failures (invalid ID, file unreadable).

### 3.6 Module structure

```
todo.py
├── Task               # dataclass(id, description, done)
├── read_tasks(file)   # → list[Task]
├── write_tasks(file, tasks, next_id)  # serialises to markdown
├── cmd_show(tasks)
├── cmd_add(tasks, text)
├── cmd_done(tasks, id)
├── cmd_rm(tasks, id)
├── cmd_clear(tasks)
├── parse_args()       # argparse wrapper
└── main()             # dispatcher
```

---

## 4. Error Handling / Edge Cases

| Situation                           | Behaviour                                                     |
|-------------------------------------|---------------------------------------------------------------|
| Empty file / no `# Todo` header     | Return empty task list; `--add` creates header automatically   |
| `--done` / `--rm` with nonexistent id | Print `"Task <id> not found"` to stderr, exit code 1         |
| `--done` on already-done task       | No-op (already `[x]`), exit 0                                  |
| `--rm` deletes last task            | File still contains header; next add resets id to 1            |
| Duplicate description               | Allowed — each `--add` creates a new task with a new id        |
| File unreadable (permissions)        | Print error to stderr, exit 1                                  |
| `--add` with empty string           | Treated as a valid task with description ""                    |
| `--clear` on empty list             | No-op, exit 0                                                  |
| Invalid id format (non-integer)     | Caught by argparse `type=int` → usage error                    |
| Corrupt lines in file               | Lines not matching the pattern are preserved verbatim          |
| Multiple flags at once              | Only one action flag is supported per invocation (argparse mutually exclusive group) |

---

## 5. Implementation Steps

1. **Create skeleton** — `todo.py` with shebang, docstring, `if __name__ == "__main__": main()`.
2. **Define `Task`** — a simple class or `NamedTuple` for `id`, `description`, `done`.
3. **Implement file I/O**
   - `TODO_MD = Path("TODO.md")` as a module constant.
   - `read_tasks()` — parse file, return `list[Task]` and `next_id` (max ID + 1).
   - `write_tasks(tasks)` — serialize header + task lines.
4. **Implement commands** — six simple functions, each taking the task list.
5. **Wire CLI** — `argparse` with a mutually exclusive group for action flags.
6. **Test manually** — run each command, verify file state, check edge cases.
7. **Commit** — `git add todo.py specs/46-spec/spec.md && git commit`.
