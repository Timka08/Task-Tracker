# Task Tracker Application

class TaskTracker:
    def __init__(self):
        self.tasks = []
        self.command_map = {
        'add': self.add
        #'status': self.status,
        #'delete': self.delete,
        #'update': self.update,
        #'list': self.list_tasks
        #'change': self.change_status
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
    
    


def main():
    tracker = TaskTracker()
    print("Welcome to Task Tracker!")
    print("App can add tasks with title and status (assigned, in-progress, done).")
    print("To make a query, enter (delete, status, list, exit, add, change).")
    print("query structure: <command> <command_args>")
    query = input("Enter query ('exit' to quit): ").lower()
    while query != 'exit':
        query_parts = query.split()
        tracker.command(query_parts[0], query_parts[1:])
        query = input("Enter query ('exit' to quit): ").lower()
        
        
main()