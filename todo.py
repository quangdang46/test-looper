#!/usr/bin/env python3
"""Markdown-based to-do tracker.

Usage:
    python todo.py              # Show all tasks (same as --show)
    python todo.py --show       # Show all tasks
    python todo.py --add "buy milk"   # Add a new task
    python todo.py --done 1     # Mark task 1 as done
    python todo.py --rm 1       # Remove task 1 entirely
    python todo.py --clear      # Remove all completed tasks

Tasks are stored in TODO.md in the current directory.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FILE = Path("TODO.md")
HEADER = "# Todo\n\n"
TASK_RE = re.compile(r"^- \[([ x])\] (\d+)\.\s*(.+)$", re.MULTILINE)

# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------


def parse_tasks(text: str) -> list[dict]:
    """Parse raw TODO.md text into a list of task dicts.

    Each task dict has keys: id (int), desc (str), done (bool).
    Lines that don't match the expected pattern are skipped.
    Returns [] for empty or header-only content.
    """
    tasks: list[dict] = []
    for match in TASK_RE.finditer(text):
        status, raw_id, desc = match.groups()
        tasks.append(
            {
                "id": int(raw_id),
                "desc": desc.strip(),
                "done": status == "x",
            }
        )
    return tasks


def format_tasks(tasks: list[dict]) -> str:
    """Format a list of task dicts back into markdown string.

    Always prepends HEADER so the result is ready to write to TODO.md.
    """
    lines: list[str] = ["# Todo", ""]
    for t in tasks:
        checkbox = "x" if t["done"] else " "
        lines.append(f"- [{checkbox}] {t['id']}. {t['desc']}")
    if tasks:
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------


def load_tasks() -> list[dict]:
    """Read tasks from TODO.md on disk.

    If the file does not exist, create it with HEADER and return [].

    Returns [] for files with no content or no '# Todo' header.
    """
    if not FILE.exists():
        FILE.write_text(HEADER, encoding="utf-8")
        return []

    raw = FILE.read_text(encoding="utf-8")
    if not raw.strip() or "# Todo" not in raw:
        return []

    return parse_tasks(raw)


def write_tasks(tasks: list[dict]) -> None:
    """Format and write tasks to TODO.md."""
    FILE.write_text(format_tasks(tasks), encoding="utf-8")


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------


def show_tasks(tasks: list[dict]) -> None:
    """Pretty-print tasks to stdout."""
    if not tasks:
        print("No tasks")
        return

    for t in tasks:
        status = "x" if t["done"] else " "
        print(f"- [{status}] {t['id']}. {t['desc']}")


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------


def _next_id(tasks: list[dict]) -> int:
    """Compute the next available task id."""
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


def add_task(tasks: list[dict], desc: str) -> list[dict]:
    """Append a new task with an auto-incremented id.

    Returns the updated task list (new list, not in-place).
    """
    new_id = _next_id(tasks)
    new_task = {"id": new_id, "desc": desc, "done": False}
    return [*tasks, new_task]


def done_task(tasks: list[dict], task_id: int) -> list[dict]:
    """Mark a task as done. Raises LookupError if task_id is not found."""
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            return tasks
    raise LookupError(f"Task {task_id} not found")


def remove_task(tasks: list[dict], task_id: int) -> list[dict]:
    """Remove a task entirely. Raises LookupError if task_id is not found."""
    for t in tasks:
        if t["id"] == task_id:
            tasks.remove(t)
            return tasks
    raise LookupError(f"Task {task_id} not found")


def clear_done(tasks: list[dict]) -> list[dict]:
    """Filter out all completed tasks."""
    return [t for t in tasks if not t["done"]]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Markdown-based to-do tracker",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--show",
        action="store_true",
        default=False,
        help="Show all tasks (default if no other flag given)",
    )
    group.add_argument("--add", type=str, help="Add a new task")
    group.add_argument("--done", type=int, help="Mark a task as completed")
    group.add_argument("--rm", type=int, help="Remove a task")
    group.add_argument("--clear", action="store_true", help="Remove all completed tasks")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Entry point: parse args, load tasks, dispatch, write back."""
    args = parse_args(argv)

    # Default to --show when no flags are passed
    flags = [args.show, args.add is not None, args.done is not None, args.rm is not None, args.clear]
    if not any(flags):
        args.show = True

    # Validation
    if args.add is not None and not args.add.strip():
        sys.stderr.write("Error: Task description cannot be empty\n")
        sys.exit(1)

    try:
        tasks = load_tasks()
    except (OSError, PermissionError) as exc:
        sys.stderr.write(f"Error reading TODO.md: {exc}\n")
        sys.exit(1)

    try:
        if args.show:
            show_tasks(tasks)
        elif args.add is not None:
            tasks = add_task(tasks, args.add.strip())
            write_tasks(tasks)
            print(f"Added task: {args.add.strip()}")
        elif args.done is not None:
            tasks = done_task(tasks, args.done)
            write_tasks(tasks)
            print(f"Completed task {args.done}")
        elif args.rm is not None:
            tasks = remove_task(tasks, args.rm)
            write_tasks(tasks)
            print(f"Removed task {args.rm}")
        elif args.clear:
            before = len(tasks)
            tasks = clear_done(tasks)
            cleared = before - len(tasks)
            write_tasks(tasks)
            print(f"Cleared {cleared} completed task(s)")
    except LookupError as exc:
        sys.stderr.write(f"Error: {exc}\n")
        sys.exit(1)
    except (OSError, PermissionError) as exc:
        sys.stderr.write(f"Error writing TODO.md: {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
