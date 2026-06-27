#!/usr/bin/env python3
"""A markdown-based to-do tracker.

Usage:
    python todo.py                    Show all tasks (same as --show)
    python todo.py --show             List pending + completed tasks with IDs
    python todo.py --add "buy milk"   Append a new pending task
    python todo.py --done 2           Mark task 2 as completed
    python todo.py --rm 1             Remove task 1 entirely
    python todo.py --clear            Remove all completed tasks

Storage: TODO.md in the working directory.
Dependencies: None (stdlib only: argparse, re, pathlib, sys).
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

TODO_FILE = Path("TODO.md")
TASK_RE = re.compile(r"^- \[( |x)\] (\d+)\.\s*(.+)$")


@dataclass
class Task:
    """A single to-do item."""

    task_id: int
    description: str
    done: bool


# ── I/O ────────────────────────────────────────────────────────────────


def load_tasks(path: Path) -> "List[Task]":
    """Parse TODO.md and return an ordered list of tasks.

    Returns [] if the file is missing, empty, or contains no parseable
    task lines (never raises).
    """
    if not path.exists():
        return []

    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []

    tasks: "List[Task]" = []
    for line in text.splitlines():
        m = TASK_RE.match(line)
        if m:
            tasks.append(
                Task(
                    task_id=int(m.group(2)),
                    description=m.group(3),
                    done=(m.group(1) == "x"),
                )
            )
    return tasks


def save_tasks(path: Path, tasks: "List[Task]") -> None:
    """Serialize tasks to TODO.md with a '# Todo' header."""
    lines = ["# Todo", ""]
    for t in tasks:
        checkbox = "x" if t.done else " "
        lines.append(f"- [{checkbox}] {t.task_id}. {t.description}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


# ── Helpers ────────────────────────────────────────────────────────────


def next_task_id(tasks: "List[Task]") -> int:
    """Return the largest existing task ID + 1 (or 1 if tasks is empty)."""
    if not tasks:
        return 1
    return max(t.task_id for t in tasks) + 1


def format_tasks(tasks: "List[Task]") -> str:
    """Format tasks for display: pending and done sections."""
    if not tasks:
        return "No tasks"

    pending = [t for t in tasks if not t.done]
    done = [t for t in tasks if t.done]

    parts: list[str] = []
    if pending:
        parts.append("Pending:")
        for t in pending:
            parts.append(f"  - [ ] {t.task_id}. {t.description}")

    if done:
        if parts:
            parts.append("")
        parts.append("Done:")
        for t in done:
            parts.append(f"  - [x] {t.task_id}. {t.description}")

    return "\n".join(parts)


# ── Actions ────────────────────────────────────────────────────────────


def add_task(tasks: "List[Task]", text: str) -> "List[Task]":
    """Append a new pending task with an auto-incremented ID."""
    tid = next_task_id(tasks)
    tasks.append(Task(task_id=tid, description=text, done=False))
    return tasks


def mark_done(tasks: "List[Task]", task_id: int) -> "List[Task]":
    """Set a task's done flag to True. Raises ValueError if not found."""
    for t in tasks:
        if t.task_id == task_id:
            t.done = True
            return tasks
    raise ValueError(task_id)


def remove_task(tasks: "List[Task]", task_id: int) -> "List[Task]":
    """Remove a task by ID. Raises ValueError if not found."""
    for i, t in enumerate(tasks):
        if t.task_id == task_id:
            tasks.pop(i)
            return tasks
    raise ValueError(task_id)


def clear_done(tasks: "List[Task]") -> "List[Task]":
    """Filter out all completed tasks."""
    return [t for t in tasks if not t.done]


# ── CLI ────────────────────────────────────────────────────────────────


def parse_args(argv: "Optional[List[str]]" = None) -> argparse.Namespace:
    """Build and parse the command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Markdown-based to-do tracker.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show all tasks (default when no other flag given)",
    )
    parser.add_argument("--add", type=str, help="Add a new task")
    parser.add_argument(
        "--done",
        type=int,
        metavar="ID",
        help="Mark a task as completed (by ID)",
    )
    parser.add_argument(
        "--rm",
        type=int,
        metavar="ID",
        help="Remove a task (by ID)",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Remove all completed tasks",
    )
    return parser.parse_args(argv)


def main(argv: "Optional[List[str]]" = None) -> None:
    """Parse arguments, dispatch to the requested action, print output.

    Exits with code 1 on error (bad ID, multiple actions, I/O failure).
    """
    args = parse_args(argv)

    # Count how many action flags were provided
    actions = [args.show, args.add is not None, args.done is not None,
               args.rm is not None, args.clear]
    action_count = sum(1 for a in actions if a)

    if action_count > 1:
        print("error: only one action flag may be used per invocation",
              file=sys.stderr)
        sys.exit(1)

    # Default to --show
    show_mode = action_count == 0 or args.show

    # Load tasks (file missing → empty list, never raises here)
    try:
        tasks = load_tasks(TODO_FILE)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    dispatch = False

    if args.add is not None:
        tasks = add_task(tasks, args.add)
        dispatch = True

    if args.done is not None:
        try:
            tasks = mark_done(tasks, args.done)
        except ValueError:
            print(f"Task {args.done} not found", file=sys.stderr)
            sys.exit(1)
        dispatch = True

    if args.rm is not None:
        try:
            tasks = remove_task(tasks, args.rm)
        except ValueError:
            print(f"Task {args.rm} not found", file=sys.stderr)
            sys.exit(1)
        dispatch = True

    if args.clear:
        tasks = clear_done(tasks)
        dispatch = True

    # Persist if any write action was performed
    if dispatch:
        try:
            save_tasks(TODO_FILE, tasks)
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            sys.exit(1)

    # Show tasks (default, or explicit --show)
    if show_mode:
        print(format_tasks(tasks))


if __name__ == "__main__":
    main()
