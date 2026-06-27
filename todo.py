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

TODO_PATH = Path(__file__).resolve().parent / "TODO.md"

HEADER = "# Todo"


# ---------------------------------------------------------------------------
# Data-layer functions
# ---------------------------------------------------------------------------

def ensure_file() -> None:
    """Create TODO.md with the ``# Todo`` header if it does not exist."""
    if not TODO_PATH.exists():
        TODO_PATH.write_text(HEADER + "\n\n", encoding="utf-8")


def parse_tasks(content: str) -> list[dict]:
    """Return a list of task dicts parsed from markdown checklist content.

    Each dict has keys: ``id``, ``desc``, ``done``, ``raw``.
    Lines that do not match the task pattern are silently skipped.
    """
    tasks: list[dict] = []
    pattern = re.compile(r"^-\s+\[([ x])\]\s+(\d+)\.\s+(.*)$")
    for line in content.splitlines():
        m = pattern.match(line)
        if m:
            tasks.append({
                "id": int(m.group(2)),
                "desc": m.group(3),
                "done": m.group(1) == "x",
                "raw": line,
            })
    return tasks


def serialize_tasks(tasks: list[dict]) -> str:
    """Convert a list of task dicts back to markdown text (header + blank line
    + task lines)."""
    lines = [HEADER, ""]
    for t in tasks:
        status = "x" if t["done"] else " "
        lines.append(f"- [{status}] {t['id']}. {t['desc']}")
    lines.append("")
    return "\n".join(lines)


def next_id(tasks: list[dict]) -> int:
    """Return ``max(existing ids) + 1``, or ``1`` if the list is empty."""
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


def read_todo() -> list[dict]:
    """Read and parse ``TODO.md``.

    On missing file, create it and return ``[]``.
    Raises ``OSError`` / ``IOError`` on other I/O failures.
    """
    ensure_file()
    content = TODO_PATH.read_text(encoding="utf-8")
    return parse_tasks(content)


def write_todo(tasks: list[dict]) -> None:
    """Serialize the task list and write ``TODO.md``.

    Raises ``OSError`` / ``IOError`` on failure.
    """
    TODO_PATH.write_text(serialize_tasks(tasks), encoding="utf-8")


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_show(tasks: list[dict]) -> None:
    """Print tasks split into 'Pending' and 'Done' groups."""
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


def cmd_add(tasks: list[dict], text: str) -> str:
    """Create a new pending task and append it to the list."""
    new_id = next_id(tasks)
    tasks.append({
        "id": new_id,
        "desc": text,
        "done": False,
        "raw": f"- [ ] {new_id}. {text}",
    })
    write_todo(tasks)
    return f"Added task {new_id}."


def cmd_done(tasks: list[dict], raw_id: str) -> str:
    """Mark a task as completed by its id."""
    task_id = int(raw_id)
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            write_todo(tasks)
            return f"Task {task_id} marked as done."
    print(f"Task {task_id} not found")
    sys.exit(1)


def cmd_rm(tasks: list[dict], raw_id: str) -> str:
    """Remove a task by its id."""
    task_id = int(raw_id)
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            del tasks[i]
            write_todo(tasks)
            return f"Removed task {task_id}."
    print(f"Task {task_id} not found")
    sys.exit(1)


def cmd_clear(tasks: list[dict]) -> str:
    """Remove all done (completed) tasks."""
    done_count = sum(1 for t in tasks if t["done"])
    if done_count == 0:
        print("No done tasks to clear.")
        sys.exit(1)
    remaining = [t for t in tasks if not t["done"]]
    write_todo(remaining)
    return f"Cleared {done_count} done task(s)."


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Parse arguments and dispatch to the appropriate command handler."""
    parser = argparse.ArgumentParser(
        description="Markdown-based to-do tracker.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--show",
        action="store_true",
        default=False,
        help="show all tasks (default)",
    )
    group.add_argument("--add", metavar="TEXT", help="add a new task")
    group.add_argument(
        "--done", metavar="ID", type=str, help="mark a task as done"
    )
    group.add_argument(
        "--rm", metavar="ID", type=str, help="remove a task"
    )
    group.add_argument(
        "--clear", action="store_true", help="clear all done tasks"
    )

    args = parser.parse_args()

    try:
        tasks = read_todo()

        if args.add is not None:
            msg = cmd_add(tasks, args.add)
        elif args.done is not None:
            msg = cmd_done(tasks, args.done)
        elif args.rm is not None:
            msg = cmd_rm(tasks, args.rm)
        elif args.clear:
            msg = cmd_clear(tasks)
        else:
            cmd_show(tasks)
            return  # cmd_show prints directly and may exit

        print(msg)
    except (OSError, IOError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
