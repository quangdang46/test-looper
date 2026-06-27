#!/usr/bin/env python3
"""todo.py — a markdown-based to-do tracker.

Usage:
    python todo.py              Show all tasks
    python todo.py --show       Show all tasks
    python todo.py --add "buy milk"      Add a new task
    python todo.py --done 2              Mark task #2 as done
    python todo.py --rm 3                Remove task #3 entirely
    python todo.py --clear               Remove all done tasks

Tasks are stored in TODO.md using GitHub-Flavored Markdown checkboxes:
    - [ ] 1. buy milk
    - [x] 2. call mom
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, NamedTuple, Optional

_TODO_FILE = Path(__file__).resolve().parent / "TODO.md"
_HEADER = "# Todo"
_PATTERN = re.compile(r"^- \[([ x])\] (\d+)\. (.+)$")


class Task(NamedTuple):
    id: int
    description: str
    done: bool


# ── helpers ──────────────────────────────────────────────────────────────────


def _die(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(1)


# ── I/O ──────────────────────────────────────────────────────────────────────


def load_tasks() -> List[Task]:
    """Parse TODO.md into a list of Task objects.

    File missing → create header → return [].
    No "# Todo" header → print "No tasks" → return [].
    """
    if not _TODO_FILE.exists():
        _TODO_FILE.write_text(_HEADER + "\n")
        return []

    text = _TODO_FILE.read_text(encoding="utf-8")
    if not text.strip().startswith("# Todo"):
        print("No tasks")
        return []

    tasks: List[Task] = []
    for line in text.splitlines():
        m = _PATTERN.match(line.strip())
        if m:
            status, tid, desc = m.groups()
            tasks.append(Task(id=int(tid), description=desc, done=(status == "x")))
    return tasks


def save_tasks(tasks: List[Task]) -> None:
    """Write the list of Task objects back to TODO.md."""
    lines = [_HEADER, ""]
    for t in tasks:
        cb = "x" if t.done else " "
        lines.append(f"- [{cb}] {t.id}. {t.description}")
    _TODO_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ── business logic ───────────────────────────────────────────────────────────


def show_tasks(tasks: List[Task]) -> None:
    """Print tasks grouped as Pending / Done."""
    if not tasks:
        print("No tasks")
        return

    pending = [t for t in tasks if not t.done]
    done = [t for t in tasks if t.done]

    if pending:
        print("### Pending")
        for t in pending:
            print(f"  {t.id}. {t.description}")
    if done:
        print("### Done")
        for t in done:
            print(f"  {t.id}. {t.description}")


def add_task(tasks: List[Task], text: str) -> None:
    """Append a new pending task with next available id."""
    existing_ids = {t.id for t in tasks}
    next_id = max(existing_ids) + 1 if existing_ids else 1
    tasks.append(Task(id=next_id, description=text, done=False))
    save_tasks(tasks)


def done_task(task_id: int) -> None:
    """Mark a task as done by id. Print error if not found."""
    tasks = load_tasks()
    for i, t in enumerate(tasks):
        if t.id == task_id:
            if not t.done:
                tasks[i] = t._replace(done=True)
                save_tasks(tasks)
            return
    _die(f"Task {task_id} not found")


def rm_task(task_id: int) -> None:
    """Remove a task line entirely by id. Print error if not found."""
    tasks = load_tasks()
    before = len(tasks)
    tasks = [t for t in tasks if t.id != task_id]
    if len(tasks) == before:
        _die(f"Task {task_id} not found")
    save_tasks(tasks)


def clear_done() -> None:
    """Remove all done tasks. Print message if none to clear."""
    tasks = load_tasks()
    pending = [t for t in tasks if not t.done]
    removed = len(tasks) - len(pending)
    if removed == 0:
        print("No done tasks to clear")
        return
    save_tasks(pending)


# ── argument parsing ─────────────────────────────────────────────────────────


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Markdown-based to-do tracker.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show all tasks (default action when no option given)",
    )
    parser.add_argument("--add", metavar="TEXT", help="Add a new task")
    parser.add_argument(
        "--done", metavar="ID", type=int, help="Mark a task as done by id"
    )
    parser.add_argument(
        "--rm", metavar="ID", type=int, help="Remove a task by id"
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Remove all done tasks",
    )
    return parser.parse_args(argv)


# ── main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    args = parse_args(sys.argv[1:])

    # Dispatch actions that modify the file first.
    if args.add is not None:
        try:
            tasks = load_tasks()
        except OSError as e:
            _die(f"Error: {e}")
        add_task(tasks, args.add)
        return

    if args.done is not None:
        try:
            done_task(args.done)
        except OSError as e:
            _die(f"Error: {e}")
        return

    if args.rm is not None:
        try:
            rm_task(args.rm)
        except OSError as e:
            _die(f"Error: {e}")
        return

    if args.clear:
        try:
            clear_done()
        except OSError as e:
            _die(f"Error: {e}")
        return

    # Default / --show: print tasks.
    try:
        tasks = load_tasks()
    except OSError as e:
        _die(f"Error: {e}")
    show_tasks(tasks)


if __name__ == "__main__":
    main()
