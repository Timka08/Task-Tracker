# Task Tracker CLI

A simple console task tracker with no unnecessary clutter.
Stores data in `tasks.json`, works with standard Python only.

## Features

* Add tasks
* Update task descriptions
* Delete tasks
* Change status:

  * `todo`
  * `in-progress`
  * `done`
* View all tasks or filter by status
* Automatic creation of `tasks.json`
* Safe writing (atomic write) — file won’t break even on failures

##  Task Storage Format (`tasks.json`)

Each task looks like this:

```json
{
    "id": 1,
    "description": "Buy milk",
    "status": "todo",
    "createdAt": "2025-11-29T23:38:01.078332Z",
    "updatedAt": "2025-11-29T23:38:01.078332Z"
}
```

## Installation

0. Make sure you have Python 3 installed.
1. Clone or copy the files to your desired directory.
2. Done — no additional setup required.

## Running

```
python tracker.py <command> [arguments]
```

## Commands

### Add a new task

```
python tracker.py add "buy pasta"
```

### Update task description

```
python tracker.py update 3 "buy pasta and cheese"
```

### Delete a task

```
python tracker.py delete 2
```

### Mark a task as in-progress

```
python tracker.py mark-in-progress 1
```

### Mark a task as done

```
python tracker.py mark-done 1
```

### List all tasks

```
python tracker.py list
```

### List tasks by status

```
python tracker.py list todo
python tracker.py list in-progress
python tracker.py list done
```

### Help

```
python tracker.py help
```

## How It Works

* All commands go through `main()`, which parses the arguments.
* Tasks are stored in a JSON file.
* Writing is done via `atomic_write()` → temporary file → safe replacement.
* Statuses are validated automatically.
* IDs are assigned automatically.
* Timestamps are stored in UTC ISO format.

## Error Handling

* Invalid commands → error message.
* Invalid status → error message.
* Empty description → error message.
* Corrupted JSON is ignored (file will be safely overwritten on next operation).

## Example

```
> python tracker.py add "Buy groceries"
Task added successfully (ID: 1)

> python tracker.py mark-in-progress 1
Task 1 marked in-progress.

> python tracker.py list todo
No tasks.

> python tracker.py list
1. Buy groceries - in-progress (created: ..., updated: ...)
```

https://roadmap.sh/projects/task-tracker
