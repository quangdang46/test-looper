---
issue: 46
title: "feat: add a markdown-based to-do tracker (todo.py)"
status: draft
---

## Objective

Add a single-file CLI tool `todo.py` that manages a simple to-do list stored in a markdown file (`TODO.md`). Users can show, add, complete, delete, and clear tasks via command-line flags, using only the Python standard library. Tasks are persisted as checkboxes in a markdown list under a `# Todo` header, with auto-incrementing integer IDs that never reuse deleted IDs.

## Implementation Plan

1. **Create `todo.py`** at the repository root.
   - Add a `#!/usr/bin/env python3` shebang and `# -*- coding: utf-8 -*-` encoding declaration.
   - Include a module-level docstring with usage examples.
   - Define helper functions for each operation (see below), a `main()` entry point with `argparse`, and an `if __name__ == "__main__"` guard.

2. **Define the file-path constant and helper functions.**

   | Function | Purpose |
   |----------|---------|
   | `get_todo_path() -> Path` | Returns `Path("TODO.md")` relative to CWD. |
   | `ensure_file() -> None` | Create `TODO.md` with `# Todo\n\n` header if missing. |
   | `read_tasks() -> list[dict]` | Parse `TODO.md`, return list of `{id, text, done}` dicts. Raise `ValueError` if `# Todo` header is absent. |
   | `write_tasks(tasks: list[dict]) -> None` | Serialize tasks back to `TODO.md` under `# Todo` header. |
   | `show_tasks() -> bool` | Print tasks in order or "No tasks". Return `True` if tasks exist. |
   | `add_task(text: str) -> None` | Compute next ID (max existing + 1, or 1 if empty), append `- [ ] <id>. <text>` and write. |
   | `done_task(task_id: int) -> None` | Find task by integer ID, mark it done (`- [x]`) and write. Raise `LookupError` if not found. |
   | `remove_task(task_id: int) -> None` | Find task by integer ID, remove its line entirely and write. Raise `LookupError` if not found. |
   | `clear_done() -> None` | Remove all done tasks from the list and write. |

3. **Parsing logic for TODO.md**
   - Read the file line by line.
   - Locate the `# Todo` header line.
   - For each subsequent line matching the regex `^\s*-\s+\[([ x])\]\s+(\d+)\.\s+(.+)$`, extract: done flag (`''` or `'x'` → boolean), ID (integer), and text.
   - Stop at the first blank line or next heading after the task list (tasks are contiguous).
   - Preserve the header and surrounding blank lines.

4. **Set up `argparse` in `main()`.**
   ```
   usage: todo.py [-h] [--show] [--add TEXT] [--done ID] [--rm ID] [--clear]
   ```
   - `--show` (store_true): display tasks.
   - `--add TEXT` (str): add a new task.
   - `--done ID` (int): mark task as done.
   - `--rm ID` (int): delete a task.
   - `--clear` (store_true): remove all completed tasks.
   - If no flags given, default to `--show` (display tasks).
   - Mutual exclusion: `--add`, `--done`, `--rm`, `--clear` are logically exclusive. Use a simple if/elif chain rather than argparse mutual-exclusion groups (friendlier error messages).

5. **Error handling and edge cases.**
   - File missing on read → call `ensure_file()` then re-read.
   - `# Todo` header absent → print "No tasks" and exit 0.
   - Task ID not found → print "Task <id> not found" and exit 1.
   - File I/O errors (permissions, disk full) → print error to stderr and exit 1.
   - Non-numeric `--done`/`--rm` → argparse handles via `type=int`.

6. **Make `todo.py` executable** (`chmod +x todo.py`).

7. **Verify** the script against the acceptance criteria below, covering all edge cases.

## Files to Change

| File | Action | Description |
|------|--------|-------------|
| `todo.py` | Create | New Python CLI script for markdown-based to-do list management. |
| `TODO.md` | Create | Auto-generated on first use; contains the markdown task list. Created by `todo.py` at runtime, not committed. |

No existing files are modified.

## Risks

- **Concurrent writes**: If two `todo.py` processes run simultaneously, one may overwrite the other's changes. Mitigation: document that this is a single-user tool; concurrent use is not supported. File locking is intentionally out of scope per the requirements (stdlib only, single file).
- **Malformed TODO.md**: If the user manually edits `TODO.md` with malformed task lines (e.g., missing dots, non-integer IDs, or extra brackets), the parser may skip those lines silently or raise a `ValueError`. Mitigation: the parser validates the checkboxes + integer-ID structure; unrecognized lines are ignored with a warning printed to stderr. The tool never corrupts the file.
- **Large files**: The tool reads the entire file into memory. Mitigation: acceptable for a personal to-do list (typically <1000 tasks). For huge files, the tool could become slow; out of scope.
- **ID reuse after deletion**: The spec requires that deleted IDs are never reused. The implementation computes `max(existing_ids) + 1`, which naturally avoids reuse since deleted lines are removed. This is correct for monotonically-increasing IDs but means IDs grow without bound over the tool's lifetime. Mitigation: acceptable; IDs are small integers and growth is negligible.
- **Task text containing `[` or `]`**: A task with literal brackets (e.g., `install [package]`) could confuse the regex. Mitigation: the regex anchors on `-[ ]`/`-[x]` at the start of the line and the `<id>.` immediately after; brackets in the text are part of `.+` and are preserved verbatim during rewrite.
- **Non-ASCII text**: Python 3 defaults to UTF-8 for file I/O, so accented characters, CJK, and emoji in task text are handled correctly. Explicit `encoding="utf-8"` is used in `open()` calls for clarity.
- **Windows line endings**: `TODO.md` could contain `\r\n`. Mitigation: Python's `open()` with default text mode handles universal newlines; `Path.write_text()` uses the platform native. The parser uses `splitlines()` which normalizes all line endings.

## Acceptance Criteria

- [ ] `todo.py` exists at the repository root with a `#!/usr/bin/env python3` shebang.
- [ ] `python3 todo.py` (no args) defaults to `--show` and prints "No tasks" when no `TODO.md` exists or `TODO.md` lacks a `# Todo` header.
- [ ] `python3 todo.py --add "buy milk"` creates `TODO.md` (if absent) with a `# Todo` header and adds `- [ ] 1. buy milk`.
- [ ] Running `--add` twice with the same text creates two separate tasks (different IDs, same text).
- [ ] `python3 todo.py --show` displays all tasks in order with their IDs and checkbox status.
- [ ] `python3 todo.py --done 1` changes `- [ ]` to `- [x]` for task ID 1.
- [ ] `python3 todo.py --done 999` prints "Task 999 not found" and exits with code 1.
- [ ] `python3 todo.py --rm 1` removes the entire line for task ID 1 from `TODO.md`.
- [ ] `python3 todo.py --rm 999` prints "Task 999 not found" and exits with code 1.
- [ ] `python3 todo.py --clear` removes all `- [x]` lines, keeping pending tasks intact.
- [ ] After deletion, new tasks receive `max(remaining IDs) + 1` (never reuse deleted IDs).
- [ ] Invalid non-numeric arguments to `--done`/`--rm` are rejected by argparse.
- [ ] Conflicting flags (`--add` + `--done` simultaneously) are handled predictably (last-wins or explicit error).
- [ ] File I/O errors (e.g., read-only filesystem) print a descriptive error to stderr and exit with code 1.
- [ ] The script contains an `if __name__ == "__main__"` guard.
- [ ] The script uses only Python standard library modules (`argparse`, `re`, `pathlib`).
- [ ] No existing files are modified.

---

Spec: specs/46-spec/spec.md
