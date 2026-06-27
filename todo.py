#!/usr/bin/env python3
"""A simple to-do tracker that stores tasks in a markdown file.

Usage:
    python todo.py                     Show all tasks
    python todo.py --show              Show all tasks
    python todo.py --add "buy milk"    Add a new pending task
    python todo.py --done 3            Mark task 3 as done
    python todo.py --rm 2              Remove task 2
    python todo.py --clear             Remove all completed tasks

Tasks are stored in TODO.md with checkboxes:
    - [ ] 1. buy milk
    - [x] 2. call mom
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

__version__ = "0.1.0"

TODO_FILE = Path("TODO.md")
HEADER = "# Todo"

# Regex for a task line: "- [ ] <id>. <description>" or "- [x] <id>. <description>"
_TASK_RE = re.compile(r"^- \[([ x])\] (\d+)\. (.+)$")


def _todo_path() -> Path:
    """Return the path to the TODO.md file."""
    return TODO_FILE


def _ensure_header() -> None:
    """Create TODO.md with the # Todo header if it doesn't exist."""
    path = _todo_path()
    if not path.exists():
        path.write_text(HEADER + "\n\n", encoding="utf-8")


def _parse_tasks(content: str) -> list[tuple[int, str, str]]:
    """Parse TODO.md content into (id, status, description) tuples.

    Status is ``' '`` for pending or ``'x'`` for done.
    Lines that don't match the task pattern are ignored.
    """
    tasks: list[tuple[int, str, str]] = []
    for line in content.splitlines():
        m = _TASK_RE.match(line)
        if m:
            tasks.append((int(m.group(2)), m.group(1), m.group(3)))
    return tasks


def _render_tasks(tasks: list[tuple[int, str, str]]) -> str:
    """Render tasks back into TODO.md content."""
    lines = [HEADER, ""]
    for task_id, status, desc in tasks:
        lines.append(f"- [{status}] {task_id}. {desc}")
    if not tasks:
        lines.append("")
    return "\n".join(lines) + "\n" if tasks else "\n".join(lines)


def _max_id(tasks: list[tuple[int, str, str]]) -> int:
    """Return the largest task id, or 0 if the list is empty."""
    return max((tid for tid, _, _ in tasks), default=0)


def _read_todo() -> str:
    """Read the entire TODO.md file content."""
    return _todo_path().read_text(encoding="utf-8")


def _write_todo(content: str) -> None:
    """Write *content* to TODO.md."""
    _todo_path().write_text(content, encoding="utf-8")


def _find_task_index(tasks: list[tuple[int, str, str]], task_id: int) -> Optional[int]:
    """Return the index of the task with *task_id*, or ``None``."""
    for i, (tid, _, _) in enumerate(tasks):
        if tid == task_id:
            return i
    return None


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_show() -> None:
    """Print all tasks, or *No tasks* if the list is empty."""
    _ensure_header()
    content = _read_todo()
    tasks = _parse_tasks(content)
    if not tasks:
        print("No tasks")
        return
    for task_id, status, desc in tasks:
        print(f"  - [{status}] {task_id}. {desc}")


def cmd_add(text: str) -> None:
    """Add a new pending task with description *text*."""
    _ensure_header()
    content = _read_todo()
    tasks = _parse_tasks(content)
    new_id = _max_id(tasks) + 1
    tasks.append((new_id, " ", text))
    _write_todo(_render_tasks(tasks))


def cmd_done(task_id: int) -> None:
    """Mark task *task_id* as completed (toggle ``[ ]`` → ``[x]``)."""
    _ensure_header()
    content = _read_todo()
    tasks = _parse_tasks(content)
    idx = _find_task_index(tasks, task_id)
    if idx is None:
        print(f"Task {task_id} not found")
        sys.exit(1)
    tid, status, desc = tasks[idx]
    if status == "x":
        # Already done — no-op
        return
    tasks[idx] = (tid, "x", desc)
    _write_todo(_render_tasks(tasks))


def cmd_rm(task_id: int) -> None:
    """Remove task *task_id* from the file entirely."""
    _ensure_header()
    content = _read_todo()
    tasks = _parse_tasks(content)
    idx = _find_task_index(tasks, task_id)
    if idx is None:
        print(f"Task {task_id} not found")
        sys.exit(1)
    tasks.pop(idx)
    _write_todo(_render_tasks(tasks))


def cmd_clear() -> None:
    """Remove all completed tasks (lines with ``[x]``)."""
    _ensure_header()
    content = _read_todo()
    tasks = _parse_tasks(content)
    pending = [(tid, status, desc) for tid, status, desc in tasks if status != "x"]
    _write_todo(_render_tasks(pending))


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Parse command-line arguments and dispatch to the matching command."""
    parser = argparse.ArgumentParser(
        description="Manage a to-do list stored in TODO.md",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--show",
        action="store_true",
        help="Show all tasks (default when no flag is given)",
    )
    group.add_argument(
        "--add",
        type=str,
        metavar="TEXT",
        help="Add a new pending task with the given description",
    )
    group.add_argument(
        "--done",
        type=int,
        metavar="ID",
        help="Mark a task as done by its numeric ID",
    )
    group.add_argument(
        "--rm",
        type=int,
        metavar="ID",
        help="Remove a task by its numeric ID",
    )
    group.add_argument(
        "--clear",
        action="store_true",
        help="Remove all completed tasks",
    )

    args = parser.parse_args()

    try:
        if args.add is not None:
            cmd_add(args.add)
        elif args.done is not None:
            cmd_done(args.done)
        elif args.rm is not None:
            cmd_rm(args.rm)
        elif args.clear:
            cmd_clear()
        else:
            # Default (no flag or --show)
            cmd_show()
    except (OSError, PermissionError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
