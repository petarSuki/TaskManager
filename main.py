from typing import Annotated, Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from storage import TaskStorage
from task import Priority, Task
from task_manager import TaskManager

app = FastAPI()

# CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskSchema(BaseModel):
    title: str
    description: str
    due_date: str  # Assuming date is in 'YYYY-MM-DD' format
    completed: bool = False
    category: Union[str, None] = None
    priority: Union[str, Priority] = "medium"  # Default priority


# class RecurringTaskSchema(TaskSchema):
#     title: str
#     description: str
#     due_date: str  # Assuming date is in 'YYYY-MM-DD' format
#     completed: bool = False
#     category: Union[str, None] = None
#     priority: Union[str, Priority] = "medium"  # Default priority
#     recurrence: str  # Recurrence pattern, e.g., "daily", "weekly", "monthly"

# class TaskManagerSchema(BaseModel):
#     tasks: list[TaskSchema]


task_manager = TaskManager()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Manager API"}


@app.get("/tasks")
def get_tasks():
    """
    Retrieve all tasks.
    """
    return task_manager.get_tasks()


@app.post("/tasks")
def create_task(
    title: str,
    description: str,
    due_date: str,
    completed: bool = False,
    category: Annotated[str, None] = None,
    priority: Annotated[str, Priority] = "medium",
):
    """
    Create a new task.
    """
    t = Task(
        title=title,
        description=description,
        due_date=due_date,
        completed=completed,
        category=category,
        priority=Priority(priority) if isinstance(priority, str) else priority,
    )
    task_manager.add_task(t.title, t.description, t.due_date, t.completed, t.category, t.priority)
    return task_manager.get_tasks()


@app.delete("/tasks/{title}")
def delete_task(title: str):
    """
    Delete a task by title.
    """
    task_manager.remove_task(title)
    return {"message": f"Task '{title}' removed successfully."}


@app.get("/tasks/search")
def search_tasks(keyword: str):
    """
    Search for tasks by keyword in title.
    """
    tasks = task_manager.get_task_by_title(keyword)
    if not tasks:
        raise HTTPException(status_code=404, detail=f"No tasks found with keyword '{keyword}'")
    return tasks


@app.patch("/tasks/{title}/complete")
def complete_task(title: str):
    """
    Mark a task as completed by title.
    """
    tasks = task_manager.get_task_by_title(title)
    if not tasks:
        raise HTTPException(status_code=404, detail=f"No task found with title '{title}'")

    task = tasks[0]
    task.mark_completed()
    return {"message": f"Task '{task.title}' marked as completed."}


@app.patch("/tasks/{title}/incomplete")
def incomplete_task(title: str):
    """
    Mark a task as incomplete by title.
    """
    tasks = task_manager.get_task_by_title(title)
    if not tasks:
        raise HTTPException(status_code=404, detail=f"No task found with title '{title}'")

    task = tasks[0]
    task.mark_incomplete()
    return {"message": f"Task '{task.title}' marked as incomplete."}


@app.get("/tasks/filter")
def filter_tasks(
    keyword: Union[str, None] = None,
    category: Union[str, None] = None,
    priority: Union[str, None] = None,
):
    """
    Filter tasks by keyword in title, category, or priority.
    """
    if keyword:
        tasks = task_manager.get_task_by_title(keyword)
    elif category:
        tasks = task_manager.get_tasks(lambda t: t.category == category)
    elif priority:
        tasks = task_manager.get_tasks(lambda t: t.priority.value == priority)
    else:
        tasks = task_manager.get_tasks()

    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found with the given filters")

    return tasks


@app.post("/tasks/save")
def save_task(path: Annotated[str, "Path to the task storage file"] = "test_fapi.json"):
    """Save tasks to storage."""
    task_storage = TaskStorage(path)
    task_storage.save_tasks(task_manager)
    return {"message": "Tasks saved successfully."}


@app.post("/tasks/load")
def load_task(path: Annotated[str, "Path to the task storage file"] = "test.json"):
    """
    Load tasks from storage.
    """
    task_storage = TaskStorage(path)
    task_storage.load_tasks(task_manager)
    return {"message": "Tasks loaded successfully."}


@app.get("/tasks/{title}")
def get_task_by_title(title: str):
    """
    Retrieve a task by its title.
    """
    tasks = task_manager.get_task_by_title(title)
    if not tasks:
        raise HTTPException(status_code=404, detail=f"No task found with title '{title}'")
    return tasks[0].to_dict()


# @app.get("/tasks/recurring")
# def get_recurring_tasks():
#     """
#     Retrieve all recurring tasks.
#     """
#     recurring_tasks = task_manager.get_tasks(lambda t: isinstance(t, RecurringTask))
#     if not recurring_tasks:
#         raise HTTPException(status_code=404, detail="No recurring tasks found")
#     return [task.to_dict() for task in recurring_tasks]

# @app.post("/tasks/recurring", response_model=RecurringTask)
# def create_recurring_task(task: RecurringTask):
#     """
#     Create a new recurring task.
#     """
#     t = RecurringTask(
#         title=task.title,
#         description=task.description,
#         due_date=task.due_date,
#         completed=task.completed,
#         category=task.category,
#         priority=Priority(task.priority) if isinstance(task.priority, str) else task.priority,
#         recurrence=task.recurrence
#     )
#     task_manager.add_task(
#         t.title, t.description, t.due_date, t.completed, t.category, t.priority, t.recurrence
#     )
#     return t.to_dict()

# @app.delete("/tasks/recurring/{title}")
# def delete_recurring_task(title: str):
#     """
#     Delete a recurring task by title.
#     """
#     task_manager.remove_task(title)
#     return {"message": f"Recurring task '{title}' removed successfully."}

# @app.get("/tasks/recurring/search")
# def search_recurring_tasks(keyword: str):
#     """
#     Search for recurring tasks by keyword in title.
#     """
#     tasks = task_manager.get_task_by_title(keyword)
#     recurring_tasks = [task for task in tasks if isinstance(task, RecurringTask)]
#     if not recurring_tasks:
#         raise HTTPException(status_code=404, detail=f"No recurring tasks found with keyword '{keyword}'")
#     return [task.to_dict() for task in recurring_tasks]

# @app.patch("/tasks/recurring/{title}/complete")
# def complete_recurring_task(title: str):
#     """
#     Mark a recurring task as completed by title.
#     """
#     tasks = task_manager.get_task_by_title(title)
#     recurring_tasks = [task for task in tasks if isinstance(task, RecurringTask)]
#     if not recurring_tasks:
#         raise HTTPException(status_code=404, detail=f"No recurring task found with title '{title}'")

#     task = recurring_tasks[0]
#     task.mark_completed()
#     return {"message": f"Recurring task '{task.title}' marked as completed."}

# @app.patch("/tasks/recurring/{title}/incomplete")
# def incomplete_recurring_task(title: str):
#     """
#     Mark a recurring task as incomplete by title.
#     """
#     tasks = task_manager.get_task_by_title(title)
#     recurring_tasks = [task for task in tasks if isinstance(task, RecurringTask)]
#     if not recurring_tasks:
#         raise HTTPException(status_code=404, detail=f"No recurring task found with title '{title}'")

#     task = recurring_tasks[0]
#     task.mark_incomplete()
#     return {"message": f"Recurring task '{task.title}' marked as incomplete."}

# @app.get("/tasks/recurring/filter")
# def filter_recurring_tasks(
#     keyword: Union[str, None] = None,
#     category: Union[str, None] = None,
#     priority: Union[str, None] = None
# ):
#     """
#     Filter recurring tasks by keyword in title, category, or priority.
#     """
#     recurring_tasks = task_manager.get_tasks(lambda t: isinstance(t, RecurringTask))

#     if keyword:
#         tasks = [task for task in recurring_tasks if keyword.lower() in task.title.lower()]
#     elif category:
#         tasks = [task for task in recurring_tasks if task.category == category]
#     elif priority:
#         tasks = [task for task in recurring_tasks if task.priority == priority]
#     else:
#         tasks = recurring_tasks

#     if not tasks:
#         raise HTTPException(status_code=404, detail="No recurring tasks found with the given filters")

#     return [task.to_dict() for task in tasks]

# @app.get("/tasks/recurring/{title}", response_model=RecurringTask)
# def get_recurring_task_by_title(title: str):
#     """
#     Retrieve a recurring task by its title.
#     """
#     tasks = task_manager.get_task_by_title(title)
#     recurring_tasks = [task for task in tasks if isinstance(task, RecurringTask)]
#     if not recurring_tasks:
#         raise HTTPException(status_code=404, detail=f"No recurring task found with title '{title}'")
#     return recurring_tasks[0].to_dict()
