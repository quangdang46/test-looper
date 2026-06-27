#!/usr/bin/env python3
"""todo.py — Markdown-based to-do list.

Store and manage tasks in TODO.md using GitHub-flavored markdown checkboxes.

Usage:
    python todo.py              Show tasks (default)
    python todo.py --show       Show all tasks
    python todo.py --add TEXT   Add a new task
    python todo.py --done ID    Mark a task as completed
    python todo.py --rm ID      Remove a task entirely
    python todo.py --clear      Remove all completed tasks
"""

import argparse
import re
import sys
from pathlib import Path

TODO_FILE = Path("TODO.md")
HEADER = "# Todo"
LAST_ID_RE = re.compile(r"<!--\s*last_id:\s*(\d+)\s*-->")
TASK_LINE_RE = re.compile(r"^- \[([ x])\] (\d+)\.\s+(.*)$")


def read_todo():
    """Parse TODO.md into (tasks, last_id).

    Each task is a dict with keys: id (int), done (bool), text (str).
    If the file does not exist, returns ([], 0).
    """
    if not TODO_FILE.exists():
        return [], 0

    text = TODO_FILE.read_text()
    lines = text.splitlines()

    tasks = []
    last_id = 0

    for line in lines:
        m = LAST_ID_RE.search(line)
        if m:
            last_id = int(m.group(1))

    for line in lines:
        m = TASK_LINE_RE.match(line)
        if m:
            tasks.append({
                'id': int(m.group(2)),
                'done': m.group(1) == 'x',
                'text': m.group(3),
            })

    return tasks, last_id


def write_todo(tasks, last_id):
    """Serialize tasks and footer back to TODO.md (atomic write via rename)."""
    lines = [HEADER, ""]
    for task in sorted(tasks, key=lambda t: t['id']):
        status = 'x' if task['done'] else ' '
        lines.append(f"- [{status}] {task['id']}. {task['text']}")
    lines.extend(["", f"<!-- last_id: {last_id} -->"])
    text = "\n".join(lines) + "\n"

    # Write to .tmp then rename for atomicity
    tmp = TODO_FILE.with_suffix(".md.tmp")
    tmp.write_text(text)
    tmp.rename(TODO_FILE)


def cmd_show():
    """List all tasks. Handles missing file and missing header."""
    if not TODO_FILE.exists():
        write_todo([], 0)
        print("No tasks")
        return

    text = TODO_FILE.read_text()
    has_header = any(line.strip() == "# Todo" for line in text.splitlines())

    if not has_header:
        write_todo([], 0)
        print("No tasks")
        return

    tasks, _ = read_todo()
    if not tasks:
        print("No tasks")
        return

    for task in tasks:
        status = ' ' if not task['done'] else 'x'
        print(f"{task['id']}. [{status}] {task['text']}")


def cmd_add(text):
    """Add a new task with the given text."""
    if not text:
        print("Error: task text cannot be empty", file=sys.stderr)
        sys.exit(1)

    # Ensure file exists before reading
    if not TODO_FILE.exists():
        write_todo([], 0)

    tasks, last_id = read_todo()
    new_id = last_id + 1
    tasks.append({'id': new_id, 'done': False, 'text': text})
    write_todo(tasks, new_id)
    print(f"Added task {new_id}: {text}")


def cmd_done(task_id):
    """Mark a task as completed (idempotent)."""
    tasks, last_id = read_todo()

    for task in tasks:
        if task['id'] == task_id:
            task['done'] = True
            write_todo(tasks, last_id)
            print(f"Marked task {task_id} as done")
            return

    print(f"Error: task {task_id} not found", file=sys.stderr)
    sys.exit(1)


def cmd_rm(task_id):
    """Remove a task entirely from the file."""
    tasks, last_id = read_todo()

    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            del tasks[i]
            write_todo(tasks, last_id)
            print(f"Removed task {task_id}")
            return

    print(f"Error: task {task_id} not found", file=sys.stderr)
    sys.exit(1)


def cmd_clear():
    """Remove all completed tasks."""
    tasks, last_id = read_todo()

    done_count = sum(1 for t in tasks if t['done'])
    if done_count == 0:
        print("No completed tasks to clear")
        return

    tasks = [t for t in tasks if not t['done']]
    write_todo(tasks, last_id)
    print(f"Cleared {done_count} completed task(s)")


def parse_args():
    """Build argparse with mutually exclusive flags."""
    parser = argparse.ArgumentParser(
        description="Manage a to-do list in TODO.md",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--show", action="store_true", default=False,
        help="Show all tasks (default)",
    )
    group.add_argument(
        "--add", type=str, default=None, metavar="TEXT",
        help="Add a new task",
    )
    group.add_argument(
        "--done", type=int, default=None, metavar="ID",
        help="Mark a task as done",
    )
    group.add_argument(
        "--rm", type=int, default=None, metavar="ID",
        help="Remove a task",
    )
    group.add_argument(
        "--clear", action="store_true", default=False,
        help="Remove all completed tasks",
    )
    return parser.parse_args()


def main():
    """Dispatch to the appropriate command based on parsed arguments."""
    args = parse_args()

    if args.add is not None:
        cmd_add(args.add)
    elif args.done is not None:
        cmd_done(args.done)
    elif args.rm is not None:
        cmd_rm(args.rm)
    elif args.clear:
        cmd_clear()
    else:
        cmd_show()


if __name__ == "__main__":
    main()
