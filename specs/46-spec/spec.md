# Specification: Issue #46 - Build a Markdown-Based To-Do Tracker

## Objective
Create a single-file CLI tool `todo.py` (Python stdlib only) that reads and writes a to-do list stored in `TODO.md` using standard GitHub-Flavored Markdown task-list syntax. The tool supports five operations: show tasks, add a task, mark a task as done, remove a task, and clear all completed tasks. No external dependencies are required.

---

## Implementation Plan

1. **Create `todo.py` skeleton**  
   - Single file at the repository root.  
   - `if __name__ == "__main__":` block that dispatches to sub-functions based on parsed CLI arguments.  
   - Module-level docstring with usage examples.

2. **Define argument parser (`argparse`)**  
   - `--show` / no-flag: list current tasks, formatted as `N. [ ] description` or `N. [x] description`.  
   - `--add TEXT`: append a new pending task with an auto-incremented integer ID.  
   - `--done ID`: mark the task with the given integer ID as completed (`[ ]` → `[x]`).  
   - `--rm ID`: remove the task line entirely from the file.  
   - `--clear`: delete all completed task lines, leaving pending tasks and non-task lines intact.  
   - Mutually exclusive group — only one action per invocation.

3. **Implement `TODO.md` I/O layer**  
   - **Read:** Parse the file into an in-memory list of `(id, text, done, line_index)` tuples plus a parallel list of non-task lines with their positions.  
     - Locate the `# Todo` header (case-insensitive regex).  
     - Below the header, scan lines matching `- [ ] <id>. <text>` (pending) or `- [x] <id>. <text>` (done).  
     - Lines that don't match the task pattern are preserved verbatim as non-task lines.  
   - **Write:** Reconstruct the file from the in-memory representation, preserving the `# Todo` header, all non-task lines in their original order, and task lines re-rendered from the `(id, text, done)` tuples.  
   - **File creation:** If `TODO.md` does not exist, create it with the `# Todo` header and a trailing blank line on first invocation.

4. **Implement core commands**  

   | Command | Logic |
   |---------|-------|
   | `--show` | Read file → print each task as `ID. [ ] text` or `ID. [x] text`. If no tasks, print "No tasks". |
   | `--add` | Read file → compute `next_id = max(existing_ids, 0) + 1` → append new pending task line → write. |
   | `--done` | Read file → find task by ID → change status to done (`- [ ]` → `- [x]`) → write. If not found, print "Task <id> not found" and exit 1. |
   | `--rm` | Read file → remove the task line entirely → write. If not found, print "Task <id> not found" and exit 1. |
   | `--clear` | Read file → remove all lines where `done == True` while preserving pending tasks and all non-task lines → write. |

5. **Error handling**  
   - `FileNotFoundError` when reading → treat as empty → create fresh file with header.  
   - `PermissionError` / `OSError` → print descriptive error message and exit 1.  
   - Malformed `TODO.md` (no `# Todo` header anywhere) → print "No tasks" without modifying the file.  
   - Empty `TODO.md` or file with only a header → print "No tasks".

6. **Idempotency and edge cases**  
   - Task IDs are integers, auto-increment from 1, never reused after deletion.  
   - Adding a task with duplicate text is allowed (each gets a unique ID).  
   - `--clear` on a file with no done tasks is a no-op (exits 0, no error, no file modification).  
   - `--done` on an already-done task is a no-op (succeeds silently).  
   - `--rm` on a non-existent ID prints "Task <id> not found" and exits 1.  

---

## Files to Change

| File | Action | Notes |
|------|--------|-------|
| `todo.py` | **Create** | The CLI tool — approximately 150 lines of Python 3. Uses only `argparse`, `re`, `os`, `sys`, and `pathlib`. |
| `TODO.md` | **Create** | Default task file; auto-created on first run if it does not exist. |
| `specs/46-spec/spec.md` | **Create** | This specification document. |

---

## Risks

1. **Non-task line preservation** — The parser must faithfully preserve comment lines, blank lines, and any other markdown content that appears between or around tasks. Using a line-based round-trip that only modifies lines matching `- [ ] N.` or `- [x] N.` mitigates this. If non-task lines are accidentally dropped or reordered, users could lose important context in their `TODO.md` file.  
2. **`# Todo` header detection** — Must be case-insensitive and tolerate trailing whitespace or variations like `# TODO`, `## Todo`, or `#todo`. Use a regex match rather than exact string equality. A missing header should not corrupt the file.  
3. **ID gaps** — Deleted IDs are never reused, so the ID sequence grows monotonically. Over very long usage with frequent add/remove cycles, IDs can become large. This is an intentional design choice that avoids confusion from ID reassignment.  
4. **Race conditions** — No file locking is implemented. Concurrent invocations on the same `TODO.md` could interleave reads and writes, causing lost updates. Acceptable for a single-user CLI tool; documenting this limitation is sufficient.  
5. **Large files** — The current approach reads the entire file into memory. For a personal to-do tracker this is acceptable, but files with tens of thousands of tasks could be slow.  
6. **Leading/trailing whitespace in task text** — User-supplied text should be stripped of extraneous whitespace when serialized to keep the file clean.

---

## Acceptance Criteria

1. `python todo.py --show` on a non-existent or empty `TODO.md` prints "No tasks" and creates `TODO.md` with the `# Todo` header.  
2. `python todo.py --add "buy milk"` creates a `- [ ] 1. buy milk` line below the header.  
3. `python todo.py --add "buy milk"` again creates a `- [ ] 2. buy milk` line (duplicate text allowed, new auto-incremented ID).  
4. `python todo.py --done 1` changes the matching line to `- [x] 1. buy milk`.  
5. `python todo.py --done 1` a second time is a no-op (the line remains `- [x] 1. buy milk`).  
6. `python todo.py --done 999` prints "Task 999 not found" to stderr and exits with code 1.  
7. `python todo.py --rm 1` removes the matching task line from `TODO.md` entirely.  
8. `python todo.py --rm 999` prints "Task 999 not found" to stderr and exits with code 1.  
9. `python todo.py --clear` removes all `- [x]` lines while leaving pending tasks and non-task lines untouched.  
10. `python todo.py --clear` with no done tasks is a no-op (exits 0, file unchanged).  
11. Non-task lines (blank lines, markdown headings, comments, arbitrary text) above, below, and between tasks survive all operations without modification.  
12. `python todo.py --add "new"` after a prior `--rm` does **not** reuse the deleted ID (the next available integer is used).  
13. All operations use only Python stdlib modules (`argparse`, `re`, `os`, `sys`, `pathlib`).  
14. `python todo.py` (no flag) behaves identically to `python todo.py --show`.  
15. Malformed `TODO.md` with no `# Todo` header causes `--show` to print "No tasks" without overwriting or corrupting the file contents.

---

Spec: specs/46-spec/spec.md
