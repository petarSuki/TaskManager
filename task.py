from datetime import datetime
from enum import Enum


def parse_date(date_str: str) -> datetime:
    """
    Parses a date string in the format "DD.MM.YYYY" into a datetime object.

    Args:
        date_str (str): Date string in the format "DD.MM.YYYY".

    Returns:
        datetime: Parsed datetime object.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        pass

    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        raise ValueError(f"Date '{date_str}' could not be parsed. Use YYYY-MM-DD or DD.MM.YYYY.")


class Priority(Enum):
    """
    Enum for task priority levels.
    """

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

    def __str__(self):
        return self.value


class Task:
    """
    Represents a to-do task.
    """

    def __init__(
        self,
        title: str,
        description: str,
        due_date: datetime,
        completed: bool,
        category: str,
        priority: str,
    ):
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
        self.due_date = due_date if isinstance(due_date, datetime) else parse_date(due_date)
        self.completed = completed
        self.category = category
        self.priority = Priority(priority) if isinstance(priority, str) else priority

    def __repr__(self):
        """
        Returns a string representation of the Task.
        """
        return (
            f"Task(\n"
            f"    title={self.title}\n"
            f"    description={self.description}\n"
            f"    due_date={self.due_date}\n"
            f"    completed={self.completed}\n"
            f"    category={self.category}\n"
            f"    priority={self.priority}\n"
            ")"
        )

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
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "completed": self.completed,
            "category": self.category,
            "priority": self.priority.value,
        }

    # class method can be used but in storage.py we are using the constructor directly
    # (it means we are creating an instance of Task directly)
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
            due_date=parse_date(data["due_date"]),
            completed=data["completed"],
            category=data["category"],
            priority=Priority(data["priority"])
            if isinstance(data["priority"], str)
            else data["priority"],
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
        return (
            f"RecurringTask(\n"
            f"    title={self.title}\n"
            f"    description={self.description}\n"
            f"    due_date={self.due_date}\n"
            f"    completed={self.completed}\n"
            f"    category={self.category}\n"
            f"    priority={self.priority}\n"
            f"    recurrence_rule={self.recurrence_rule}\n"
            ")"
        )

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
            due_date=parse_date(data["due_date"]),
            completed=data["completed"],
            category=data["category"],
            priority=Priority(data["priority"])
            if isinstance(data["priority"], str)
            else data["priority"],
            recurrence_rule=data["recurrence_rule"],
        )
