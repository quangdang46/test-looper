#!/usr/bin/env python3
"""A simple CLI to-do list stored in a markdown file.

Tasks are persisted as Markdown checkbox list items in TODO.md with
sequential integer IDs that are never reused.

Usage:
    python todo.py                     # Show all tasks
    python todo.py --show              # Show all tasks
    python todo.py --add "buy milk"    # Add a new pending task
    python todo.py --done 3            # Mark task 3 as completed
    python todo.py --rm 2              # Remove task 2 entirely
    python todo.py --clear             # Delete all completed tasks
"""

import argparse
import re
import sys
from pathlib import Path

TODO_FILE = Path("TODO.md")
TASK_PATTERN = re.compile(r"^- \[([ x])\] (\d+)\. (.+)$")
HEADER = "# Todo"


def parse_todo(path: Path):
    """Read and parse the TODO.md file.

    Returns (tasks, next_id) where:
      tasks   — list of dicts with keys: id, description, done
      next_id — the next available task ID (max existing + 1, or 1 if none)
    """
    if not path.exists():
        return [], 1

    content = path.read_text(encoding="utf-8")
    return _parse_content(content)


def _parse_content(content: str):
    """Parse TODO.md content string into tasks."""
    tasks = []
    max_id = 0
    found_header = False

    for line in content.splitlines():
        if line.strip() == HEADER:
            found_header = True
        m = TASK_PATTERN.match(line)
        if m:
            done = m.group(1) == "x"
            task_id = int(m.group(2))
            desc = m.group(3)
            tasks.append({"id": task_id, "description": desc, "done": done})
            max_id = max(max_id, task_id)

    if not found_header:
        return [], 1

    return tasks, max_id + 1


def _find_task_by_id(tasks, task_id):
    """Return the task dict with the given id, or None."""
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None


def ensure_header(content: str) -> str:
    """Prepend '# Todo' header if content does not already start with it."""
    lines = content.splitlines()
    if not lines or lines[0].strip() != HEADER:
        return HEADER + "\n" + content
    return content


def show_tasks(path: Path):
    """Display all tasks grouped by Pending / Done status."""
    if not path.exists():
        path.write_text(HEADER + "\n", encoding="utf-8")
        print("No tasks.")
        return

    content = path.read_text(encoding="utf-8")
    tasks, _ = _parse_content(content)

    if not tasks:
        print("No tasks.")
        return

    pending = [t for t in tasks if not t["done"]]
    done = [t for t in tasks if t["done"]]

    if pending:
        print("Pending:")
        for t in pending:
            print(f"{t['id']}. {t['description']}")
        print()

    if done:
        print("Done:")
        for t in done:
            print(f"{t['id']}. {t['description']}")
        print()


def add_task(description: str, path: Path):
    """Append a new pending task and print confirmation."""
    tasks, next_id = parse_todo(path)

    if not path.exists() or not tasks:
        if path.exists():
            content = path.read_text(encoding="utf-8")
            content = ensure_header(content)
        else:
            content = HEADER + "\n"
        path.write_text(content, encoding="utf-8")

    task_id = next_id
    with path.open("a", encoding="utf-8") as f:
        f.write(f"- [ ] {task_id}. {description}\n")

    print(f"Added task {task_id}: {description}")


def mark_done(task_id: int, path: Path):
    """Mark a task as completed (no-op if already done)."""
    if not path.exists():
        path.write_text(HEADER + "\n", encoding="utf-8")
        print(f"Task {task_id} not found")
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    tasks, _ = _parse_content(content)

    if not _find_task_by_id(tasks, task_id):
        print(f"Task {task_id} not found")
        sys.exit(1)

    lines = content.splitlines(keepends=True)
    new_lines = []
    found = False
    for line in lines:
        m = TASK_PATTERN.match(line.strip())
        if m and int(m.group(2)) == task_id:
            new_lines.append(line.replace("- [ ] ", "- [x] ", 1))
            found = True
        else:
            new_lines.append(line)

    if found:
        path.write_text("".join(new_lines), encoding="utf-8")
        print(f"Task {task_id} completed")
    else:
        # Shouldn't reach here after _find_task_by_id check, but be safe
        print(f"Task {task_id} not found")
        sys.exit(1)


def remove_task(task_id: int, path: Path):
    """Remove a task line entirely from TODO.md."""
    if not path.exists():
        path.write_text(HEADER + "\n", encoding="utf-8")
        print(f"Task {task_id} not found")
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    tasks, _ = _parse_content(content)

    if not _find_task_by_id(tasks, task_id):
        print(f"Task {task_id} not found")
        sys.exit(1)

    lines = content.splitlines(keepends=True)
    new_lines = []
    for line in lines:
        m = TASK_PATTERN.match(line.strip())
        if m and int(m.group(2)) == task_id:
            continue  # skip this task line
        new_lines.append(line)

    path.write_text("".join(new_lines), encoding="utf-8")
    print(f"Removed task {task_id}")


def clear_done(path: Path):
    """Remove all completed task lines."""
    if not path.exists():
        print("No tasks.")
        return

    content = path.read_text(encoding="utf-8")
    tasks, _ = _parse_content(content)

    done_tasks = [t for t in tasks if t["done"]]
    if not done_tasks:
        print("No completed tasks to clear.")
        return

    lines = content.splitlines(keepends=True)
    new_lines = []
    for line in lines:
        m = TASK_PATTERN.match(line.strip())
        if m and m.group(1) == "x":
            continue  # skip done task lines
        new_lines.append(line)

    path.write_text("".join(new_lines), encoding="utf-8")
    print(f"Cleared {len(done_tasks)} completed task(s).")


def main():
    """Parse command-line arguments and dispatch to the appropriate handler."""
    parser = argparse.ArgumentParser(
        description="Manage a to-do list stored in TODO.md"
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show all tasks (default behavior)",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--add",
        type=str,
        metavar="TEXT",
        help="Add a new task with the given description",
    )
    group.add_argument(
        "--done",
        type=int,
        metavar="ID",
        help="Mark a task as completed by its ID",
    )
    group.add_argument(
        "--rm",
        type=int,
        metavar="ID",
        help="Remove a task by its ID",
    )
    group.add_argument(
        "--clear",
        action="store_true",
        help="Remove all completed tasks",
    )

    args = parser.parse_args()

    if args.add is not None:
        if not args.add.strip():
            print("Task description cannot be empty", file=sys.stderr)
            sys.exit(1)
        add_task(args.add.strip(), TODO_FILE)
    elif args.done is not None:
        mark_done(args.done, TODO_FILE)
    elif args.rm is not None:
        remove_task(args.rm, TODO_FILE)
    elif args.clear:
        clear_done(TODO_FILE)
    else:
        show_tasks(TODO_FILE)


if __name__ == "__main__":
    main()
