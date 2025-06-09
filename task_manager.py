from task import Task


class TaskManager:
    """
    Manages a collection of tasks.
    Allows adding, removing, and retrieving tasks.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list.
        """
        self.tasks = []

    def add_task(
        self, title, description, due_date, completed=False, category=None, priority=None
    ):
        """
        Adds a new task to the task list.
        """
        task = Task(title, description, due_date, completed, category, priority)
        self.tasks.append(task)

    def remove_task(self, title):
        """
        Removes a task from the task list by title.
        If multiple tasks have the same title, all will be removed.
        """
        self.tasks = [task for task in self.tasks if task.title != title]

    def get_tasks(self, filter=None):
        """
        Retrieves all tasks, optionally filtered by a given function.
        If no filter is provided, returns all tasks.
        """
        if filter is None:
            return self.tasks
        return [task for task in self.tasks if filter(task)]

    def get_task_by_title(self, keyword):
        """
        Retrieves tasks that contain a specific keyword in their title.
        """
        return [task for task in self.tasks if keyword.lower() in task.title.lower()]
