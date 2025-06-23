from storage import TaskStorage
from task_manager import TaskManager


def main_menu():
    print("Welcome to TaskManager!")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Complete Task")
    print("4. Remove Task")
    print("5. Filter Tasks")
    print("6. Sort Tasks")
    print("7. Save Tasks")
    print("8. Load Tasks")
    print("9. Exit")


def run_cli():
    task_manager = TaskManager()
    # task_storage = TaskStorage()
    while True:
        main_menu()
        choice = input("Please select an option (1-5): ")
        if choice == "1":
            print("You selected Option 1.")
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            due_date = input("Enter task due date: ")
            category = input("Enter task category (optional): ")
            priority = input("Enter task priority (optional): ")
            task_manager.add_task(
                title, description, due_date, category=category, priority=priority
            )
        elif choice == "2":
            print("You selected Option 2.")
            tasks = task_manager.get_tasks()
            print(f"Current Tasks: {tasks}")
        elif choice == "3":
            print("You selected Option 3.")
            title = input("Enter the title of the task to complete: ")
            tasks = task_manager.get_task_by_title(title)
            if tasks:
                task = tasks[0]
                task.mark_completed()
                print(f"Task '{task.title}' marked as completed.")
            else:
                print(f"No task found with title '{title}'.")
        elif choice == "4":
            print("You selected Option 4.")
            title = input("Enter the title of the task to remove: ")
            task_manager.remove_task(title)
            # Assuming remove_task updates the task list and saves it to the storage.
            print(f"Task '{title}' removed.")
        elif choice == "5":
            print("You selected Option 5.")
            print("Choose a filter option:")
            print("1. Filter by keyword in title")
            print("2. Filter by category")
            print("3. Filter by priority")
            filter_choice = input("Please select an option (1-3): ")
            if filter_choice == "1":
                print("You selected to filter by keyword in title.")
                keyword = input("Enter a keyword to filter tasks by title: ")
                filtered_tasks = task_manager.get_task_by_title(keyword)
                if filtered_tasks:
                    print(f"Filtered Tasks: {filtered_tasks}")
                else:
                    print(f"No tasks found with keyword '{keyword}'.")

            elif filter_choice == "2":
                print("You selected to filter by category.")
                category = input("Enter a category to filter tasks: ")
                filtered_tasks = [
                    task for task in task_manager.get_tasks(lambda t: t.category == category)
                ]
                if filtered_tasks:
                    print(f"Filtered Tasks: {filtered_tasks}")
                else:
                    print(f"No tasks found in category '{category}'.")
            elif filter_choice == "3":
                print("You selected to filter by priority.")
                priority = input("Enter a priority to filter tasks: ")
                filtered_tasks = [
                    task for task in task_manager.get_tasks(lambda t: t.priority == priority)
                ]
                if filtered_tasks:
                    print(f"Filtered Tasks: {filtered_tasks}")
                else:
                    print(f"No tasks found with priority '{priority}'.")

        elif choice == "6":
            print("You selected Option 6.")
            print("Choose a sort option:")
            print("1. Sort by title")
            print("2. Sort by due date")
            print("3. Sort by priority")
            sort_choice = input("Please select an option (1-3): ")
            if sort_choice == "1":
                sorted_tasks = sorted(task_manager.get_tasks(), key=lambda x: x.title)
                print(f"Tasks sorted by title: {sorted_tasks}")
            elif sort_choice == "2":
                sorted_tasks = sorted(task_manager.get_tasks(), key=lambda x: x.due_date)
                print(f"Tasks sorted by due date: {sorted_tasks}")
            elif sort_choice == "3":
                sorted_tasks = sorted(task_manager.get_tasks(), key=lambda x: x.priority)
                print(f"Tasks sorted by priority: {sorted_tasks}")
            else:
                print("Invalid choice, please try again.")

        elif choice == "7":
            print("You selected Option 7.")
            filename = input("Enter the filename to save tasks to (default is 'tasks.json'): ")
            task_storage = TaskStorage(filename)
            task_storage.save_tasks(task_manager)
            print("Tasks saved successfully.")
        elif choice == "8":
            print("You selected Option 8.")
            filename = input("Enter the filename to load tasks from (default is 'tasks.json'): ")
            task_storage = TaskStorage(filename)
            task_storage.load_tasks(task_manager)
            print("Tasks loaded successfully.")
        elif choice == "9":
            print("Exiting TaskManager. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    run_cli()
