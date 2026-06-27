#!/usr/bin/env python3
"""A CLI to-do list manager that stores tasks in TODO.md using Markdown checkboxes.

Usage:
    python todo.py               Show all tasks (same as --show)
    python todo.py --show        Show all tasks
    python todo.py --add "text"  Add a new pending task
    python todo.py --done <id>   Mark a task as completed
    python todo.py --rm <id>     Remove a task entirely
    python todo.py --clear       Remove all completed tasks
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TODO_FILE = Path("TODO.md")
HEADER = "# Todo"
TASK_RE = re.compile(
    r"^-\s+\[(?P<status>[ x])\]\s+(?P<id>\d+)\.\s+(?P<text>.+)$",
    re.MULTILINE,
)


def ensure_file() -> bool:
    """Create TODO.md with header if it does not exist.

    Returns True if the file was newly created, False otherwise.
    """
    if TODO_FILE.exists():
        return False
    TODO_FILE.write_text(f"{HEADER}\n\n")
    return True


def read_tasks() -> list[dict]:
    """Read TODO.md and return a list of task dicts.

    Each task dict has keys: id (int), text (str), done (bool).
    Returns an empty list if the file is empty or has no # Todo header.
    """
    if not TODO_FILE.exists():
        return []

    content = TODO_FILE.read_text(encoding="utf-8")

    has_header = False
    for line in content.splitlines():
        if line.strip() == HEADER:
            has_header = True
            break
    if not has_header:
        return []

    tasks = []
    for match in TASK_RE.finditer(content):
        tasks.append(
            {
                "id": int(match.group("id")),
                "text": match.group("text"),
                "done": match.group("status") == "x",
            }
        )
    tasks.sort(key=lambda t: t["id"])
    return tasks


def write_tasks(tasks: list[dict]) -> None:
    """Write tasks back to TODO.md."""
    tasks.sort(key=lambda t: t["id"])
    lines = [f"{HEADER}\n", "\n"]
    for task in tasks:
        status = "x" if task["done"] else " "
        lines.append(f"- [{status}] {task['id']}. {task['text']}\n")
    TODO_FILE.write_text("".join(lines), encoding="utf-8")


def next_id(tasks: list[dict]) -> int:
    """Compute the next available task ID."""
    return max((t["id"] for t in tasks), default=0) + 1


def find_task(tasks: list[dict], task_id: int) -> dict | None:
    """Find a task by its id. Returns None if not found."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def show(tasks: list[dict]) -> None:
    """Print all tasks or 'No tasks' if the list is empty."""
    if not tasks:
        print("No tasks")
        return
    for task in tasks:
        status = " " if not task["done"] else "x"
        print(f"[{status}] {task['id']}. {task['text']}")


def add(tasks: list[dict], text: str) -> None:
    """Add a new pending task."""
    if not text:
        print("Error: task text cannot be empty", file=sys.stderr)
        sys.exit(1)
    tasks.append({"id": next_id(tasks), "text": text, "done": False})
    write_tasks(tasks)


def done(tasks: list[dict], task_id: int) -> None:
    """Mark a task as completed."""
    task = find_task(tasks, task_id)
    if task is None:
        print(f"Task {task_id} not found", file=sys.stderr)
        sys.exit(1)
    task["done"] = True
    write_tasks(tasks)


def remove(tasks: list[dict], task_id: int) -> None:
    """Remove a task entirely."""
    task = find_task(tasks, task_id)
    if task is None:
        print(f"Task {task_id} not found", file=sys.stderr)
        sys.exit(1)
    tasks[:] = [t for t in tasks if t["id"] != task_id]
    write_tasks(tasks)


def clear(tasks: list[dict]) -> None:
    """Remove all completed tasks."""
    tasks[:] = [t for t in tasks if not t["done"]]
    write_tasks(tasks)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Manage a markdown-based to-do list (TODO.md)."
    )
    parser.add_argument("--show", action="store_true", help="Show all tasks")
    parser.add_argument("--add", type=str, help="Add a new pending task")
    parser.add_argument("--done", type=int, help="Mark a task as completed")
    parser.add_argument("--rm", type=int, help="Remove a task")
    parser.add_argument("--clear", action="store_true", help="Remove all done tasks")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Parse arguments, load the file, and dispatch to the appropriate action."""
    try:
        ensure_file()
        tasks = read_tasks()
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    args = parse_args(argv)

    try:
        if args.add is not None:
            add(tasks, args.add)
        elif args.done is not None:
            done(tasks, args.done)
        elif args.rm is not None:
            remove(tasks, args.rm)
        elif args.clear:
            clear(tasks)
        else:
            show(tasks)
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
