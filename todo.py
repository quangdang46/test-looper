#!/usr/bin/env python3
"""A markdown-based to-do tracker.

Stores tasks in TODO.md as markdown checkboxes.
Zero dependencies beyond the Python standard library.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, NamedTuple, Tuple

TODO_MD = Path("TODO.md")
TASK_RE = re.compile(r"^-\s+\[([ x])\]\s+(\d+)\.\s+(.*)$")
HEADER = "# Todo"


class Task(NamedTuple):
    """A single to-do item."""

    id: int
    description: str
    done: bool


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------


def read_tasks(file: Path) -> Tuple[List[Task], int]:
    """Parse the markdown file and return (tasks, next_id).

    Lines that don't match the expected pattern are silently skipped.
    """
    if not file.exists():
        return [], 1

    text = file.read_text(encoding="utf-8")
    tasks: List[Task] = []
    max_id = 0

    for line in text.splitlines():
        m = TASK_RE.match(line)
        if m:
            status = m.group(1)
            tid = int(m.group(2))
            desc = m.group(3)
            tasks.append(Task(tid, desc, done=(status == "x")))
            if tid > max_id:
                max_id = tid

    next_id = max_id + 1 if tasks else 1
    return tasks, next_id


def write_tasks(file: Path, tasks: List[Task]) -> None:
    """Serialise tasks to the markdown file."""
    lines = [HEADER + "\n"]
    for t in sorted(tasks, key=lambda x: x.id):
        status = "x" if t.done else " "
        lines.append(f"- [{status}] {t.id}. {t.description}\n")
    file.write_text("".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_show(tasks: List[Task]) -> int:
    """Print all tasks grouped by status (pending first, done after)."""
    if not tasks:
        print("No tasks")
        return 0

    pending = [t for t in tasks if not t.done]
    done = [t for t in tasks if t.done]

    for t in pending:
        print(f"[ ] {t.id}. {t.description}")
    for t in done:
        print(f"[x] {t.id}. {t.description}")
    return 0


def cmd_add(tasks: List[Task], next_id: int, text: str) -> int:
    """Append a new task with the next available ID."""
    tasks.append(Task(next_id, text, done=False))
    write_tasks(TODO_MD, tasks)
    print(f"Added task {next_id}")
    return 0


def cmd_done(tasks: List[Task], task_id: int) -> int:
    """Mark a task as completed."""
    for i, t in enumerate(tasks):
        if t.id == task_id:
            if t.done:
                return 0
            updated = list(tasks)
            updated[i] = Task(task_id, t.description, done=True)
            write_tasks(TODO_MD, updated)
            return 0
    print(f"Task {task_id} not found", file=sys.stderr)
    return 1


def cmd_rm(tasks: List[Task], task_id: int) -> int:
    """Delete a task entirely from the file."""
    for i, t in enumerate(tasks):
        if t.id == task_id:
            updated = list(tasks)
            updated.pop(i)
            write_tasks(TODO_MD, updated)
            return 0
    print(f"Task {task_id} not found", file=sys.stderr)
    return 1


def cmd_clear(tasks: List[Task]) -> int:
    """Remove all completed tasks."""
    pending = [t for t in tasks if not t.done]
    if len(pending) == len(tasks):
        return 0  # no-op
    write_tasks(TODO_MD, pending)
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments using argparse."""
    parser = argparse.ArgumentParser(description="Markdown-based to-do tracker")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--show", action="store_true", help="Show all tasks")
    group.add_argument(
        "--add", type=str, metavar="TEXT", help="Add a new task"
    )
    group.add_argument(
        "--done", type=int, metavar="ID", help="Mark a task as done"
    )
    group.add_argument(
        "--rm", type=int, metavar="ID", help="Remove a task"
    )
    group.add_argument(
        "--clear", action="store_true", help="Remove all completed tasks"
    )
    return parser.parse_args()


def main() -> None:
    """Entry point — parse CLI arguments, dispatch to the right command."""
    args = parse_args()

    try:
        tasks, next_id = read_tasks(TODO_MD)
    except (OSError, PermissionError) as e:
        print(f"Error reading TODO.md: {e}", file=sys.stderr)
        sys.exit(1)

    if args.show:
        sys.exit(cmd_show(tasks))
    elif args.add is not None:
        sys.exit(cmd_add(tasks, next_id, args.add))
    elif args.done is not None:
        sys.exit(cmd_done(tasks, args.done))
    elif args.rm is not None:
        sys.exit(cmd_rm(tasks, args.rm))
    elif args.clear:
        sys.exit(cmd_clear(tasks))


if __name__ == "__main__":
    main()
