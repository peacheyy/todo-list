import json
from task import Task

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, due_date=None):
        task = Task(title, description, due_date)
        self.tasks.append(task)

    def delete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            del self.tasks[task_index]

    def mark_task_complete(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].mark_as_complete()

    def list_tasks(self):
        for i, task in enumerate(self.tasks):
            print(f"{i}. {task}")

    def save_tasks(self, filename):
        with open(filename, 'w') as tasks_file:
            json.dump([task.to_dict() for task in self.tasks], tasks_file, indent=4)

    def load_tasks(self, filename):
        try:
            with open(filename, 'r') as tasks_file:
                data = json.load(tasks_file)
                self.tasks = [Task(**task) for task in data]
                print(f"Loaded {len(self.tasks)} tasks from {filename}")
        except FileNotFoundError:
            print(f"No such file: {filename}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {filename}")
