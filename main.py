# Task Tracker Application

class TaskTracker:
    def __init__(self):
        self.tasks = []
        self.command_map = {
        'add': self.add,
        'delete': self.delete,
        'list': self.list_tasks,
        'change': self.change
        }
        self.valid_statuses = ['assigned', 'in-progress', 'done']
    
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
            print("Invalid query. Please provide a command and necessary arguments.")
            return
        title = ' '.join(title)
        status ='assigned'
        self.tasks.append([title, status])
        print(f"Task '{title}' added")
    
    def list_tasks(self):
        if not self.tasks:
            print("First, add your important tasks here :)")
            return
        print("Here are your tasks:")
        for i, task in enumerate(self.tasks, start=1):
            print(f"{i}. {task[0]} - {task[1]}")
    
    def delete(self, *args):
        if len(args) != 1 or not args[0].isdigit():
            print("Invalid query. Please provide a command and necessary arguments.")
            return
        index = int(args[0]) - 1
        if 0 <= index < len(self.tasks):
            removed_task = self.tasks.pop(index)
            print(f"Task '{removed_task[0]}' deleted")
        else:
            print("You don`t have this task :(")
        
    def change(self, *args):
        if len(args) < 2 or not args[0].isdigit():
            print("Invalid query. Please provide a command and necessary arguments.")
            return
        index = int(args[0]) - 1
        if args[1] == 'status':
            print("Changing status\n 1. assigned\n 2. in-progress\n 3. done")
            if len(args) != 2 :
                print("")
                return
            if 0 <= index < len(self.tasks):
                edit_status = int(input("Enter new status number: "))
                if edit_status < 1 or edit_status > 3:
                    print("Invalid status number. Please enter 1, 2, or 3.")
                    return
                self.tasks[index][1] = self.valid_statuses[edit_status - 1] 
                print(f"Task '{self.tasks[index][0]}' status changed to '{self.valid_statuses[edit_status - 1]}'")
            else:
                print("You don`t have this task :(")
        elif args[1] == 'title':
            if len(args) < 2:
                print("Invalid query. Please provide a new title.")
                return
            new_title = input("Enter new title: ")
            if 0 <= index < len(self.tasks):
                old_title = self.tasks[index][0]
                self.tasks[index][0] = new_title
                print(f"Task title changed from '{old_title}' to '{new_title}'")
            else:
                print("You don`t have this task :(")
        else:
            print("Use 'status' or 'title' to make a change :\\")
    

def main():
    tracker = TaskTracker()
    print("Welcome to Task Tracker!")
    print("App can add tasks with title and status (assigned, in-progress, done).")
    print("To make a query, enter (delete, status, list, exit, add, change).")
    print("query structure: <command> <command_args>")
    query = input("\nEnter query ('exit' to quit): \n")
    while query != 'exit':
        if not query.strip():
            print("You could have typed something :\\")
            query = input("\nEnter query ('exit' to quit): \n")
            continue
        query_parts = query.split()
        tracker.command(query_parts[0].lower(), query_parts[1:])
        query = input("\nEnter query ('exit' to quit): \n")
        
        
main()