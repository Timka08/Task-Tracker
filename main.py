import os
import json
from colorama import init, Fore, Style
init()
class TaskTracker:
    def __init__(self):
        self.tasks = []
        self.filename = 'tasks.json'
        self.command_map = {
        'add': self.add,
        'delete': self.delete,
        'list': self.list_tasks,
        'change': self.change,
        'clear': self.clear_tasks,
        'load': self.load_from_file
        }
        self.valid_statuses = ['assigned','in-progress','done']
    
    def auto_save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)
    
    def help(self):
        print("Available commands:")
        print("add <title> - Add a new task with the given title (status defaults to 'assigned').")
        print("delete <task_number> - Delete the task with the specified number.")
        print("list - List all tasks.")
        print("change <task_number> status <new_status> - Change the status of the specified task.")
        print("change <task_number> title <new_title> - Change the title of the specified task.")
        print("clear - Clear all tasks (with backup).")
        print("load - Load tasks from file.")
        print("exit - Exit the application.")
    def command(self, cmd, args): 
        if not cmd:
            print("No command provided.") 
            return
        if cmd in self.command_map:
            self.command_map[cmd](*args)
        else:
            print(f"Unknown command: {cmd}")           
    
    def add(self, *title):
        if len(title) < 1:
            print(Fore.RED + Style.BRIGHT + "Invalid query. Please provide a command and necessary arguments." + Style.RESET_ALL)
            return
        title = ' '.join(title)
        status ='assigned'
        self.tasks.append([title, status])
        print(f"Task '{title}' added")
        self.list_tasks()

        
    def sort_by_status(self):
        order = {'assigned': 1, 'in-progress': 0, 'done': 2}
        self.tasks.sort(key=lambda t: order[t[-1]])
        
    def list_tasks(self):
        self.sort_by_status()
        self.auto_save()
        if not self.tasks:
            print("First, add your important tasks here :)")
            return
        print("Here are your tasks:")
        color_map = {
            "assigned": Fore.MAGENTA,
            "in-progress": Fore.YELLOW,
            "done": Fore.GREEN
            }
        for i, task in enumerate(self.tasks, start=1):
            status_colored = color_map.get(task[1], Fore.WHITE) + task[1] + Style.RESET_ALL
            print(f"{i}. {task[0]} - {status_colored}")
    
    

    def delete(self, *args):
        if len(args) != 1 or not args[0].isdigit():
            print(Fore.RED + Style.BRIGHT + "Invalid query. Please provide a command and necessary arguments." + Style.RESET_ALL)
            return
        index = int(args[0]) - 1
        if 0 <= index < len(self.tasks):
            removed_task = self.tasks.pop(index)
            print(f"Task '{removed_task[0]}' deleted")
            self.list_tasks()
        else:
            print("You don`t have this task :(")
   
        
    def change(self, *args):
        if len(args) < 2 or not args[0].isdigit():
            print(Fore.RED + Style.BRIGHT + "Invalid query. Please provide a command and necessary arguments." + Style.RESET_ALL)
            return
        index = int(args[0]) - 1
        if args[1] == 'status':
            if len(args) < 3 or args[2] not in self.valid_statuses:
                print(Fore.RED + Style.BRIGHT + f"Invalid status. Valid statuses are: {', '.join(self.valid_statuses)}." + Style.RESET_ALL)
                return
            else:
                new_status = args[2]
                if 0 <= index < len(self.tasks):
                    old_status = self.tasks[index][1]
                    self.tasks[index][1] = new_status
                    print(f"Task status changed from '{old_status}' to '{new_status}'")
                    self.list_tasks()
                else:
                    print("You don`t have this task :(")
        elif args[1] == 'title':
            if len(args) < 3:
                print(Fore.RED + Style.BRIGHT + "Invalid query. Please provide a new title." + Style.RESET_ALL)
                return
            new_title = ' '.join(args[2:])
            if 0 <= index < len(self.tasks):
                old_title = self.tasks[index][0]
                self.tasks[index][0] = new_title
                print(f"Task title changed from '{old_title}' to '{new_title}'")
                self.list_tasks()
            else:
                print("You don`t have this task :(")
        else:
            print("Use 'status' or 'title' to make a change :\\")
    
    def clear_tasks(self):
        if input("Are you sure you want to clear all tasks? (y/n): ").lower() == 'y':
            with open(self.filename + '.bak', 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=4)
            self.tasks.clear()
            print("All tasks have been cleared. Backup saved as tasks.json.bak")
            self.list_tasks()
        else:
            print("Clear operation cancelled.")

    def load_from_file(self):
        if not os.path.exists(self.filename):
            print("No saved tasks found, starting fresh.")
            return
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.tasks = json.load(f)
            print("Tasks loaded successfully ✅")
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"Error loading tasks: {e}" + Style.RESET_ALL)

def main():
    tracker = TaskTracker()
    tracker.load_from_file()
    print("Welcome to Task Tracker!")
    print("App can add tasks with title and status (assigned, in-progress, done).\n")
    print("To make a query, enter (delete, list, exit, add, change).")
    print("query structure: <command> <command_args>\n")
    tracker.list_tasks()
    query = input("\nEnter query ('exit' to quit): \n")
    while query != 'exit':
        if not query.strip():
            print("You could have typed something :\\")
            query = input("\nEnter query ('exit' to quit): \n")
            continue
        query_parts = query.split()
        tracker.command(query_parts[0].lower(), query_parts[1:])
        query = input("\nEnter query ('exit' to quit): \n")
    tracker.auto_save() 
    print(Fore.GREEN + "\nYour tasks are safe ;). See you next time 👋" + Style.RESET_ALL)

main()