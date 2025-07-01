import json
from typing import List

from pydantic import TypeAdapter

from task import AnyTask
from task_manager import TaskManager

AnyTaskAdapter = TypeAdapter(List[AnyTask])


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

    def save_tasks(self, task_manager: TaskManager):
        """
        Saves the tasks from the TaskManager to a JSON file.
        """
        tasks_as_dict = [task.model_dump(mode="json") for task in task_manager.get_tasks()]
        with open(self.filename, "w") as file:
            json.dump(tasks_as_dict, file, indent=4)

    def load_tasks(self, task_manager: TaskManager):
        """
        Loads tasks from a JSON file into the TaskManager.
        """
        try:
            with open(self.filename, "r") as file:
                tasks_data = json.load(file)
                loaded_tasks = AnyTaskAdapter.validate_python(tasks_data)
                task_manager.tasks = loaded_tasks
        except FileNotFoundError:
            pass
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error loading tasks from {self.filename}: {e}")
