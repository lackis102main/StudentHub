import json
import os

FILE = "tasks.json"

if not os.path.exists(FILE):
    with open(FILE, "w") as f:
        f.write("[]")  # initialize empty list

def load_tasks():
    if not os.path.exists(FILE):
        return []  # File missing → return empty list

    with open(FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # File is empty or corrupted → reset it
            return []

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task():
    title = input("Task name: ")
    deadline = input("Deadline (YYYY-MM-DD): ")

    tasks = load_tasks()
    tasks.append({
        "title": title,
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

    print("\nYour tasks:\n")

    for i, task in enumerate(tasks):
        status = "✅" if task["done"] else "❌"
        print(f"{i}. {task['title']} | Due: {task['deadline']} | {status}")

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

def main():
    while True:
        print("\n=== StudyHub v1 ===")
        print("1. Add task")
        print("2. View tasks")
        print("3. Complete task")
        print("4. Exit")

        choice = input("> ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            print("Bye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()