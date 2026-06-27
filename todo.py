#!/usr/bin/env python3
"""Markdown-based to-do tracker.

Usage:
  python todo.py                    # show all tasks
  python todo.py --show             # show all tasks
  python todo.py --add "buy milk"   # add a new task
  python todo.py --done 1           # mark task 1 as done
  python todo.py --rm 2             # delete task 2
  python todo.py --clear            # remove all done tasks
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TODO_PATH = Path("TODO.md")
TODO_HEADER = "# Todo"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments using mutually exclusive groups."""
    parser = argparse.ArgumentParser(
        description="Manage a to-do list stored in TODO.md"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--show", action="store_true", help="show all tasks")
    group.add_argument("--add", metavar="TEXT", type=str, help="add a new task")
    group.add_argument("--done", metavar="ID", type=int, help="mark task as done")
    group.add_argument("--rm", metavar="ID", type=int, help="remove a task")
    group.add_argument("--clear", action="store_true", help="remove all done tasks")
    return parser.parse_args()


def ensure_file() -> bool:
    """Check if TODO.md exists and contains the # Todo header.

    Returns:
        True if the file exists and has the header, False otherwise.
    """
    if not TODO_PATH.exists():
        return False
    try:
        content = TODO_PATH.read_text(encoding="utf-8")
    except OSError as e:
        print(f"Error reading {TODO_PATH}: {e}", file=sys.stderr)
        sys.exit(1)
    return TODO_HEADER in content


def read_tasks() -> list[dict] | None:
    """Parse TODO.md and return a list of task dicts.

    Each task dict: {"id": int, "desc": str, "done": bool}.

    Returns:
        List of task dicts, or None if the file/header is missing.
    """
    if not ensure_file():
        return None
    try:
        content = TODO_PATH.read_text(encoding="utf-8")
    except OSError as e:
        print(f"Error reading {TODO_PATH}: {e}", file=sys.stderr)
        sys.exit(1)

    tasks: list[dict] = []
    pattern = re.compile(r"^- \[([ x])\] (\d+)\. (.+)$")
    for line in content.splitlines():
        m = pattern.match(line)
        if m:
            tasks.append({
                "id": int(m.group(2)),
                "desc": m.group(3),
                "done": m.group(1) == "x",
            })
    return tasks


def write_tasks(tasks: list[dict]) -> None:
    """Write the # Todo header and task list to TODO.md.

    Args:
        tasks: List of task dicts to write.
    """
    lines = [TODO_HEADER, ""]
    # Sort by id for deterministic output
    for t in sorted(tasks, key=lambda x: x["id"]):
        checkbox = "x" if t["done"] else " "
        lines.append(f"- [{checkbox}] {t['id']}. {t['desc']}")
    try:
        TODO_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except OSError as e:
        print(f"Error writing {TODO_PATH}: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_show(tasks: list[dict]) -> None:
    """Display all tasks grouped by status."""
    if not tasks:
        print("No tasks")
        return

    pending = [t for t in tasks if not t["done"]]
    done = [t for t in tasks if t["done"]]

    if pending:
        print("Pending:")
        for t in pending:
            print(f"  {t['id']}. {t['desc']}")

    if done:
        if pending:
            print()
        print("Done:")
        for t in done:
            print(f"  {t['id']}. {t['desc']}")


def cmd_add(tasks: list[dict], text: str) -> list[dict]:
    """Add a new task and return the updated list."""
    next_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({"id": next_id, "desc": text, "done": False})
    print(f"Added task {next_id}")
    return tasks


def cmd_done(tasks: list[dict], task_id: int) -> list[dict]:
    """Mark a task as completed. Exits with code 1 if not found."""
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            print(f"Task {task_id} marked as done")
            return tasks
    print(f"Task {task_id} not found", file=sys.stderr)
    sys.exit(1)


def cmd_rm(tasks: list[dict], task_id: int) -> list[dict]:
    """Remove a task. Exits with code 1 if not found."""
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            del tasks[i]
            print(f"Removed task {task_id}")
            return tasks
    print(f"Task {task_id} not found", file=sys.stderr)
    sys.exit(1)


def cmd_clear(tasks: list[dict]) -> list[dict]:
    """Remove all completed tasks."""
    kept = [t for t in tasks if not t["done"]]
    removed = len(tasks) - len(kept)
    if removed:
        print(f"Cleared {removed} done task{'s' if removed != 1 else ''}")
    else:
        print("No done tasks to clear")
    return kept


def main() -> None:
    """Parse args, read/write tasks, and dispatch to the appropriate command."""
    args = parse_args()

    # Determine if the command is a write operation
    is_write = args.add is not None or args.done is not None or args.rm is not None or args.clear

    tasks = read_tasks()

    if tasks is None and not is_write:
        # Read-only command with no file/header
        print("No tasks")
        return

    if tasks is None:
        # Write command with no file/header — initialise empty
        tasks = []

    # Dispatch
    if args.add is not None:
        tasks = cmd_add(tasks, args.add)
    elif args.done is not None:
        tasks = cmd_done(tasks, args.done)
    elif args.rm is not None:
        tasks = cmd_rm(tasks, args.rm)
    elif args.clear:
        tasks = cmd_clear(tasks)
    else:
        # Default / --show
        cmd_show(tasks)
        return  # read-only, no write back

    write_tasks(tasks)


if __name__ == "__main__":
    main()
