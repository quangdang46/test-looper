# Spec: Markdown-based To-Do Tracker (`todo.py`)

> Issue [#46](https://github.com/quangdang46/test-looper/issues/46)

## 1. Overview

A single-file CLI (`todo.py`) that persists tasks in a markdown file (`TODO.md`)
using GitHub-Flavored Markdown checklist syntax.

**No external dependencies** — only Python stdlib (`argparse`, `re`, `pathlib`).

## 2. Markdown storage format

```
# Todo

- [ ] 1. buy milk
- [ ] 2. call mom
- [x] 3. finish homework
```

- The file must begin with a `# Todo` header.
- Each task is one list item with a checkbox and an id.
- Ids are integers, auto-incremented from `1`, and **never reused** after deletion.
- Deleted tasks are removed from the file entirely so remaining ids stay the same.

## 3. CLI interface

| Command | Example | Behaviour |
|---|---|---|
| `python todo.py` (no args) | — | Alias for `--show` |
| `python todo.py --show` | | Print all tasks. Empty/absent file → `"No tasks"` |
| `python todo.py --add "buy milk"` | | Append a new task with the next available id. Duplicate text is OK. |
| `python todo.py --done <task-id>` | `--done 2` | Change `- [ ]` → `- [x]` for that id. |
| `python todo.py --rm <task-id>` | `--rm 3` | Remove that line entirely. |
| `python todo.py --clear` | | Remove all `- [x]` lines (keep pending tasks). |

### Error messages

- Invalid task id → `"Task <id> not found"` to stderr, exit code `1`.
- File does not exist (and `--show` or `--done` / `--rm` / `--clear`) → `"No tasks"` to stdout, exit code `0`.
- File I/O errors → print message to stderr, exit code `1`.

## 4. Module structure (single file)

```
todo.py
├── TASK_RE       = re.compile(r"^- \[([ x])\] (\d+)\. (.+)$")
├── HEADER        = "# Todo"
│
├── find_next_id(lines: list[str]) -> int
├── parse_tasks(lines: list[str]) -> list[dict]
├── read_todo(path: Path) -> list[str]
├── write_todo(path: Path, lines: list[str]) -> None
├── cmd_show(path: Path) -> bool
├── cmd_add(path: Path, text: str) -> bool
├── cmd_done(path: Path, task_id: int) -> bool
├── cmd_rm(path: Path, task_id: int) -> bool
├── cmd_clear(path: Path) -> bool
├── build_parser() -> ArgumentParser
├── main() -> None
└── __main__ block
```

### Module‑level helpers

| Helper | Purpose |
|---|---|
| `TASK_RE` | `r"^- \[([ x])\] (\d+)\. (.+)$"` — captures status, id, description |
| `HEADER` | `"# Todo"` — the required first line |

### Function contracts

| Function | Signature | Behaviour |
|---|---|---|
| `find_next_id` | `(lines: list[str]) -> int` | Scan lines; return max id + 1, or 1 if none exist. Guarantees no reuse. |
| `parse_tasks` | `(lines: list[str]) -> list[dict]` | Return `[{id, status, text}]` for every line matching `TASK_RE`. |
| `read_todo` | `(path: Path) -> list[str]` | Read file; return lines. **Missing file → return empty list** (caller decides behaviour). |
| `write_todo` | `(path: Path, lines: list[str]) -> None` | Write lines to disk. |
| `cmd_show` | `(path: Path) -> bool` | Print tasks or `"No tasks"`. Return `True` on success. |
| `cmd_add` | `(path: Path, text: str) -> bool` | Ensure header exists, compute next id, append task line. |
| `cmd_done` | `(path: Path, task_id: int) -> bool` | Replace `[ ]` → `[x]`. Print `"Task <id> not found"` on miss. |
| `cmd_rm` | `(path: Path, task_id: int) -> bool` | Remove matching line. Print `"Task <id> not found"` on miss. |
| `cmd_clear` | `(path: Path) -> bool` | Remove all lines matching `- [x] ...`. |
| `build_parser` | `() -> ArgumentParser` | Configure argparse with all flags. |
| `main` | `() -> None` | Parse args, delegate to cmd_*, handle errors. |

## 5. Edge cases

| Scenario | Behaviour |
|---|---|
| `TODO.md` missing & `--show` | Print `"No tasks"` |
| `TODO.md` missing & `--add` | Create the file with `# Todo` header, then insert the task |
| `TODO.md` missing & `--done`/`--rm` | Print `"Task <id> not found"` |
| `TODO.md` missing & `--clear` | No-op (print nothing, exit 0) |
| `TODO.md` missing header | Still try to work — re-add `# Todo` as first line if needed |
| `--done` with non‑existent id | `"Task <id> not found"` to stderr, exit 1 |
| `--rm` with non‑existent id | `"Task <id> not found"` to stderr, exit 1 |
| `--add` with duplicate text | Accepted — same text, new id |
| Ids after deletion | Never reused; `find_next_id` uses the max remaining id + 1 |
| `--done` on already‑done task | No-op (idempotent — stays `[x]`) |
| Concurrent writes | Not handled (out of scope: single‑user tool) |
| File I/O error (permissions, disk) | Print error to stderr, exit 1 |

## 6. Implementation steps

1. **Create `todo.py`** — single file in repo root.
2. **Define `TASK_RE` and `HEADER`** module constants.
3. **Implement `find_next_id`** — scan all lines, match `TASK_RE`, return max_id + 1 (or 1).
4. **Implement `parse_tasks`** — iterate lines, match `TASK_RE`, yield dicts.
5. **Implement `read_todo` / `write_todo`** — thin `Path` wrappers.
6. **Implement `cmd_show`** — call `parse_tasks`, print table or `"No tasks"`.
7. **Implement `cmd_add`** — ensure header, compute id, append `"- [ ] <id>. <text>"`.
8. **Implement `cmd_done`** — find line by id, replace `[ ]` with `[x]`.
9. **Implement `cmd_rm`** — find line by id, remove it entirely.
10. **Implement `cmd_clear`** — filter out lines matching `- [x] ...`.
11. **Implement `build_parser`** — argparse with all + `--show` as default action when no args.
12. **Implement `main`** — wire parser → cmd_*, handle `SystemExit`/`FileNotFoundError`.
13. **Add `__main__` block** and usage docstring.
