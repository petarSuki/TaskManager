import json

from task import RecurringTask, Task


class TaskStorage:
    """
    Handles the storage of tasks in a JSON file.
    Provides methods to save and load tasks.
    """

    def __init__(self, filename="tasks.json"):
        """
        Initializes the TaskStorage with a specified filename.
        """
        self.filename = filename

    def save_tasks(self, task_manager):
        """
        Saves the tasks from the TaskManager to a JSON file.
        """
        with open(self.filename, "w") as file:
            json.dump([task.to_dict() for task in task_manager.get_tasks()], file, indent=4)

    def load_tasks(self, task_manager):
        """
        Loads tasks from a JSON file into the TaskManager.
        """
        try:
            with open(self.filename, "r") as file:
                tasks_data = json.load(file)
                for task_data in tasks_data:
                    if "recurrence" in task_data:
                        task = RecurringTask.from_dict(task_data)
                    else:
                        task = Task.from_dict(task_data)
                        # task = Task(
                        #     title=task_data["title"],
                        #     description=task_data["description"],
                        #     due_date=task_data["due_date"],
                        #     completed=task_data["completed"],
                        #     category=task_data.get("category"),
                        #     priority=task_data.get("priority"),
                        # )
                    task_manager.tasks.append(task)
        except FileNotFoundError:
            print()
