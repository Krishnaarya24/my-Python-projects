
#  TO DO LIST



import json
import os
from datetime import datetime

TASK_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(TASK_FILE):
        try:
            with open(TASK_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading tasks:", e)
    return []

# Save tasks to file
def save_tasks(tasks):
    try:
        with open(TASK_FILE, "w") as f:
            json.dump(tasks, f, indent=4)
    except Exception as e:
        print("Error saving tasks:", e)

# Add a new task
def add_task(tasks):
    title = input("Enter task title: ").strip()
    due_date = input("Enter due date (YYYY-MM-DD): ").strip()
    priority = input("Enter priority (High/Medium/Low): ").strip().capitalize()

    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    task = {
        "title": title,
        "due_date": due_date,
        "priority": priority,
        "completed": False
    }

    tasks.append(task)
    save_tasks(tasks)
    print("✅ Task added successfully!\n")

# View tasks
def view_tasks(tasks):
    if not tasks:
        print("No tasks found.\n")
        return

    print("\n--- Task List ---")
    for i, task in enumerate(tasks, 1):
        status = "✅ Done" if task["completed"] else "⏳ Pending"
        due_date = datetime.strptime(task["due_date"], "%Y-%m-%d")
        if not task["completed"] and due_date < datetime.now():
            status = "⚠️ Overdue"
        print(f"{i}. {task['title']} | Due: {task['due_date']} | Priority: {task['priority']} | Status: {status}")
    print()

# Mark task as completed
def complete_task(tasks):
    view_tasks(tasks)
    try:
        idx = int(input("Enter task number to mark as completed: ")) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]["completed"] = True
            save_tasks(tasks)
            print("✅ Task marked as completed!\n")
        else:
            print("Invalid task number.\n")
    except Exception:
        print("Please enter a valid number.\n")

# Delete a task
def delete_task(tasks):
    view_tasks(tasks)
    try:
        idx = int(input("Enter task number to delete: ")) - 1
        if 0 <= idx < len(tasks):
            removed = tasks.pop(idx)
            save_tasks(tasks)
            print(f"🗑️ Task '{removed['title']}' deleted.\n")
        else:
            print("Invalid task number.\n")
    except Exception:
        print("Please enter a valid number.\n")

# View stats
def view_stats(tasks):
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    pending = total - completed
    overdue = sum(1 for t in tasks if not t["completed"] and datetime.strptime(t["due_date"], "%Y-%m-%d") < datetime.now())

    print("\n--- Task Stats ---")
    print(f"📌 Total tasks: {total}")
    print(f"✅ Completed: {completed}")
    print(f"⏳ Pending: {pending}")
    print(f"⚠️ Overdue: {overdue}\n")

# Menu
def menu():
    tasks = load_tasks()
    while True:
        print("=== Task Manager ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. View Stats")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            view_stats(tasks)
        elif choice == "6":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please try again.\n")

# Run the app
if __name__ == "__main__":
    menu()
