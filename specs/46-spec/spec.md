# Spec: Markdown-based To-Do Tracker

## Overview

A single-file CLI tool `todo.py` that manages a simple to-do list stored in `TODO.md`.
Uses only Python stdlib (`argparse`, `re`, `pathlib`).

## File Format

`TODO.md` uses GitHub-flavored markdown checkboxes with numbered items:

```markdown
# Todo

- [ ] 1. buy milk
- [x] 2. call mom
- [ ] 3. finish homework
<!-- last_id: 3 -->
```

A hidden HTML comment `<!-- last_id: N -->` tracks the highest ID ever assigned so that
deleted IDs are never reused (auto-increment always starts from max(last_id, max(existing ids)) + 1).

## Data Model

- **Task**: `{id: int, text: str, done: bool}`
- **TodoFile**: `{header: list[str], tasks: list[Task], footer: list[str], last_id: int}`

## Architecture

```
read_todo() → TodoFile        Parse TODO.md → structured model
write_todo(TodoFile) → void   Write structured model → TODO.md
cmd_show()                    Print tasks grouped by status
cmd_add(text)                 Append new pending task
cmd_done(id)                  Mark task done
cmd_rm(id)                    Remove task entirely
cmd_clear()                   Remove all done tasks
```

## Parser Logic

1. Scan lines for `# Todo` header
2. After header, match lines against `^- \[([ x])\] (\d+)\. (.+)$`
3. Content before header → header, matches → tasks, content after last match → footer
4. Scan footer for `<!-- last_id: N -->` comment

## Writer Logic

1. Write header lines verbatim
2. Format each task as `- [x] N. text\n` or `- [ ] N. text\n`
3. Write footer lines (strip stale `<!-- last_id: -->` lines)
4. Append fresh `<!-- last_id: N -->\n`

## Edge Cases Handled

| Case | Behavior |
|------|----------|
| Missing TODO.md | Create with `# Todo\n\n` header |
| File exists, no `# Todo` | Treat as empty → "No tasks" |
| Invalid task ID | stderr: "Task <id> not found", exit 1 |
| Empty task text on --add | stderr: "Error: task text cannot be empty", exit 1 |
| Duplicate text on add | OK (same text, new auto-incremented ID) |
| Deleted IDs | Removed from file; never reused |
| File I/O error | stderr with OSError message, exit 1 |

## CLI Interface

```
python todo.py              Show all tasks (default, same as --show)
python todo.py --show       Show all tasks
python todo.py --add TEXT   Add a new task
python todo.py --done ID    Mark task as completed
python todo.py --rm ID      Remove a task
python todo.py --clear      Remove all completed tasks
```

All flags are mutually exclusive. Default action (no flag) = show.

## Output Format (--show)

```
Pending:
  1. buy milk
  3. finish homework

Done:
  2. call mom
```
