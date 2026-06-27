# Spec: Markdown-based To-Do Tracker

Issue: [#46 — build a markdown-based to-do tracker](https://github.com/quangdang46/test-looper/issues/46)

## Overview

Create `todo.py`, a zero-dependency CLI tool that manages a simple to-do list stored in a markdown file (`TODO.md`). Tasks are persisted as Markdown checkbox list items with sequential integer IDs.

## Data Format (`TODO.md`)

```
# Todo

- [ ] 1. buy milk
- [ ] 2. call mom
- [x] 3. finish homework
```

- File begins with a top-level `# Todo` heading (required for the file to be considered "valid").
- Each task is a Markdown checkbox list item: `- [ ] <id>. <description>` (pending) or `- [x] <id>. <description>` (done).
- Task IDs are positive integers, auto-incremented from 1, and **never reused** (deleting a task does not release its ID for future use).
- A blank line between the heading and the task list is allowed but not required.

## CLI Interface

All arguments use long-form flags via `argparse`. Default behavior when no task-modifying flag is given is to **show** tasks.

| Command | Behavior |
|---|---|
| `python todo.py [--show]` | List all tasks grouped by status |
| `python todo.py --add "text"` | Append a new pending task |
| `python todo.py --done <id>` | Mark a task as completed |
| `python todo.py --rm <id>` | Remove a task entirely |
| `python todo.py --clear` | Delete all completed tasks |

### `--show` (default)
- Parse `TODO.md` and print pending and completed tasks separately.
- If the file does not exist, create it with the `# Todo` header and print "No tasks".
- If the file exists but has no `# Todo` heading or no task items, print "No tasks".
- Otherwise, print a summary:
  ```
  Pending:
  1. buy milk
  2. call mom

  Done:
  3. finish homework
  ```

### `--add "text"`
- Parse existing tasks to determine the next available ID (max existing ID + 1; 1 if no tasks exist).
- Append `- [ ] <next_id>. <description>` after the last task line.
- For a missing file, create it with the header and add the task.
- Print confirmation: `Added task <id>: <description>`.

### `--done <id>`
- Locate the task line whose id matches `<id>`.
- Replace `- [ ]` with `- [x]`.
- If the task is already done, treat as a no-op (still print success).
- Print confirmation: `Task <id> completed`.
- If `<id>` not found, print `Task <id> not found` and exit with code 1.

### `--rm <id>`
- Remove the entire task line matching `<id>` (including the trailing newline).
- Other tasks and their IDs are untouched.
- Print confirmation: `Removed task <id>`.
- If `<id>` not found, print `Task <id> not found` and exit with code 1.

### `--clear`
- Remove all lines whose checkbox is `[x]` (completed).
- Print `Cleared <count> completed task(s).` or `No completed tasks to clear.` if none.
- If the file has no `# Todo` heading or doesn't exist, print "No tasks."

## Error Handling

| Scenario | Behavior |
|---|---|
| File I/O error (permissions, disk full) | Print error message to stderr, exit with code 1 |
| `--done`/`--rm` with missing file | Create file with header, then print "Task <id> not found" |
| `--done`/`--rm` with non-existent id | Print "Task <id> not found", exit code 1 |
| `--add` with empty string | Print "Task description cannot be empty", exit code 1 |
| `--done`/`--rm` with non-integer id | argparse rejects via `type=int` |
| Conflicting flags (e.g. `--add` and `--done`) | argparse handles mutually exclusive group |

## Implementation Plan

### Step 1: Create `todo.py` scaffold

Create `todo.py` with:
- Module docstring with usage examples
- Shebang line
- `__main__` block calling `main()`

### Step 2: Implement file reading & parsing

Function `parse_todo(path: Path) -> Tuple[List[Dict], int]`:
- Read `TODO.md` if it exists
- Determine whether `# Todo` header is present
- Parse lines matching `- [ |x] <int>. <description>` into a list of task dicts `{id, description, done}`
- Return task list + next_id (max id + 1, or 1 if empty)

Function `ensure_header(content: str) -> str`:
- If content doesn't start with `# Todo`, prepend it (with a trailing newline).

### Step 3: Implement display (`--show`)

Function `show_tasks(tasks)`:
- Print pending tasks and done tasks in two sections.
- If no tasks, print "No tasks."

### Step 4: Implement add (`--add`)

Function `add_task(task_descs: str, path: Path)`:
- Parse file to find next_id.
- Append `- [ ] <next_id>. <description>` to file.
- Print confirmation.

### Step 5: Implement mark done (`--done`)

Function `mark_done(task_id: int, path: Path)`:
- Read file line by line, find the matching line.
- Replace `- [ ]` with `- [x]`.
- Write back.
- Print confirmation or error.

### Step 6: Implement remove (`--rm`)

Function `remove_task(task_id: int, path: Path)`:
- Read file, filter out the matching line.
- Write back.
- Print confirmation or error.

### Step 7: Implement clear (`--clear`)

Function `clear_done(path: Path)`:
- Read file, filter out all `- [x]` lines.
- Write back.
- Print count or "No completed tasks."

### Step 8: Wire up `main()` and argument parser

- Use `argparse` with mutually exclusive group for `--add`, `--done`, `--rm`, `--clear`.
- `--show` is default (store_true, mutually exclusive with others — or simply no-flag default).
- `TODO.md` path defaults to `Path("TODO.md")` in CWD.

### Step 9: Test edge cases

- Missing TODO.md
- Empty TODO.md (no heading)
- File with header but no tasks
- Invalid task IDs for `--done`/`--rm`
- Duplicate task descriptions
- Deleting a task then adding (ensures no ID reuse)
- Already-completed tasks targeted with `--done`

## File Location

- Script: `todo.py` at repository root
- Every invocation reads/writes `TODO.md` in the current working directory

## Dependencies

None (Python stdlib only: `argparse`, `re`, `pathlib`, `sys`)
