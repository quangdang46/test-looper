#!/usr/bin/env python3
"""Markdown-based to-do tracker.

Usage:
    python todo.py [--show]                    Display all tasks
    python todo.py --add "buy milk"            Add a new task
    python todo.py --done <id>                 Mark task as completed
    python todo.py --rm <id>                   Remove a task permanently
    python todo.py --clear                     Remove all completed tasks

Tasks are stored in TODO.md using standard markdown checkbox syntax.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional

TODO_FILENAME = "TODO.md"

# Regex for a task line: "- [ ] N. text" or "- [x] N. text"
_TASK_RE = re.compile(r"^-\s+\[([ x])\]\s+(\d+)\.\s+(.*)$")


def _parse_task(line: str, line_num: int) -> Optional[dict]:
    """Parse a single line as a task, or return None."""
    m = _TASK_RE.match(line)
    if not m:
        return None
    return {
        "line": line_num,
        "id": int(m.group(2)),
        "done": m.group(1) == "x",
        "text": m.group(3),
        "raw": line,
    }


def read_tasks(path: Path) -> List[dict]:
    """Read all tasks from TODO.md.

    Returns a list of task dicts.  Returns an empty list when the file
    does not exist or contains no task lines.
    """
    try:
        text = path.read_text()
    except FileNotFoundError:
        return []

    tasks: List[dict] = []
    for i, raw_line in enumerate(text.splitlines(keepends=True)):
        task = _parse_task(raw_line, i)
        if task is not None:
            tasks.append(task)
    return tasks


def _read_all_lines(path: Path) -> List[str]:
    """Read all raw lines from a file, or return [] if it doesn't exist."""
    try:
        text = path.read_text()
    except FileNotFoundError:
        return []
    return text.splitlines(keepends=True)


def _write_lines(path: Path, lines: List[str]) -> None:
    """Write a list of lines back to the file."""
    try:
        path.write_text("".join(lines))
    except PermissionError:
        print(f"Error: cannot write {TODO_FILENAME} — Permission denied", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error: cannot write {TODO_FILENAME} — {e}", file=sys.stderr)
        sys.exit(1)


def _ensure_header(lines: List[str]) -> List[str]:
    """Ensure the file starts with a ``# Todo`` header.

    If the file is empty or does not start with ``# Todo``, prepend the
    header.  Return the (possibly extended) line list.
    """
    if not lines or not lines[0].strip().startswith("# Todo"):
        return ["# Todo\n", "\n"] + lines
    return lines


def cmd_show(path: Path) -> None:
    """Print all tasks to stdout, or 'No tasks' if there are none."""
    tasks = read_tasks(path)
    if not tasks:
        print("No tasks")
        return
    for t in tasks:
        box = "[x]" if t["done"] else "[ ]"
        print(f"{box} {t['id']}. {t['text']}")


def cmd_add(path: Path, text: str) -> None:
    """Add a new task with the given description text."""
    tasks = read_tasks(path)
    next_id = max((t["id"] for t in tasks), default=0) + 1

    lines = _read_all_lines(path)
    lines = _ensure_header(lines)

    # Ensure trailing newline before appending
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"

    lines.append(f"- [ ] {next_id}. {text}\n")
    _write_lines(path, lines)


def cmd_done(path: Path, task_id: int) -> None:
    """Mark the task identified by *task_id* as completed."""
    lines = _read_all_lines(path)
    if not lines:
        print(f"Task {task_id} not found", file=sys.stderr)
        sys.exit(1)

    found = False
    for i, raw_line in enumerate(lines):
        task = _parse_task(raw_line, i)
        if task is not None and task["id"] == task_id:
            # Replace [ ] with [x]
            lines[i] = _TASK_RE.sub(r"- [x] \2. \3", raw_line)
            found = True
            break

    if not found:
        print(f"Task {task_id} not found", file=sys.stderr)
        sys.exit(1)

    _write_lines(path, lines)


def cmd_rm(path: Path, task_id: int) -> None:
    """Remove the task identified by *task_id* entirely."""
    lines = _read_all_lines(path)
    if not lines:
        print(f"Task {task_id} not found", file=sys.stderr)
        sys.exit(1)

    new_lines = []
    found = False
    for raw_line in lines:
        task = _parse_task(raw_line, len(new_lines))
        if task is not None and task["id"] == task_id:
            found = True
            continue  # skip this line
        new_lines.append(raw_line)

    if not found:
        print(f"Task {task_id} not found", file=sys.stderr)
        sys.exit(1)

    _write_lines(path, new_lines)


def cmd_clear(path: Path) -> None:
    """Remove all completed tasks from the file."""
    lines = _read_all_lines(path)
    if not lines:
        return

    new_lines = []
    for raw_line in lines:
        task = _parse_task(raw_line, len(new_lines))
        if task is not None and task["done"]:
            continue  # skip completed tasks
        new_lines.append(raw_line)

    _write_lines(path, new_lines)


def create_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Markdown-based to-do tracker.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display all tasks",
    )
    parser.add_argument(
        "--add",
        metavar="TEXT",
        help="Add a new task",
    )
    parser.add_argument(
        "--done",
        metavar="ID",
        type=int,
        help="Mark task <id> as completed",
    )
    parser.add_argument(
        "--rm",
        metavar="ID",
        type=int,
        help="Remove task <id> permanently",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Remove all completed tasks",
    )
    return parser


def main() -> None:
    """Parse arguments and dispatch to the appropriate command."""
    parser = create_parser()
    args = parser.parse_args()

    path = Path(TODO_FILENAME)

    # Single-action dispatch with defined precedence
    if args.add is not None:
        cmd_add(path, args.add)
    elif args.done is not None:
        cmd_done(path, args.done)
    elif args.rm is not None:
        cmd_rm(path, args.rm)
    elif args.clear:
        cmd_clear(path)
    else:
        cmd_show(path)


if __name__ == "__main__":
    main()
