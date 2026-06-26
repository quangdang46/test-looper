# Spec: Markdown-Based To-Do Tracker

**Issue:** #46 — build a markdown-based to-do tracker

---

## Objective

Create a single-file CLI tool `todo.py` (Python stdlib only) that reads and writes a to-do list stored in `TODO.md` using standard GitHub-Flavored Markdown task-list syntax. The tool supports five operations: show tasks, add a task, mark a task as done, remove a task, and clear all completed tasks.

---

## Implementation Plan

1. **Create `todo.py` skeleton**  
   - Single file at repository root.  
   - `if __name__ == "__main__":` block that dispatches to sub-functions based on parsed CLI arguments.  
   - Module-level docstring with usage examples.

2. **Define argument parser (`argparse`)**  
   - `--show` / no-flag: list current tasks.  
   - `--add TEXT`: add a new pending task.  
   - `--done ID`: mark task with given integer ID as completed.  
   - `--rm ID`: remove the task line entirely.  
   - `--clear`: delete all completed tasks.  
   - Mutually exclusive groups so only one action runs per invocation.

3. **Implement `TODO.md` I/O layer**  
   - **Read:** Parse the file into an in-memory list of `(id, text, done)` tuples.  
     - Locate the `# Todo` header (case-insensitive).  
     - Below the header, scan lines matching `- [ ] <id>. <text>` (pending) or `- [x] <id>. <text>` (done).  
     - Lines that don't match the task pattern are preserved verbatim as non-task lines (separator rows, comments, blank lines).  
   - **Write:** Reconstruct the file from the in-memory representation, preserving:
     - The `# Todo` header line.  
     - All non-task lines in their original positions.  
     - Task lines re-rendered from the `(id, text, done)` tuples.  
   - **File creation:** If `TODO.md` does not exist, create it with the `# Todo` header and a trailing blank line.

4. **Implement core commands**  

   | Command | Logic |
   |---------|-------|
   | `--show` | Read file → print each task as `ID. [ ] text` or `ID. [x] text`. If no tasks, print "No tasks". |
   | `--add` | Read file → compute `next_id = max(existing_ids, 0) + 1` → append new task line → write. |
   | `--done` | Read file → find task by ID → change `- [ ]` to `- [x]` → write. If not found, print "Task <id> not found" and exit 1. |
   | `--rm` | Read file → remove the task line entirely → write. If not found, print "Task <id> not found" and exit 1. |
   | `--clear` | Read file → remove all lines where `done == True` (preserve everything else) → write. |

5. **Error handling**  
   - `FileNotFoundError` when reading → treat as empty, create fresh file with header.  
   - `PermissionError` / `OSError` → print descriptive error and exit 1.  
   - Malformed `TODO.md` (e.g. no `# Todo` header) → treat as "No tasks", but preserve the file's existing content above/below non-header lines.  
   - Empty `TODO.md` (no `# Todo` header at all) → print "No tasks".

6. **Idempotency and edge cases**  
   - Task IDs are integers, auto-increment from 1, never reused after deletion.  
   - Adding a task with duplicate text is allowed (each gets a unique ID).  
   - `--clear` on a file with no done tasks is a no-op (exits 0, no error).  
   - `--done` on an already-done task is a no-op (succeeds silently).  
   - `--rm` on a non-existent ID prints "Task <id> not found" and exits 1.  

---

## Files to Change

| File | Action | Notes |
|------|--------|-------|
| `todo.py` | **Create** | The CLI tool — ~150 lines of Python. |
| `TODO.md` | **Create** | Default task file (auto-created on first run). |
| `specs/46-spec/spec.md` | **Create** | This document. |

---

## Risks

1. **Non-task line preservation** — The parser must faithfully preserve comment lines, blank lines, and any non-task markdown between or around tasks. A line-based round-trip that only touches lines matching `- [ ] N.` or `- [x] N.` mitigates this.  
2. **`# Todo` header detection** — Must be case-insensitive and tolerate trailing whitespace or variation like `# TODO`. Use a regex match rather than exact equality.  
3. **ID gaps** — Since deleted IDs are never reused, the ID sequence can grow unbounded over time if tasks are frequently added and removed. This is an intentional design choice per the spec.  
4. **Race conditions** — No file locking; concurrent invocations on the same `TODO.md` could interleave reads and writes. Acceptable for a single-user CLI tool.  
5. **Large files** — The current approach reads the entire file into memory. Acceptable for a personal to-do tracker.

---

## Acceptance Criteria

1. `python todo.py --show` on a non-existent or empty `TODO.md` prints "No tasks" and creates `TODO.md` with the `# Todo` header.  
2. `python todo.py --add "buy milk"` creates a `- [ ] 1. buy milk` line below the header.  
3. `python todo.py --add "buy milk"` a second time creates `- [ ] 2. buy milk` (duplicate text, new ID).  
4. `python todo.py --done 1` changes the line to `- [x] 1. buy milk`.  
5. `python todo.py --done 1` a second time is a no-op (already done).  
6. `python todo.py --done 999` prints "Task 999 not found" and exits with code 1.  
7. `python todo.py --rm 1` removes that line from `TODO.md` entirely.  
8. `python todo.py --rm 999` prints "Task 999 not found" and exits with code 1.  
9. `python todo.py --clear` removes all `- [x]` lines, leaves pending tasks and non-task lines intact.  
10. `python todo.py --clear` with no done tasks is a no-op (exits 0).  
11. **Non-task lines** (blank lines, comments, other markdown) above/below/between tasks survive all operations without modification.  
12. `python todo.py --add "task"` after `--rm` does **not** reuse the deleted ID (next available integer).  
13. All operations use only Python stdlib (`argparse`, `re`, `pathlib`).  
14. `python todo.py` (no flag) behaves identically to `python todo.py --show`.

---

Spec: specs/46-spec/spec.md
