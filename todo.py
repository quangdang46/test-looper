#!/usr/bin/env python3
"""Markdown-based to-do tracker.

Tasks are stored in TODO.md using GitHub-flavored markdown checkboxes.
Each task has a unique integer ID that auto-increments and is never reused.

Usage:
    python todo.py                    # Show all tasks
    python todo.py --show             # Show all tasks
    python todo.py --add "buy milk"   # Add a new task
    python todo.py --done 1           # Mark task 1 as completed
    python todo.py --rm 1             # Remove task 1
    python todo.py --clear            # Remove all completed tasks
    python todo.py --help             # Show this help message
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional

TODO_PATH = Path("TODO.md")

# Regex to match a task line: "- [ ] N. description" or "- [x] N. description"
_TASK_RE = re.compile(r"^- \[([ xX])\] (\d+)\. (.+)$")


# ---------------------------------------------------------------------------
# Parsing & Rendering
# ---------------------------------------------------------------------------

def _parse_tasks(lines: List[str]) -> list[dict]:
    """Parse a list of markdown lines into task dicts.

    Returns a list of ``{"id": int, "done": bool, "text": str}`` dicts
    sorted by id.  Non-matching lines are silently skipped.
    """
    tasks: list[dict] = []
    for line in lines:
        m = _TASK_RE.match(line)
        if m:
            done = m.group(1) in ("x", "X")
            tasks.append({
                "id": int(m.group(2)),
                "done": done,
                "text": m.group(3),
            })
    tasks.sort(key=lambda t: t["id"])
    return tasks


def _render_tasks(tasks: list[dict]) -> str:
    """Render a list of task dicts back into markdown."""
    lines = ["# Todo", ""]
    for t in tasks:
        checkbox = "x" if t["done"] else " "
        lines.append(f"- [{checkbox}] {t['id']}. {t['text']}")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def _read_todo() -> Optional[list[dict]]:
    """Read tasks from *TODO.md*.

    Returns ``None`` when the file does not exist.
    Returns an empty list when the file exists but has no tasks or header.
    Exits on I/O errors.
    """
    if not TODO_PATH.exists():
        return None
    try:
        raw = TODO_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Error reading TODO.md: {exc}", file=sys.stderr)
        sys.exit(1)

    lines = raw.splitlines()

    # Treat empty file or missing header as empty task list.
    if not lines or lines[0].strip() != "# Todo":
        return []

    return _parse_tasks(lines)


def _write_todo(tasks: list[dict]) -> None:
    """Write tasks to *TODO.md*.  Exits on I/O errors."""
    content = _render_tasks(tasks)
    try:
        TODO_PATH.write_text(content, encoding="utf-8")
    except OSError as exc:
        print(f"Error writing TODO.md: {exc}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_show(tasks: Optional[list[dict]]) -> None:
    """Display all tasks."""
    if tasks is None:
        # File didn't exist — create it and report empty.
        _write_todo([])
        print("No tasks")
        return
    if not tasks:
        print("No tasks")
        return
    for t in tasks:
        status = "x" if t["done"] else " "
        print(f"{t['id']}. [{status}] {t['text']}")


def cmd_add(tasks: Optional[list[dict]], text: str) -> None:
    """Add a new task."""
    if tasks is None:
        tasks = []
    next_id = max(t["id"] for t in tasks) + 1 if tasks else 1
    tasks.append({"id": next_id, "done": False, "text": text})
    _write_todo(tasks)
    print(f"Added task {next_id}: {text}")


def _find_task(tasks: Optional[list[dict]], task_id: int) -> Optional[int]:
    """Return the index of a task by id, or ``None`` if not found."""
    if tasks is None:
        return None
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            return i
    return None


def cmd_done(tasks: Optional[list[dict]], task_id: int) -> None:
    """Mark a task as completed."""
    idx = _find_task(tasks, task_id)
    if idx is None:
        print(f"Task {task_id} not found")
        return
    tasks[idx]["done"] = True  # type: ignore[index]
    _write_todo(tasks)  # type: ignore[arg-type]
    print(f"Task {task_id} marked as done")


def cmd_rm(tasks: Optional[list[dict]], task_id: int) -> None:
    """Remove a task."""
    idx = _find_task(tasks, task_id)
    if idx is None:
        print(f"Task {task_id} not found")
        return
    tasks.pop(idx)  # type: ignore[union-attr]
    _write_todo(tasks)  # type: ignore[arg-type]
    print(f"Removed task {task_id}")


def cmd_clear(tasks: Optional[list[dict]]) -> None:
    """Remove all completed tasks."""
    if tasks is None:
        tasks = []
    done_count = sum(1 for t in tasks if t["done"])
    if done_count == 0:
        print("No completed tasks to clear")
        return
    tasks[:] = [t for t in tasks if not t["done"]]
    _write_todo(tasks)
    plural = "s" if done_count > 1 else ""
    print(f"Cleared {done_count} completed task{plural}")


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    """Parse CLI args and dispatch to the appropriate command."""
    parser = argparse.ArgumentParser(
        description="Markdown-based to-do tracker. Tasks stored in TODO.md."
    )
    parser.add_argument(
        "--show", action="store_true", help="Show all tasks"
    )
    parser.add_argument(
        "--add", type=str, help="Add a new task with the given description"
    )
    parser.add_argument(
        "--done", type=int, help="Mark a task as completed by its ID"
    )
    parser.add_argument(
        "--rm", type=int, help="Remove a task by its ID"
    )
    parser.add_argument(
        "--clear", action="store_true", help="Remove all completed tasks"
    )
    args = parser.parse_args()

    # Priority order: --add > --done > --rm > --clear > --show / default
    if args.add is not None:
        tasks = _read_todo()
        cmd_add(tasks, args.add)
    elif args.done is not None:
        tasks = _read_todo()
        cmd_done(tasks, args.done)
    elif args.rm is not None:
        tasks = _read_todo()
        cmd_rm(tasks, args.rm)
    elif args.clear:
        tasks = _read_todo()
        cmd_clear(tasks)
    else:
        tasks = _read_todo()
        cmd_show(tasks)


if __name__ == "__main__":
    main()
