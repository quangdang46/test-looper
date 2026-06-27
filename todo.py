#!/usr/bin/env python3
"""Markdown-based to-do list tracker.

Manages a simple to-do list stored in TODO.md in the current working directory.
Uses standard markdown checkboxes (- [ ] for pending, - [x] for done).

Usage:
    python todo.py --show              Show all tasks
    python todo.py --add "task text"   Add a new task
    python todo.py --done <task-id>    Mark a task as completed
    python todo.py --rm <task-id>      Remove a task
    python todo.py --clear             Remove all completed tasks
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

TODO_FILE = Path("TODO.md")
HEADER = "# Todo"

# Matches task lines: "- [ ] <id>. <description>" or "- [x] <id>. <description>"
TASK_RE = re.compile(r"^- \[([ x])\] (\d+)\. (.+)")


def _build_parser() -> argparse.ArgumentParser:
    """Create the argument parser with mutually exclusive flags."""
    parser = argparse.ArgumentParser(
        description="Manage a to-do list stored in TODO.md",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--show",
        action="store_true",
        help="show all tasks",
    )
    group.add_argument(
        "--add",
        metavar="TEXT",
        type=str,
        help="add a new task",
    )
    group.add_argument(
        "--done",
        metavar="TASK_ID",
        type=int,
        help="mark a task as completed",
    )
    group.add_argument(
        "--rm",
        metavar="TASK_ID",
        type=int,
        help="remove a task",
    )
    group.add_argument(
        "--clear",
        action="store_true",
        help="remove all completed tasks",
    )
    return parser


PARSER = _build_parser()


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    return PARSER.parse_args()


def ensure_file() -> None:
    """Create TODO.md with the # Todo header if it does not exist."""
    if not TODO_FILE.exists():
        try:
            TODO_FILE.write_text(HEADER + "\n")
        except OSError as e:
            print(f"Error creating {TODO_FILE}: {e}", file=sys.stderr)
            sys.exit(1)


def read_tasks() -> list[tuple[int, str, bool]]:
    """Parse TODO.md into a list of (id, description, done) tuples.

    Returns an empty list if the file does not exist, has no # Todo header,
    or contains no matching task lines.
    """
    if not TODO_FILE.exists():
        return []
    try:
        content = TODO_FILE.read_text()
    except OSError as e:
        print(f"Error reading {TODO_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    # Without the header, treat the file as empty
    if HEADER not in content:
        return []

    tasks: list[tuple[int, str, bool]] = []
    for line in content.splitlines():
        m = TASK_RE.match(line)
        if m:
            tasks.append((int(m.group(2)), m.group(3), m.group(1) == "x"))
    return tasks


def write_tasks(tasks: list[tuple[int, str, bool]]) -> None:
    """Serialize tasks back to TODO.md in markdown format."""
    lines = [HEADER, ""]
    for tid, desc, done in tasks:
        checkbox = "x" if done else " "
        lines.append(f"- [{checkbox}] {tid}. {desc}")
    try:
        TODO_FILE.write_text("\n".join(lines) + "\n")
    except OSError as e:
        print(f"Error writing {TODO_FILE}: {e}", file=sys.stderr)
        sys.exit(1)


def find_task(tasks: list[tuple[int, str, bool]], task_id: int) -> Optional[int]:
    """Return the index of a task by its ID, or None if not found."""
    for i, (tid, _, _) in enumerate(tasks):
        if tid == task_id:
            return i
    return None


def next_id(tasks: list[tuple[int, str, bool]]) -> int:
    """Return the next available task ID.

    Uses max(existing IDs) + 1, or 1 if the list is empty.
    Deleted IDs are never reused.
    """
    if not tasks:
        return 1
    return max(tid for tid, _, _ in tasks) + 1


def cmd_show(tasks: list[tuple[int, str, bool]]) -> None:
    """Print all tasks, or 'No tasks' if the list is empty."""
    if not tasks:
        print("No tasks")
        return
    for tid, desc, done in tasks:
        status = "x" if done else " "
        print(f"{tid}. {desc} [{status}]")


def cmd_add(tasks: list[tuple[int, str, bool]], text: str) -> None:
    """Append a new task with the given description."""
    stripped = text.strip()
    if not stripped:
        print("Error: task text cannot be empty", file=sys.stderr)
        sys.exit(1)
    tasks.append((next_id(tasks), stripped, False))
    write_tasks(tasks)
    print(f"Added task {tasks[-1][0]}: {stripped}")


def cmd_done(tasks: list[tuple[int, str, bool]], task_id: int) -> None:
    """Mark a task as completed."""
    idx = find_task(tasks, task_id)
    if idx is None:
        print(f"Task {task_id} not found", file=sys.stderr)
        sys.exit(1)
    tid, desc, _ = tasks[idx]
    tasks[idx] = (tid, desc, True)
    write_tasks(tasks)
    print(f"Task {task_id} marked as done")


def cmd_rm(tasks: list[tuple[int, str, bool]], task_id: int) -> None:
    """Remove a task entirely from the list."""
    idx = find_task(tasks, task_id)
    if idx is None:
        print(f"Task {task_id} not found", file=sys.stderr)
        sys.exit(1)
    tid, desc, _ = tasks[idx]
    tasks.pop(idx)
    write_tasks(tasks)
    print(f"Removed task {tid}: {desc}")


def cmd_clear(tasks: list[tuple[int, str, bool]]) -> None:
    """Remove all completed tasks from the list."""
    done_task_ids = [tid for tid, _, done in tasks if done]
    if not done_task_ids:
        print("No completed tasks to clear")
        return
    tasks[:] = [(tid, desc, done) for tid, desc, done in tasks if not done]
    write_tasks(tasks)
    count = len(done_task_ids)
    print(f"Cleared {count} completed task{'s' if count != 1 else ''}")


def main() -> None:
    """Parse arguments, load tasks, and dispatch to the requested command."""
    args = parse_args()

    # No action flag given — print usage
    if not (
        args.show
        or args.add is not None
        or args.done is not None
        or args.rm is not None
        or args.clear
    ):
        PARSER.print_usage()
        sys.exit(1)

    ensure_file()
    tasks = read_tasks()

    if args.show:
        cmd_show(tasks)
    elif args.add is not None:
        cmd_add(tasks, args.add)
    elif args.done is not None:
        cmd_done(tasks, args.done)
    elif args.rm is not None:
        cmd_rm(tasks, args.rm)
    elif args.clear:
        cmd_clear(tasks)


if __name__ == "__main__":
    main()
