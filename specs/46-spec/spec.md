# Spec: Markdown-based To-Do Tracker (`todo.py`)

**Issue:** #46  
**Status:** Draft  
**Author:** quangdang46  

## 1. Problem Statement

Build a zero-dependency CLI tool `todo.py` that manages a to-do list persisted in a markdown file (`TODO.md`). The tool reads and writes the file using standard markdown checkbox syntax (`- [ ]` / `- [x]`) and provides subcommands for listing, adding, completing, deleting, and housekeeping tasks.

## 2. Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Persistence file | `TODO.md` in CWD | Simple, human-readable, version-control-friendly |
| Task ID scheme | Auto-incrementing integer, never reused | Matches issue spec; deleted IDs are gone forever |
| ID source | Max existing ID + 1 | No separate counter file needed |
| CLI framework | `argparse` (stdlib) | Matches project convention; `greeting.py` uses `sys.argv` but argparse is cleaner for subcommands |
| File format | Flat list under `# Todo` header | Simple regex parsing, no YAML/JSON dependency |
| Python version | 3.10+ (std lib only) | Modern enough for `pathlib` and `argparse` |

## 3. File Format

`TODO.md` structure:

```markdown
# Todo

- [ ] 1. buy milk
- [ ] 2. call mom
- [x] 3. finish homework
```

- Each task line matches regex: `^- \[([ x])\] (\d+)\. (.+)$`
- Tasks are numbered inside the same file; headless lines are ignored
- The `# Todo` header at line 1 is optional — the file may also start with tasks immediately
- Empty files or files with no task lines → "No tasks"

## 4. CLI Interface

```text
usage: todo.py [-h] [--show] [--add ADD] [--done DONE] [--rm RM] [--clear]

Markdown-based to-do tracker.

optional arguments:
  -h, --help   show this help message and exit
  --show       Display all tasks
  --add ADD    Add a new task
  --done DONE  Mark task <id> as completed
  --rm RM      Remove task <id> permanently
  --clear      Remove all completed tasks
```

### Precedence (when multiple flags are given)

Only **one** action runs per invocation, in this priority order:

1. `--add`
2. `--done`
3. `--rm`
4. `--clear`
5. `--show` (default if no action flag given)

This avoids surprising side effects from combining flags.

## 5. Behaviour by Operation

### 5.1 `--show` (or no flags)

1. Read `TODO.md`
2. If file is missing OR has no `- [ ]` / `- [x]` lines → print `"No tasks"`
3. Otherwise print all task lines with their current checkbox state

### 5.2 `--add "text"`

1. Read `TODO.md` (create with `# Todo` header if missing)
2. Compute `next_id = max(existing_ids, default=0) + 1`
3. Append `- [ ] <next_id>. <text>` to file
4. Print confirmation (optional, not required by spec)

### 5.3 `--done <id>`

1. Read `TODO.md`
2. Locate line `- [ ] <id>.` — replace `[ ]` with `[x]`
3. If no matching line found → print `"Task <id> not found"` and exit with code 1
4. Write updated content back to file

### 5.4 `--rm <id>`

1. Read `TODO.md`
2. Remove the line `- [ ] <id>.` or `- [x] <id>.` entirely
3. If no matching line found → print `"Task <id> not found"` and exit with code 1
4. Write remaining content back to file

### 5.5 `--clear`

1. Read `TODO.md`
2. Remove all lines matching `- [x] <id>.` (completed tasks)
3. Write remaining content back

## 6. Edge Cases

| Scenario | Expected behaviour |
|----------|--------------------|
| `TODO.md` does not exist | Created with `# Todo` header on first `--add`; otherwise treated as empty |
| `TODO.md` is empty | Treated as "no tasks" — prints `"No tasks"` |
| `TODO.md` has content but no `- [ ]` lines | Prints `"No tasks"` |
| Invalid `--done` / `--rm` id | Prints `"Task <id> not found"`, exits code 1 |
| `--done` on already-done task | Works (idempotent) — keeps `[x]` |
| Duplicate task text | Allowed — same text produces a new task with a new id |
| Task id reuse after delete | Never — deleted IDs are removed from the file; next ID is always `max + 1` |
| Extra whitespace in file | Tolerated — blank lines are preserved, non-task lines ignored |
| `--done` / `--rm` with non-integer arg | argparse handles type coercion error |
| File is not writable | Catch `PermissionError`, print descriptive message, exit code 1 |

## 7. Error Handling

- **File not found during read**: treated as "no tasks" (not an error)
- **File not writable**: print `"Error: cannot write TODO.md — <reason>"`, exit code 1
- **Unexpected I/O error**: print `"Error: <reason>"`, exit code 1
- **Invalid arguments**: argparse generates a clear usage message

## 8. Implementation Plan

### File: `todo.py`

```
todo.py
├── Imports: argparse, re, pathlib, sys
├── TODO_FILENAME = "TODO.md"
├── --
├── read_tasks(path) -> list[dict]
│   Returns list of {line, id, done, text, raw}
│   Replaces '\n' before returning
├── write_tasks(path, lines)
│   Write list of strings back to file
├── cmd_show(path)
├── cmd_add(path, text)
├── cmd_done(path, task_id)
├── cmd_rm(path, task_id)
├── cmd_clear(path)
├── create_parser() -> ArgumentParser
├── main()
└── if __name__ == "__main__"
```

### 8.1 Helper: `read_tasks(path) -> list[dict]`

1. Try to read file; if `FileNotFoundError` → return `[]`
2. Parse each line with regex `^-\s+\[([ x])\]\s+(\d+)\.\s+(.*)$`
3. Return list of dicts `{"line": int, "id": int, "done": bool, "text": str, "raw": str}`

### 8.2 Helper: `write_tasks(path, lines: list[str])`

1. Join lines with `\n`, write to path
2. Catch `PermissionError` / `OSError` → print error, exit

### 8.3 `cmd_show`

- Call `read_tasks()`; if empty → print "No tasks"
- Else print each task with `[ ]`/`[x]` prefix and id

### 8.4 `cmd_add`

- Call `read_tasks()` to discover existing IDs (even if file has no header)
- `next_id = max([t["id"] for t in tasks], default=0) + 1`
- Append the new task line, preserving any `# Todo` header or non-task content

### 8.5 `cmd_done`

- `tasks = read_tasks()`; find matching id
- If not found → print "Task <id> not found"; `sys.exit(1)`
- Replace `[ ]` with `[x]` on matching line; write back

### 8.6 `cmd_rm`

- `tasks = read_tasks()`; find matching id
- If not found → print "Task <id> not found"; `sys.exit(1)`
- Remove that line; write back

### 8.7 `cmd_clear`

- `tasks = read_tasks()`; filter out done tasks
- Reconstruct file lines (preserving header/non-task lines); write back

## 9. Testing Scenarios

| # | Scenario | Command | Expected output |
|---|----------|---------|-----------------|
| 1 | No file exists, `--show` | `python todo.py --show` | "No tasks" |
| 2 | Add first task | `python todo.py --add "buy milk"` | File created with `- [ ] 1. buy milk` |
| 3 | Add second task | `python todo.py --add "call mom"` | `- [ ] 2. call mom` appended |
| 4 | Show tasks | `python todo.py --show` | Both tasks printed |
| 5 | Mark done | `python todo.py --done 1` | First task becomes `[x]` |
| 6 | Invalid done id | `python todo.py --done 99` | "Task 99 not found" |
| 7 | Remove | `python todo.py --rm 2` | Task 2 line removed |
| 8 | Clear done | `python todo.py --clear` | Done tasks removed |
| 9 | Empty file → show | `python todo.py --show` | "No tasks" |
| 10 | Missing file → show | `python todo.py --show` | "No tasks" |

## 10. Code Style

Follow conventions from `greeting.py`:
- `#!/usr/bin/env python3` shebang
- Module-level docstring
- Type annotations on function signatures
- `main()` function with `if __name__ == "__main__":`
- Consistent 4-space indentation

## 11. Deliverables

- `todo.py` — single-file implementation
- `TODO.md` — created on first use (not committed)
- `specs/46-spec/spec.md` — this document

No external dependencies beyond Python stdlib.
