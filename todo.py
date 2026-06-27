#!/usr/bin/env python3
"""Markdown-based to-do tracker.

Manages a simple to-do list stored in TODO.md using GitHub-flavoured
markdown checkboxes.  Only the Python standard library is used.

Usage:
    python todo.py              Show all tasks (same as --show)
    python todo.py --show       Show all tasks
    python todo.py --add TEXT   Add a new task
    python todo.py --done ID    Mark a task as completed
    python todo.py --rm ID      Remove a task
    python todo.py --clear      Remove all completed tasks
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

TODO_FILE = Path("TODO.md")

# Regex patterns
_TASK_RE = re.compile(r"^- \[([ x])\] (\d+)\. (.+)$")
_LAST_ID_RE = re.compile(r"<!-- last_id:\s*(\d+)\s*-->")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Task:
    """A single to-do item."""

    task_id: int
    text: str
    done: bool = False


@dataclass
class TodoFile:
    """In-memory representation of a TODO.md file."""

    header: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)
    footer: list[str] = field(default_factory=list)
    last_id: int = 0


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def read_todo() -> TodoFile:
    """Parse TODO.md into a ``TodoFile``.

    If the file does not exist it is automatically created with the
    ``# Todo`` header.  If it exists but lacks that header an empty
    ``TodoFile`` is returned so callers can treat it as "no tasks".
    """
    if not TODO_FILE.exists():
        TODO_FILE.write_text("# Todo\n\n")
        return TodoFile(header=["# Todo\n", "\n"])

    lines = TODO_FILE.read_text().splitlines(keepends=True)
    result = TodoFile()
    found_header = False
    in_task_section = False

    for line in lines:
        if not found_header and line.strip() == "# Todo":
            found_header = True
            result.header.append(line)
            continue

        m = _TASK_RE.match(line)
        if m:
            in_task_section = True
            result.tasks.append(
                Task(
                    task_id=int(m.group(2)),
                    text=m.group(3),
                    done=m.group(1) == "x",
                )
            )
        elif in_task_section:
            result.footer.append(line)
        else:
            result.header.append(line)

    if not found_header:
        return TodoFile()

    # Extract last_id from footer if present
    for line in result.footer:
        m = _LAST_ID_RE.match(line.strip())
        if m:
            result.last_id = int(m.group(1))
            break

    return result


def write_todo(tf: TodoFile) -> None:
    """Serialize a ``TodoFile`` back to TODO.md."""
    lines = list(tf.header)
    for t in tf.tasks:
        checkbox = "x" if t.done else " "
        lines.append(f"- [{checkbox}] {t.task_id}. {t.text}\n")
    # Keep footer lines, dropping any stale last-id tag
    for line in tf.footer:
        if _LAST_ID_RE.match(line.strip()):
            continue
        lines.append(line)
    # Ensure a trailing newline before the tag
    if not lines or lines[-1] != "\n":
        lines.append("\n")
    lines.append(f"<!-- last_id: {tf.last_id} -->\n")
    TODO_FILE.write_text("".join(lines))


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _next_id(tasks: list[Task], last_id: int) -> int:
    """Return the next auto-increment ID (deleted IDs are never reused)."""
    return max((t.task_id for t in tasks), default=last_id) + 1


def _find(tasks: list[Task], task_id: int) -> Optional[int]:
    """Return the index of *task_id* in *tasks*, or ``None``."""
    for i, t in enumerate(tasks):
        if t.task_id == task_id:
            return i
    return None


# ---------------------------------------------------------------------------
# Command implementations
# ---------------------------------------------------------------------------

def cmd_show(tf: TodoFile) -> None:
    """Print pending then completed tasks."""
    if not tf.tasks:
        print("No tasks")
        return

    pending = [t for t in tf.tasks if not t.done]
    done = [t for t in tf.tasks if t.done]

    if pending:
        print("Pending:")
        for t in pending:
            print(f"  {t.task_id}. {t.text}")

    if pending and done:
        print()

    if done:
        print("Done:")
        for t in done:
            print(f"  {t.task_id}. {t.text}")


def cmd_add(tf: TodoFile, text: str) -> None:
    """Append a new pending task."""
    next_id = _next_id(tf.tasks, tf.last_id)
    tf.tasks.append(Task(task_id=next_id, text=text, done=False))
    tf.last_id = max(next_id, tf.last_id)
    write_todo(tf)


def cmd_done(tf: TodoFile, task_id: int) -> None:
    """Mark a task as completed."""
    idx = _find(tf.tasks, task_id)
    if idx is None:
        print(f"Task {task_id} not found", file=sys.stderr)
        sys.exit(1)
    tf.tasks[idx].done = True
    write_todo(tf)


def cmd_rm(tf: TodoFile, task_id: int) -> None:
    """Remove a task entirely from the list."""
    idx = _find(tf.tasks, task_id)
    if idx is None:
        print(f"Task {task_id} not found", file=sys.stderr)
        sys.exit(1)
    tf.tasks.pop(idx)
    write_todo(tf)


def cmd_clear(tf: TodoFile) -> None:
    """Remove all completed tasks from the list."""
    before = len(tf.tasks)
    tf.tasks = [t for t in tf.tasks if not t.done]
    if len(tf.tasks) < before:
        write_todo(tf)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Parse arguments and dispatch to the appropriate command."""
    parser = argparse.ArgumentParser(description="Markdown-based to-do tracker")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--show", action="store_true", help="Show all tasks")
    group.add_argument("--add", type=str, metavar="TEXT", help="Add a new task")
    group.add_argument("--done", type=int, metavar="ID", help="Mark a task as done")
    group.add_argument("--rm", type=int, metavar="ID", help="Remove a task")
    group.add_argument("--clear", action="store_true", help="Remove all done tasks")

    args = parser.parse_args()

    try:
        if args.add is not None:
            text = args.add.strip()
            if not text:
                print("Error: task text cannot be empty", file=sys.stderr)
                sys.exit(1)
            cmd_add(read_todo(), text)
        elif args.done is not None:
            cmd_done(read_todo(), args.done)
        elif args.rm is not None:
            cmd_rm(read_todo(), args.rm)
        elif args.clear:
            cmd_clear(read_todo())
        else:
            # Default: show
            cmd_show(read_todo())
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
