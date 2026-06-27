#!/usr/bin/env python3
"""Markdown-based to-do tracker.

Usage:
    python todo.py                  show tasks (default)
    python todo.py --show           show tasks
    python todo.py --add "text"     add a task
    python todo.py --done <id>      mark task as done
    python todo.py --rm <id>        remove a task
    python todo.py --clear          clear all done tasks
"""

import argparse
import re
import sys
from pathlib import Path

TODO_FILENAME = "TODO.md"


def _get_todo_dir():
    return Path(__file__).resolve().parent


def _ensure_file(todo_path):
    """Create TODO.md with the # Todo header if it doesn't exist."""
    if not todo_path.exists():
        todo_path.write_text("# Todo\n\n", encoding="utf-8")


def parse_tasks(content):
    """Return list of dicts with keys: id, desc, done.

    Only lines matching ``- [<sp| x>] <id>. <desc>`` are parsed;
    all other lines (header, blanks, etc.) are ignored.
    """
    tasks = []
    for line in content.splitlines():
        m = re.match(r"^- \[([ x])\] (\d+)\. (.+)$", line)
        if m:
            tasks.append({
                "id": int(m.group(2)),
                "desc": m.group(3),
                "done": m.group(1) == "x",
            })
    return tasks


def serialize_tasks(tasks):
    """Convert task list back to markdown (header + blank + tasks + trailing newline)."""
    lines = ["# Todo", ""]
    for t in tasks:
        box = "x" if t["done"] else " "
        lines.append(f"- [{box}] {t['id']}. {t['desc']}")
    lines.append("")
    return "\n".join(lines)


def next_id(tasks):
    """Return max(existing ids) + 1, or 1 if tasks is empty.

    Deleted task ids are never reused.
    """
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


def read_todo():
    """Read and parse TODO.md.  Create the file with the header if it's missing."""
    todo_path = _get_todo_dir() / TODO_FILENAME
    _ensure_file(todo_path)
    content = todo_path.read_text(encoding="utf-8")
    return parse_tasks(content)


def write_todo(tasks):
    """Serialize the task list and write it back to TODO.md."""
    todo_path = _get_todo_dir() / TODO_FILENAME
    todo_path.write_text(serialize_tasks(tasks), encoding="utf-8")


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------


def _find_task_or_exit(tasks, raw_id):
    """Look up a task by its id string.  Print error and exit(1) on failure."""
    try:
        tid = int(raw_id)
    except ValueError:
        print(f"Task {raw_id} not found")
        sys.exit(1)
    for i, t in enumerate(tasks):
        if t["id"] == tid:
            return t, i
    print(f"Task {tid} not found")
    sys.exit(1)


def cmd_show(tasks):
    """Print tasks grouped by status.  Exits with 0 if the list is empty."""
    if not tasks:
        print("No tasks.")
        sys.exit(0)
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


def cmd_add(tasks, text):
    """Append a new pending task."""
    tid = next_id(tasks)
    tasks.append({"id": tid, "desc": text, "done": False})
    write_todo(tasks)
    return f"Added task {tid}."


def cmd_done(tasks, raw_id):
    """Mark a task as completed."""
    t, _ = _find_task_or_exit(tasks, raw_id)
    t["done"] = True
    write_todo(tasks)
    return f"Task {t['id']} marked as done."


def cmd_rm(tasks, raw_id):
    """Remove a task entirely."""
    t, idx = _find_task_or_exit(tasks, raw_id)
    del tasks[idx]
    write_todo(tasks)
    return f"Removed task {t['id']}."


def cmd_clear(tasks):
    """Remove all completed tasks."""
    done = [t for t in tasks if t["done"]]
    if not done:
        print("No done tasks to clear.")
        sys.exit(1)
    tasks[:] = [t for t in tasks if not t["done"]]
    write_todo(tasks)
    return f"Cleared {len(done)} done task(s)."


# ---------------------------------------------------------------------------
# Argument parsing & main
# ---------------------------------------------------------------------------


def parse_args(argv=None):
    """Build argument parser with mutually exclusive flags.

    Default to --show when no flag is provided.
    """
    parser = argparse.ArgumentParser(description="Markdown-based to-do tracker")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--show", action="store_true", help="show tasks")
    group.add_argument("--add", metavar="TEXT", help="add a task")
    group.add_argument("--done", metavar="ID", help="mark task as done")
    group.add_argument("--rm", metavar="ID", help="remove a task")
    group.add_argument("--clear", action="store_true", help="clear all done tasks")
    args = parser.parse_args(argv)
    if not any([args.show, args.add, args.done, args.rm, args.clear]):
        args.show = True
    return args


def main(argv=None):
    """Entry point: parse args, dispatch to the right handler."""
    args = parse_args(argv)
    try:
        tasks = read_todo()
        if args.show:
            cmd_show(tasks)
        elif args.add is not None:
            print(cmd_add(tasks, args.add))
        elif args.done is not None:
            print(cmd_done(tasks, args.done))
        elif args.rm is not None:
            print(cmd_rm(tasks, args.rm))
        elif args.clear:
            print(cmd_clear(tasks))
    except (OSError, IOError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
