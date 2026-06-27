# Implementation Plan: Markdown-based To-Do Tracker (Issue #46)

**Issue:** quangdang46/test-looper#46
**File:** `todo.py` (single-file CLI tool)
**Dependencies:** Python stdlib only (`argparse`, `re`, `pathlib`)

---

## 1. Overview

Create `todo.py` — a CLI to-do list manager that stores tasks in a `TODO.md` file
using Markdown checkbox syntax. The tool lives in the repo root alongside
`greeting.py` and follows the same coding style (shebang, docstring, `__main__`
guard, type annotations).

---

## 2. Data Format

The `TODO.md` file has a `# Todo` header followed by checkbox list items:

```markdown
# Todo

- [ ] 1. buy milk
- [ ] 2. call mom
- [x] 3. finish homework
```

- Task IDs are **integers**, auto-incrementing from 1.
- **Deleted IDs are never reused** — a new task always gets `max(existing_ids) + 1`.
- When a task is removed, its line is **deleted entirely** from the file
  (remaining IDs stay unchanged).

---

## 3. CLI Interface

| Command | Behaviour |
|---|---|
| `python todo.py` | Print all tasks (same as `--show`) |
| `python todo.py --show` | Print all tasks or "No tasks" if empty |
| `python todo.py --add "buy milk"` | Append a new pending task |
| `python todo.py --done 3` | Mark task 3 as done (`[ ]` → `[x]`) |
| `python todo.py --rm 2` | Remove task 2's line entirely |
| `python todo.py --clear` | Delete all done (checked) tasks |

---

## 4. Edge Cases (per issue requirements)

| Scenario | Behaviour |
|---|---|
| `TODO.md` exists, has `# Todo` header, but no tasks | Print "No tasks" |
| `TODO.md` is missing | Create it with `# Todo\n\n` header |
| `TODO.md` has no `# Todo` header | Treat as empty — print "No tasks" |
| `--done` / `--rm` with non-existent id | Print "Task <id> not found" |
| `--add` with duplicate text | OK — same text, new ID |
| Empty `--add` text | Print error message, exit non-zero |
| File I/O failure (permissions, etc.) | Print error message, exit non-zero |

---

## 5. Implementation Steps

### Step 1 — File scaffolding

Create `todo.py` at repo root with:
- Shebang line `#!/usr/bin/env python3`
- Module-level docstring describing the tool and usage
- `import` statements: `argparse`, `re`, `pathlib.Path`
- `__main__` guard with `main()` call

### Step 2 — Constants & helpers

Define:
- `TODO_FILE: Path` — path to `TODO.md` in the current working directory.
- `HEADER = "# Todo"` — the expected section header.
- `TASK_RE: re.Pattern` — compiled regex to match `- [ ] <id>. <text>` or
  `- [x] <id>. <text>`. Named groups: `status` (space or `x`), `id` (digits),
  `text` (rest of line).

### Step 3 — `ensure_file() -> bool`

If `TODO.md` does not exist, create it with `# Todo\n\n` content.
Returns `True` if the file was newly created, `False` otherwise.
This lets callers distinguish "just created the file" from "file existed".

### Step 4 — `read_tasks(path) -> list[dict]`

Read `TODO.md`, return a list of task dicts `{id: int, text: str, done: bool}`.

- Open and read the file.
- If the file is empty or has no `# Todo` header, return an empty list.
- Use `TASK_RE.finditer` to extract all task lines after the header.
- Return tasks sorted by `id`.

### Step 5 — `write_tasks(path, tasks) -> None`

Write tasks back to `TODO.md`.

- Open the file for writing.
- Write `# Todo\n\n`.
- For each task (sorted by id), write `- [x] {id}. {text}\n` if done,
  else `- [ ] {id}. {text}\n`.

### Step 6 — `next_id(tasks) -> int`

Compute the next available task ID: `max(t['id'] for t in tasks, default=0) + 1`.

### Step 7 — `find_task(tasks, task_id) -> dict | None`

Linear scan for a task dict with matching `id`. Returns `None` if not found.

### Step 8 — CLI sub-commands

Each maps to a function called from `main()`.

1. **`show(tasks)`** — If `tasks` empty, print "No tasks". Otherwise, print each
   task with status prefix (e.g., `[ ] 1. buy milk` or `[x] 3. finish homework`).

2. **`add(tasks, text, path)`** — Compute `next_id`, append a new task dict,
   call `write_tasks`.

3. **`done(tasks, task_id, path)`** — `find_task`. If not found, print
   "Task <id> not found" and exit(1). Otherwise, set `done = True`,
   call `write_tasks`.

4. **`remove(tasks, task_id, path)`** — `find_task`. If not found, print
   "Task <id> not found" and exit(1). Otherwise, filter out the task,
   call `write_tasks`.

5. **`clear(tasks, path)`** — Filter out done tasks, call `write_tasks`.

### Step 9 — `main()` wiring

```
Create ArgumentParser with:
  - --show   (store_true, default)
  - --add    (str)
  - --done   (int)
  - --rm     (int)
  - --clear  (store_true)

→ ensure_file()
→ read_tasks()
→ dispatch based on which arg was set:
    • --add    → add(tasks, args.add)
    • --done   → done(tasks, args.done)
    • --rm     → remove(tasks, args.rm)
    • --clear  → clear(tasks)
    • default  → show(tasks)
```

Arguments are **mutually exclusive**: only one action per invocation.

---

## 6. Error Handling Strategy

| Situation | Behaviour |
|---|---|
| File read error (permissions) | `print("Error: ...", file=sys.stderr); sys.exit(1)` |
| File write error (permissions) | Same as above |
| `--add ""` (empty text) | `print("Error: task text cannot be empty", file=sys.stderr); sys.exit(1)` |
| `--done` / `--rm` with non-existent id | `print("Task <id> not found", file=sys.stderr); sys.exit(1)` |
| Multiple conflicting flags | argparse's built-in conflict detection handles this |

---

## 7. Architecture Diagram (Data Flow)

```
User CLI input
      │
      ▼
  main()           ◄── argparse parses args
      │
      ▼
  ensure_file()    ◄── creates TODO.md if missing
      │
      ▼
  read_tasks()     ◄── parses TODO.md → list of dicts
      │
      ▼
  dispatch ──┬── show/tasks   (read-only)
             ├── add          (mutate → write_tasks)
             ├── done         (mutate → write_tasks)
             ├── remove       (mutate → write_tasks)
             └── clear        (mutate → write_tasks)
```

---

## 8. File Layout

```
repo-root/
├── greeting.py          (existing)
├── todo.py              ★ NEW — the todo CLI
├── specs/46-spec/
│   └── spec.md          ★ NEW — this plan
└── README.md
```

`TODO.md` will be created at repo root on first run.

---

## 9. Testing Plan

Manual verification checklist (issue is a simple CLI tool, no test framework):

1. `rm -f TODO.md && python todo.py` → creates TODO.md, prints "No tasks"
2. `python todo.py --add "buy milk"` → adds task 1
3. `python todo.py --add "call mom"` → adds task 2
4. `python todo.py --show` → shows both tasks
5. `python todo.py --done 1` → marks task 1 as `[x]`
6. `python todo.py --rm 2` → removes task 2 entirely
7. `python todo.py --clear` → removes done task 1
8. `python todo.py --done 99` → prints "Task 99 not found"
9. `python todo.py --rm 99` → prints "Task 99 not found"
10. `python todo.py --add "buy milk"` → adds task 2 (id increments correctly)
11. `python todo.py --show` on empty file with only header → "No tasks"
