# Implementation Plan: Markdown-based To-Do Tracker (`todo.py`)

**Issue:** [#46 — build a markdown-based to-do tracker](https://github.com/quangdang46/test-looper/issues/46)

## Overview

Create a single-file CLI tool `todo.py` that manages a simple to-do list stored in a `TODO.md` file. The tool uses only Python stdlib (`argparse`, `re`, `pathlib`) and reads/writes a markdown-formatted checklist file.

## Design

### File path

`TODO.md` lives in the current working directory.

### Task format in `TODO.md`

```markdown
# Todo

- [ ] 1. buy milk
- [ ] 2. call mom
- [x] 3. finish homework
```

- Header: `# Todo` at the top of the file
- Each task is a list item: `- [ ] <id>. <description>` (pending) or `- [x] <id>. <description>` (done)
- Task IDs are integers, auto-incrementing from 1, never reused after deletion

### Program structure — `todo.py`

| Section | Description |
|---|---|
| `parse_args()` | Build `argparse` parser with `--show`, `--add`, `--done`, `--rm`, `--clear` |
| `ensure_file()` | Create `TODO.md` with `# Todo` header if missing |
| `read_tasks()` | Parse `TODO.md` into a list of `(id, description, done)` tuples. Returns empty list if file is empty or has no tasks. |
| `write_tasks(tasks)` | Serialize tasks back to `TODO.md` markdown |
| `cmd_show(tasks)` | Print all tasks; print "No tasks" if list is empty |
| `cmd_add(tasks, text)` | Append new task with next available id |
| `cmd_done(tasks, task_id)` | Mark task as completed (toggle `[ ]` → `[x]`) |
| `cmd_rm(tasks, task_id)` | Remove task entirely |
| `cmd_clear(tasks)` | Remove all completed tasks |
| `find_task(tasks, task_id)` | Helper: return task index or `None` |
| `next_id(tasks)` | Helper: `max(existing ids) + 1`, or `1` if no tasks |
| `main()` | Dispatch to sub-command based on parsed args |

### Argument interface

```
python todo.py --show          # show all tasks
python todo.py --add "buy milk" # add a new task
python todo.py --done 1         # mark task 1 as done
python todo.py --rm 2           # remove task 2
python todo.py --clear          # remove all done tasks
```


### CLI flags are mutually exclusive

Only one action per invocation (enforced by `add_mutually_exclusive_group` in argparse).

## Error Handling

| Scenario | Behavior |
|---|---|
| `TODO.md` doesn't exist | Created automatically with `# Todo` header on first write operation |
| `TODO.md` exists but is empty or has no `# Todo` header | Treated as empty (no tasks) — header is added on first write |
| Invalid/missing task id for `--done` or `--rm` | Print `"Task <id> not found"` to stderr, exit with code 1 |
| No tasks and `--show` | Print `"No tasks"` to stdout, exit with code 0 |
| `--add` with empty text | Print error to stderr, exit with code 1 |
| `--clear` with no done tasks | Print `"No completed tasks to clear"` to stdout, exit with code 0 |
| File I/O failure (permission, disk full) | Print error to stderr, exit with code 1 |

## Edge Cases

- **Empty TODO.md:** If the file exists but has no `# Todo` header, treat as empty. Re-initialize on write (add the header).
- **Missing file:** Create on write operations (`--add`, `--done`, `--rm`, `--clear`). For `--show`, create the file with header and print "No tasks".
- **Duplicate text on `--add`:** Allowed — each call creates a new task with a unique id.
- **Id reuse:** Never. Deleted task ids are gone forever. `next_id` = `max(remaining ids) + 1`.
- **File with only a header but no tasks:** Show prints "No tasks". `--add` appends normally.
- **Concurrent edits:** Not handled — single-user tool. If the file is modified externally between read and write, changes may be overwritten.

## Implementation Order

1. Create `todo.py` with shebang, docstring, imports
2. Implement `parse_args()` with mutually exclusive group
3. Implement `ensure_file()`, `read_tasks()`, `write_tasks()`
4. Implement `find_task()` and `next_id()` helpers
5. Implement `cmd_show()`, `cmd_add()`, `cmd_done()`, `cmd_rm()`, `cmd_clear()`
6. Wire `main()` dispatch
7. Add `if __name__ == "__main__": main()` block
8. Test each operation manually

## Testing Checklist

- [ ] `python todo.py --show` on fresh repo → "No tasks", creates `TODO.md`
- [ ] `python todo.py --add "buy milk"` → task 1 appears
- [ ] `python todo.py --add "buy milk"` → task 2 appears (duplicate ok)
- [ ] `python todo.py --done 1` → first task marked `[x]`
- [ ] `python todo.py --done 99` → "Task 99 not found"
- [ ] `python todo.py --rm 2` → task 2 removed, task 1 stays
- [ ] `python todo.py --clear` → removes done tasks, keeps pending
- [ ] `python todo.py` (no args) → prints usage
- [ ] `python todo.py --add ""` → error on empty text
