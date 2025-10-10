# Task Tracker CLI

**Task Tracker** is a simple Python console task manager that allows you to add, delete, and edit tasks while tracking their status. Perfect for personal use or as a learning project.

---

## 💡 Features
- Add tasks with a title (default status: `assigned`)
- Delete tasks by number
- Change task status (`assigned`, `in-progress`, `done`) or title
- Clear all tasks with automatic backup
- Auto-save after every action
- Sort tasks by status (`in-progress` → `assigned` → `done`)
- Colorful console output using `colorama`
- Load saved tasks from a file

---

## ⚙️ Installation

1. Clone the repository:
```bash
gh repo clone Timka08/Task-Tracker
cd <your-repo-folder>
```

2. Install dependencies:
```bash
pip install colorama
```

3. Run the application:
```bash
python main.py
```

---

## 📑 Commands
| Command | Description |
|---------|------------|
| `add <title>` | Add a new task (default status: `assigned`) |
| `delete <task_number>` | Delete a task by its number |
| `list` | List all tasks |
| `change <num> status <new_status>` | Change the status of a task |
| `change <num> title <new_title>` | Change the title of a task |
| `clear` | Clear all tasks (backup is saved automatically) |
| `load` | Load tasks from the file |
| `help` | Show available commands |
| `exit` | Exit the application |

---

## 📦 Example

```
> add Finish homework
Task 'Finish homework' added
1. Finish homework - assigned

> change 1 status in-progress
Task status changed from 'assigned' to 'in-progress'
1. Finish homework - in-progress
```

---

## 💾 Files

- `main.py` — main script
- `tasks.json` — file to store tasks (created automatically)
- `tasks.json.bak` — backup file when clearing all tasks

---

## 🛠️ License
MIT License

