import json
import os

FILE = "tasks.json"

# -----------------------------
# File handling
# -----------------------------
def load_tasks():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# -----------------------------
# Core features
# -----------------------------
def add_task():
    title = input("Task name: ")
    task_type = input("Type (homework/exam/project): ").lower()
    deadline = input("Deadline (YYYY-MM-DD): ")

    tasks = load_tasks()

    tasks.append({
        "title": title,
        "type": task_type,
        "deadline": deadline,
        "done": False
    })

    save_tasks(tasks)
    print("✅ Task added!")

def view_tasks():
    tasks = load_tasks()

    if not tasks:
        print("No tasks yet.")
        return

    # Sort by deadline
    tasks.sort(key=lambda x: x["deadline"])

    print("\nAll tasks:\n")

    for i, task in enumerate(tasks):
        status = "✅" if task["done"] else "❌"
        print(f"{i}. [{task['type'].upper()}] {task['title']} | {task['deadline']} | {status}")

def view_by_type():
    tasks = load_tasks()

    if not tasks:
        print("No tasks available.")
        return

    selected = input("Enter type (homework/exam/project): ").lower()

    filtered = [t for t in tasks if t["type"] == selected]

    if not filtered:
        print("No tasks of this type.")
        return

    filtered.sort(key=lambda x: x["deadline"])

    print(f"\n{selected.upper()} tasks:\n")

    for i, task in enumerate(filtered):
        status = "✅" if task["done"] else "❌"
        print(f"{i}. {task['title']} | {task['deadline']} | {status}")

def complete_task():
    tasks = load_tasks()

    if not tasks:
        print("No tasks to complete.")
        return

    view_tasks()

    try:
        index = int(input("\nEnter task number: "))
        tasks[index]["done"] = True
        save_tasks(tasks)
        print("🎉 Task completed!")
    except:
        print("Invalid input.")

# -----------------------------
# Main loop
# -----------------------------
def main():
    print("=== StudentHub v0.2-alpha ===")

    while True:
        print("\nMenu:")
        print("1. Add task")
        print("2. View all tasks")
        print("3. Complete task")
        print("4. View by type")
        print("5. Exit")

        choice = input("> ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            view_by_type()
        elif choice == "5":
            print("Goodbye 👋")
            wait: 2
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()