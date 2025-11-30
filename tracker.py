import sys
import os
import json
from datetime import datetime
from tempfile import NamedTemporaryFile
from shutil import move

FILENAME = "tasks.json"
VALID_STATUSES = {"todo", "in-progress", "done"}

def now_iso():
    return datetime.utcnow().isoformat() + "Z"


def atomic_write(path, data):
    dirpath = os.path.dirname(os.path.abspath(path)) or "."
    with NamedTemporaryFile("w", dir=dirpath, delete=False, encoding="utf-8") as tf:
        json.dump(data, tf, ensure_ascii=False, indent=4)
        tmpname = tf.name
    move(tmpname, path)


def load_tasks():
    if not os.path.exists(FILENAME):
        return []

    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        return []

    new = []
    for item in raw:
        if isinstance(item, dict) and "id" in item and "description" in item and "status" in item:
            new.append(item)
            continue
        # skip invalid items
        continue

    # ensure all items have ids; assign later
    # Also clean invalid statuses
    for t in new:
        if t.get("status") not in VALID_STATUSES:
            t["status"] = "todo"
        if "createdAt" not in t or not t["createdAt"]:
            t["createdAt"] = now_iso()
        if "updatedAt" not in t or not t["updatedAt"]:
            t["updatedAt"] = t["createdAt"]

    used_ids = {t["id"] for t in new if t["id"] is not None}
    next_id = 1
    for t in new:
        if t["id"] is None:
            while next_id in used_ids:
                next_id += 1
            t["id"] = next_id
            used_ids.add(next_id)
            next_id += 1

    return new


def save_tasks(tasks):
    atomic_write(FILENAME, tasks)


def find_task(tasks, tid):
    for t in tasks:
        if t["id"] == tid:
            return t
    return None


def next_id(tasks):
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


def print_task(task):
    print(f"{task['id']}. {task['description']} - {task['status']} (created: {task['createdAt']}, updated: {task['updatedAt']})")


# ---------- Commands ----------

def cmd_add(args):
    if not args:
        print("Error: missing description. Usage: add \"task description\"")
        return
    desc = " ".join(args).strip()
    if not desc:
        print("Error: empty description.")
        return

    tasks = load_tasks()
    tid = next_id(tasks)
    ts = now_iso()
    task = {
        "id": tid,
        "description": desc,
        "status": "todo",
        "createdAt": ts,
        "updatedAt": ts
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {tid})")


def cmd_delete(args):
    if len(args) != 1 or not args[0].isdigit():
        print("Error: delete requires a single numeric id. Usage: delete <id>")
        return
    tid = int(args[0])
    tasks = load_tasks()
    task = find_task(tasks, tid)
    if not task:
        print("No such task with id", tid)
        return
    tasks = [t for t in tasks if t["id"] != tid]
    save_tasks(tasks)
    print(f"Task {tid} deleted.")


def cmd_update(args):
    if len(args) < 2 or not args[0].isdigit():
        print("Usage: update <id> \"new description\"")
        return
    tid = int(args[0])
    new_desc = " ".join(args[1:]).strip()
    if not new_desc:
        print("Error: empty description.")
        return
    tasks = load_tasks()
    task = find_task(tasks, tid)
    if not task:
        print("No such task with id", tid)
        return
    task["description"] = new_desc
    task["updatedAt"] = now_iso()
    save_tasks(tasks)
    print(f"Task {tid} updated.")


def cmd_mark_in_progress(args):
    if len(args) != 1 or not args[0].isdigit():
        print("Usage: mark-in-progress <id>")
        return
    tid = int(args[0])
    tasks = load_tasks()
    task = find_task(tasks, tid)
    if not task:
        print("No such task with id", tid)
        return
    task["status"] = "in-progress"
    task["updatedAt"] = now_iso()
    save_tasks(tasks)
    print(f"Task {tid} marked in-progress.")


def cmd_mark_done(args):
    if len(args) != 1 or not args[0].isdigit():
        print("Usage: mark-done <id>")
        return
    tid = int(args[0])
    tasks = load_tasks()
    task = find_task(tasks, tid)
    if not task:
        print("No such task with id", tid)
        return
    task["status"] = "done"
    task["updatedAt"] = now_iso()
    save_tasks(tasks)
    print(f"Task {tid} marked done.")


def cmd_list(args):
    tasks = load_tasks()
    filter_status = args[0] if len(args) >= 1 else None

    if filter_status and filter_status not in ("todo", "done", "in-progress"):
        print(f"Unknown filter: {filter_status}")
        return

    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]

    if not tasks:
        print("No tasks.")
        return

    for t in tasks:
        print(f"{t['id']}. {t['description']} - {t['status']} "
              f"(created: {t['createdAt']}, updated: {t['updatedAt']})")


def cmd_help(_args=None):
    print("Task Tracker CLI")
    print("Commands:")
    print("  add <description>                - Add new task")
    print("  update <id> <new description>    - Update task description")
    print("  delete <id>                      - Delete task")
    print("  mark-in-progress <id>            - Set status to in-progress")
    print("  mark-done <id>                   - Set status to done")
    print("  list [done|todo|in-progress]     - List tasks (optional filter)")
    print("  help                             - Show this help")


# ---------- Main dispatch ----------

def main():
    if len(sys.argv) < 2:
        cmd_help()
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    # ensure file exists (create if missing)
    if not os.path.exists(FILENAME):
        try:
            save_tasks([])
        except Exception:
            pass

    try:
        if cmd == "add":
            cmd_add(args)
        elif cmd == "update":
            cmd_update(args)
        elif cmd == "delete":
            cmd_delete(args)
        elif cmd == "mark-in-progress":
            cmd_mark_in_progress(args)
        elif cmd == "mark-done":
            cmd_mark_done(args)
        elif cmd == "list":
            cmd_list(args)
        elif cmd == "help":
            cmd_help()
        else:
            print("Unknown command. Use 'help' to see available commands.")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
