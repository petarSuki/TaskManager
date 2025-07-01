from datetime import datetime
from enum import Enum
from typing import Literal, Union

from pydantic import BaseModel, field_validator


def parse_date(date_str: str) -> datetime:
    """
    Parses a date string in the format "DD.MM.YYYY" into a datetime object.

    Args:
        date_str (str): Date string in the format "DD.MM.YYYY".

    Returns:
        datetime: Parsed datetime object.
    """
    if isinstance(date_str, str) and "T" in date_str:
        date_str = date_str.split("T")[0]  # Handle ISO format with time
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        pass

    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except ValueError:
        raise ValueError(f"Date '{date_str}' could not be parsed. Use YYYY-MM-DD or DD.MM.YYYY.")


class Priority(str, Enum):
    """
    Enum for task priority levels.
    """

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskBase(BaseModel):
    """
    Represents a to-do task.
    """

    title: str
    description: Union[str, None] = None
    due_date: datetime
    completed: bool = False
    category: Union[str, None] = None
    priority: Priority = Priority.MEDIUM

    @field_validator("due_date", mode="before")
    @classmethod
    def validate_due_date(cls, value):
        """
        Validates the due date format.
        Accepts both "YYYY-MM-DD" and "DD.MM.YYYY" formats.
        """
        if isinstance(value, str):
            return parse_date(value)
        return value

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


class Task(TaskBase):
    """
    A simple, non-recurring to-do task.
    """

    task_type: Literal["simple"] = "simple"


class RecurringTask(TaskBase):
    """
    Represents a recurring to-do task.
    """

    task_type: Literal["recurring"] = "recurring"
    recurrence: str  # Recurrence pattern, e.g., "daily", "weekly", "monthly"


AnyTask = Union[Task, RecurringTask]
