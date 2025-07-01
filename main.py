from typing import Annotated, List, Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from storage import TaskStorage
from task import AnyTask, Priority, RecurringTask, Task
from task_manager import TaskManager

app = FastAPI(
    title="TaskManager API", description="A simple API to manage tasks.", version="1.0.0"
)

# CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

task_manager = TaskManager()


class TaskCreate(BaseModel):
    title: str
    description: Union[str, None] = None
    due_date: str  # Assuming date is in 'YYYY-MM-DD' format
    category: Union[str, None] = None
    priority: Priority = Priority.MEDIUM  # Default priority


class RecurringTaskCreate(TaskCreate):
    recurrence: str  # Recurrence pattern, e.g., "daily", "weekly", "monthly"


@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Manager API"}


@app.get("/tasks", response_model=List[AnyTask])
def get_tasks():
    """
    Retrieve all tasks.
    """
    return task_manager.get_tasks()


@app.post("/tasks", response_model=Task)
def create_task(task_create: TaskCreate):
    """
    Create a new task.
    """
    task = Task(**task_create.model_dump())
    task_manager.add_task(task)
    return task


@app.post("/tasks/recurring", response_model=RecurringTask)
def create_recurring_task(task_create: RecurringTaskCreate):
    """
    Create a new recurring task.
    """
    task = RecurringTask(**task_create.model_dump())
    task_manager.add_task(task)
    return task


@app.delete("/tasks/{title}", status_code=204)
def delete_task(title: str):
    """
    Delete a task by title.
    """
    if not task_manager.remove_task(title):
        raise HTTPException(status_code=404, detail=f"Task '{title}' not found")
    return {"message": f"Task '{title}' removed successfully."}


@app.get("/tasks/search", response_model=List[AnyTask])
def search_tasks(keyword: str):
    """
    Search for tasks by keyword in title.
    """
    tasks = task_manager.get_task_by_title(keyword)
    if not tasks:
        raise HTTPException(status_code=404, detail=f"No tasks found with keyword '{keyword}'")
    return tasks


@app.patch("/tasks/{title}/complete", response_model=AnyTask)
def complete_task(title: str):
    """
    Mark a task as completed by title.
    """
    tasks = task_manager.get_task_by_title(title)
    if not tasks:
        raise HTTPException(status_code=404, detail=f"No task found with title '{title}'")
    task = tasks[0]
    task.mark_completed()
    return task


@app.patch("/tasks/{title}/incomplete", response_model=AnyTask)
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


@app.get("/tasks/filter", response_model=List[AnyTask])
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
        tasks = task_manager.get_tasks(lambda t: t.category.lower() == category.lower())
    elif priority:
        tasks = task_manager.get_tasks(lambda t: t.priority.value.lower() == priority.lower())
    else:
        tasks = task_manager.get_tasks()

    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found with the given filters")

    return tasks


@app.post("/tasks/save")
def save_task(path: Annotated[str, "Path to the task storage file"] = "test_fapi.json"):
    """Save tasks to storage."""
    TaskStorage(path).save_tasks(task_manager)
    return {"message": f"Tasks saved successfully to {path}"}


@app.post("/tasks/load")
def load_task(path: Annotated[str, "Path to the task storage file"] = "test.json"):
    """
    Load tasks from storage.
    """
    TaskStorage(path).load_tasks(task_manager)
    return {"message": "Tasks loaded successfully."}


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
