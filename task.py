class Task:
    """
    Represents a to-do task.
    """

    def __init__(self, title, description, due_date, completed, category, priority):
        """
        Initializes a Task.

        Args:
            title (str): Title of the task.
            description (str): Details about the task.
            due_date (datetime): When the task is due.
            completed (bool): Whether the task is completed.
            category (str): Category of the task.
            priority (str): Priority of the task.
        """
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed
        self.category = category
        self.priority = priority

    def __repr__(self):
        """
        Returns a string representation of the Task.
        """
        return f"Task: title={self.title},\n description={self.description},\n due_date={self.due_date},\n completed={self.completed},\n category={self.category},\n priority={self.priority}\n)"

    def mark_completed(self):
        """
        Marks this task as completed.
        """
        self.completed = True

    def mark_incomplete(self):
        """
        Marks this task as incomplete.
        """
        self.completed = False

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "completed": self.completed,
            "category": self.category,
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Task instance from a dictionary.
        Args:
            data (dict): Dictionary containing task attributes.
        Returns:
            Task: An instance of Task.
        """
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
            completed=data["completed"],
            category=data["category"],
            priority=data["priority"],
        )


class RecurringTask(Task):
    """ "
    Represents a recurring to-do task.
    """

    def __init__(
        self, title, description, due_date, completed, category, priority, recurrence_rule
    ):
        """
        Initializes a RecurringTask.
        Args:
            title (str): Title of the task.
            description (str): Details about the task.
            due_date (datetime): When the task is due.
            completed (bool): Whether the task is completed.
            category (str): Category of the task.
            priority (str): Priority of the task.
            recurrence_rule (str): Rule defining how often the task recurs.
        """
        super().__init__(title, description, due_date, completed, category, priority)
        self.recurrence_rule = recurrence_rule

    def __repr__(self):
        """
        Returns a string representation of the RecurringTask.
        """
        return f"RecurringTask(title={self.title}, description={self.description}, due_date={self.due_date}, completed={self.completed}, category={self.category}, priority={self.priority}, recurrence_rule={self.recurrence_rule})"

    def to_dict(self):
        """
        Converts the RecurringTask to a dictionary.
        """
        data = super().to_dict()
        data["recurrence_rule"] = self.recurrence_rule
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Creates a RecurringTask instance from a dictionary.
        Args:
            data (dict): Dictionary containing task attributes.
        Returns:
            RecurringTask: An instance of RecurringTask.
        """
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
            completed=data["completed"],
            category=data["category"],
            priority=data["priority"],
            recurrence_rule=data["recurrence_rule"],
        )
