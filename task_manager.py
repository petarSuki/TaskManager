from typing import List

from task import AnyTask


class TaskManager:
    """
    Manages a collection of tasks.
    Allows adding, removing, and retrieving tasks.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list.
        """
        self.tasks: List[AnyTask] = []

    def add_task(self, task: AnyTask):
        """
        Adds a new task to the task list.
        """
        self.tasks.append(task)

    def remove_task(self, title: str) -> bool:
        """
        Removes a task from the task list by title.
        If multiple tasks have the same title, all will be removed.
        """
        inital_length = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.title != title]
        return len(self.tasks) < inital_length

    def get_tasks(self, filter=None) -> List[AnyTask]:
        """
        Retrieves all tasks, optionally filtered by a given function.
        If no filter is provided, returns all tasks.
        """
        if filter is None:
            return self.tasks
        return [task for task in self.tasks if filter(task)]

    def get_task_by_title(self, keyword: str) -> List[AnyTask]:
        """
        Retrieves tasks that contain a specific keyword in their title.
        """
        return [task for task in self.tasks if keyword.lower() in task.title.lower()]
