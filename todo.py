#!/usr/bin/env python3
"""Markdown-based to-do tracker.

Usage:
    python todo.py                  Show all tasks (alias for --show)
    python todo.py --show           Show all tasks
    python todo.py --add "task"     Add a new task
    python todo.py --done <id>      Mark a task as completed
    python todo.py --rm <id>        Remove a task
    python todo.py --clear          Remove all completed tasks

Tasks are stored in TODO.md using GitHub-Flavored Markdown checklist syntax.
"""

import argparse
import re
import sys
from pathlib import Path

TASK_RE = re.compile(r"^- \[([ x])\] (\d+)\. (.+)$")
HEADER = "# Todo"
TODO_FILE = Path("TODO.md")


# ── Helpers ──────────────────────────────────────────────────────────────────


def find_next_id(lines: list[str]) -> int:
    """Return the next available task id (max existing id + 1, or 1)."""
    max_id = 0
    for line in lines:
        m = TASK_RE.match(line)
        if m:
            max_id = max(max_id, int(m.group(2)))
    return max_id + 1


def parse_tasks(lines: list[str]) -> list[dict]:
    """Return a list of task dicts with keys: id, status, text."""
    tasks: list[dict] = []
    for line in lines:
        m = TASK_RE.match(line)
        if m:
            tasks.append({
                "id": int(m.group(2)),
                "done": m.group(1) == "x",
                "text": m.group(3),
            })
    return tasks


def read_todo(path: Path) -> list[str]:
    """Read file, return lines.  Missing file → empty list."""
    try:
        return path.read_text().splitlines(keepends=True)
    except FileNotFoundError:
        return []


def write_todo(path: Path, lines: list[str]) -> None:
    """Write lines to disk."""
    path.write_text("".join(lines))


# ── Commands ─────────────────────────────────────────────────────────────────


def cmd_show(path: Path) -> bool:
    """Print all tasks or 'No tasks'.  Return True on success."""
    lines = read_todo(path)
    tasks = parse_tasks(lines)
    if not tasks:
        print("No tasks")
        return True

    for t in tasks:
        status = "x" if t["done"] else " "
        print(f"[{status}] {t['id']}. {t['text']}")
    return True


def cmd_add(path: Path, text: str) -> bool:
    """Append a new task.  Create file with header if missing."""
    lines = read_todo(path)

    # Ensure header exists as first line
    if not lines or not lines[0].rstrip("\n\r") == HEADER:
        lines = [HEADER + "\n", "\n"]

    # Ensure blank line after header
    if len(lines) == 1 or lines[1].strip():
        lines.insert(1, "\n")

    next_id = find_next_id(lines)
    lines.append(f"- [ ] {next_id}. {text}\n")
    write_todo(path, lines)
    return True


def cmd_done(path: Path, task_id: int) -> bool:
    """Mark a task as completed.  Print error if not found."""
    lines = read_todo(path)
    if not lines:
        print(f"Task {task_id} not found", file=sys.stderr)
        return False

    found = False
    for i, line in enumerate(lines):
        m = TASK_RE.match(line)
        if m and int(m.group(2)) == task_id:
            lines[i] = f"- [x] {m.group(2)}. {m.group(3)}\n"
            found = True
            break

    if not found:
        print(f"Task {task_id} not found", file=sys.stderr)
        return False

    write_todo(path, lines)
    return True


def cmd_rm(path: Path, task_id: int) -> bool:
    """Remove a task line entirely.  Print error if not found."""
    lines = read_todo(path)
    if not lines:
        print(f"Task {task_id} not found", file=sys.stderr)
        return False

    found = False
    for i, line in enumerate(lines):
        m = TASK_RE.match(line)
        if m and int(m.group(2)) == task_id:
            lines.pop(i)
            found = True
            break

    if not found:
        print(f"Task {task_id} not found", file=sys.stderr)
        return False

    write_todo(path, lines)
    return True


def cmd_clear(path: Path) -> bool:
    """Remove all completed tasks (lines matching - [x] ...)."""
    lines = read_todo(path)
    if not lines:
        return True

    cleaned = [line for line in lines if not TASK_RE.match(line) or line.startswith("- [ ]")]
    write_todo(path, cleaned)
    return True


# ── CLI ──────────────────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    """Configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Markdown-based to-do tracker.",
    )
    parser.add_argument(
        "--show", action="store_true", help="Show all tasks",
    )
    parser.add_argument(
        "--add", metavar="TEXT", help="Add a new task",
    )
    parser.add_argument(
        "--done", metavar="ID", type=int, help="Mark a task as completed",
    )
    parser.add_argument(
        "--rm", metavar="ID", type=int, dest="remove", help="Remove a task",
    )
    parser.add_argument(
        "--clear", action="store_true", help="Remove all completed tasks",
    )
    return parser


def main() -> None:
    """Parse arguments and dispatch to the appropriate command."""
    parser = build_parser()
    args = parser.parse_args()

    path = TODO_FILE

    try:
        # Default: --show when no args
        if not any([args.show, args.add, args.done is not None,
                    args.remove is not None, args.clear]):
            cmd_show(path)
            return

        if args.show:
            cmd_show(path)
        elif args.add is not None:
            cmd_add(path, args.add)
        elif args.done is not None:
            if not cmd_done(path, args.done):
                sys.exit(1)
        elif args.remove is not None:
            if not cmd_rm(path, args.remove):
                sys.exit(1)
        elif args.clear:
            cmd_clear(path)
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
