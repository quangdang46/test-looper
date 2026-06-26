---
title: Markdown-based To-Do Tracker
issue: 46
status: draft
---

## Objective

Build a single-file CLI tool `todo.py` (no external dependencies, Python stdlib only) that manages a simple to-do list stored in a markdown file (`TODO.md`). Users create, list, complete, delete, and clear tasks via command-line flags, and the file remains human-readable markdown at all times.

---

## Implementation Plan

### 1. Create `todo.py` in the repo root

A single Python script with an `if __name__ == "__main__"` block. Structure:

- **Constants / paths**: define `TODO_FILENAME = "TODO.md"` as a module-level constant. Let the caller override via an env var `TODO_FILE` so tests can use a temp path.
- **Task representation**: Use a `dataclass` (stdlib, Python 3.7+) or a plain `NamedTuple` to hold `(id: int, text: str, done: bool)`.
- **Parse function** `parse_todo(path: Path) -> tuple[list[Task], bool]`:
  - If the file does not exist, return `([], False)` (fresh start).
  - Read the markdown file line by line.
  - Look for the `# Todo` header to confirm the file has content. If absent, return `([], False)` signifying "no tasks".
  - For each line, match `- [ ] <id>. <text>` (pending) or `- [x] <id>. <text>` (done). Build the task list preserving file order.
  - Lines that don't match a task pattern are ignored (so users can add comments or blank lines).
  - **Edge case**: Empty file or file with only a `# Todo` header → return `([], True)` (header exists but no tasks).
- **Write function** `write_todo(path: Path, tasks: list[Task]) -> None`:
  - Reconstruct the full markdown: `# Todo\n\n` followed by one line per task in the current order.
  - Create the file (and its parent directories) if it doesn't exist.
- **CLI argument parser** using `argparse`:
  - `--show` / no flag: display tasks (default action).
  - `--add TEXT`: append a new pending task with the next available id.
  - `--done ID`: mark a task as completed by id.
  - `--rm ID`: remove a task by id entirely.
  - `--clear`: remove all completed tasks.
  - Mutually exclusive group so only one action runs per invocation.
- **Display logic**:
  - File missing or `# Todo` header absent → print `"No tasks"`.
  - Zero tasks under a valid header → print `"No tasks"`.
  - Otherwise print each task as `id. [ ] text` or `id. [x] text` (mirroring the markdown format).
- **Error handling** for task id operations:
  - `--done` / `--rm` with an id that doesn't exist → print `"Task <id> not found"` and exit with code 1.
- **Id assignment**:
  - Scan existing tasks for the highest id, then assign `max_id + 1`.
  - Never reuse ids from deleted tasks.

### 2. Verify with manual smoke tests

Run `python todo.py`, `python todo.py --add "test"`, `python todo.py --done 1`, `python todo.py --rm 1`, `python todo.py --clear` against the default `TODO.md` and a temp file.

### 3. Optionally add a usage docstring at the top of `todo.py`

Include example invocations so `python todo.py --help` and `python todo.py -h` provide useful output.

---

## Files to Change

| File | Action | Description |
|------|--------|-------------|
| `todo.py` | **Create** | The CLI to-do tracker; contains all parsing, formatting, and CLI dispatch logic. Single file, no external dependencies. |
| `TODO.md` | **Create** (auto) | The markdown data file, created on first write if missing. Listed here for documentation; the tool itself creates it. |

No existing files are modified.

---

## Risks

1. **File locking / concurrent writes**: Two `todo.py` invocations at the same time could corrupt `TODO.md`. Mitigation: not required for this issue; accept single-user sequential usage as the baseline. If needed later, add `filelock` or an atomic-write pattern.
2. **Idempotency on `--done`**: Running `--done` on an already-completed task is harmless but the implementation must handle it gracefully (re-write the same state, no error).
3. **Id gaps after `--rm`**: Deleted tasks leave gaps in the id sequence. The spec says "never reuse deleted ids" — this is by design. If the file is hand-edited and ids become non-sequential, parsing should still work (ids are read from the file, not regenerated).
4. **Hand-edited `TODO.md`**: Users may edit the file directly. The parser must tolerate extra whitespace, missing space after `- [x]`, or non-standard id ordering. The `re` regex should be flexible enough for reasonable human edits (e.g., optional spaces, case-insensitive `x`).
5. **Large task lists**: Not a concern for the expected use case, but re-writing the entire file on every mutation is O(n). Acceptable.

---

## Acceptance Criteria

1. **`python todo.py`** (no args) prints current tasks from `TODO.md`, or `"No tasks"` if the file is missing/empty/headerless.
2. **`python todo.py --show`** behaves identically to the no-arg case.
3. **`python todo.py --add "buy milk"`** appends a new pending task with the next sequential id and prints no output on success.
4. **`python todo.py --done 3`** marks task id 3 as completed (`- [x]`) in `TODO.md`.
5. **`python todo.py --rm 2`** removes task id 2 from `TODO.md` entirely, leaving other tasks' ids unchanged.
6. **`python todo.py --clear`** removes all completed (`- [x]`) tasks, keeping pending tasks intact.
7. **`python todo.py --done 999`** prints `"Task 999 not found"` and exits with code 1.
8. **`python todo.py --add`** (no text) triggers argparse error with usage message.
9. **File creation**: Running `--add` when `TODO.md` does not exist creates `TODO.md` with the `# Todo` header.
10. **Id assignment**: After deleting tasks, a new `--add` uses `max(existing ids) + 1`, not the first available slot.
11. **Duplicate text allowed**: `--add "buy milk"` twice produces two tasks with distinct ids and the same text.
12. **No external dependencies**: `import` statements use only Python stdlib modules.
13. **`__main__` block** present in `todo.py`.
14. **Usage shown** via `python todo.py --help`.

---

Spec: specs/46-spec/spec.md
