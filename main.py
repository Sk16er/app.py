import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import time

# Initialize the main window
root = tk.Tk()
root.title("To-Do List Application")
root.geometry("800x600")

# Set the theme for CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create the main frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Create a label for the title
title_label = ctk.CTkLabel(main_frame, text="To-Do List", font=("Helvetica", 24))
title_label.pack(pady=10)

# Initialize the database
def init_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        category TEXT,
        due_date TEXT,
        completed BOOLEAN NOT NULL DEFAULT 0
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

init_db()# Function to add a new task
def add_task():
    task = task_entry.get()
    category = category_entry.get()
    due_date = due_date_entry.get()
    if task:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todos (task, category, due_date) VALUES (?, ?, ?)", (task, category, due_date))
        conn.commit()
        conn.close()
        display_tasks()
        task_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        due_date_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Enter a task.")

# Function to display tasks
def display_tasks():
    for widget in tasks_frame.winfo_children():
        widget.destroy()

    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        task_var = tk.BooleanVar(value=row[4])
        task_check = ctk.CTkCheckBox(tasks_frame, text=row[1], variable=task_var, command=lambda r=row: toggle_task(r[0], task_var.get()))
        task_check.pack(pady=5)
        if row[2]:
            category_label = ctk.CTkLabel(tasks_frame, text=f"Category: {row[2]}")
            category_label.pack(pady=5)
        if row[3]:
            due_date_label = ctk.CTkLabel(tasks_frame, text=f"Due: {row[3]}")
            due_date_label.pack(pady=5)
        edit_button = ctk.CTkButton(tasks_frame, text="Edit", command=lambda r=row: edit_task(r[0], r[1], r[2], r[3]))
        edit_button.pack(pady=5)

# Function to toggle task completion
def toggle_task(task_id, completed):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET completed = ? WHERE id = ?", (completed, task_id))
    conn.commit()
    conn.close()
    display_tasks()

# Function to edit a task
def edit_task(task_id, old_task, old_category, old_due_date):
    def save_task():
        new_task = edit_entry.get()
        new_category = edit_category_entry.get()
        new_due_date = edit_due_date_entry.get()
        if new_task:
            conn = sqlite3.connect('todo.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE todos SET task = ?, category = ?, due_date = ? WHERE id = ?", (new_task, new_category, new_due_date, task_id))
            conn.commit()
            conn.close()
            edit_window.destroy()
            display_tasks()
        else:
            messagebox.showwarning("Warning", "Enter a task.")

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Task")
    edit_entry = ctk.CTkEntry(edit_window, width=300)
    edit_entry.insert(0, old_task)
    edit_entry.pack(pady=10)
    edit_category_entry = ctk.CTkEntry(edit_window, width=300)
    edit_category_entry.insert(0, old_category)
    edit_category_entry.pack(pady=10)
    edit_due_date_entry = ctk.CTkEntry(edit_window, width=300)
    edit_due_date_entry.insert(0, old_due_date)
    edit_due_date_entry.pack(pady=10)
    save_button = ctk.CTkButton(edit_window, text="Save", command=save_task)
    save_button.pack(pady=10)

# Function to delete all tasks
def delete_all_tasks():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos")
    conn.commit()
    conn.close()
    display_tasks()

# Function to search tasks
def search_tasks():
    search_term = search_entry.get()
    for widget in tasks_frame.winfo_children():
        widget.destroy()

    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos WHERE task LIKE ?", ('%' + search_term + '%',))
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        task_var = tk.BooleanVar(value=row[4])
        task_check = ctk.CTkCheckBox(tasks_frame, text=row[1], variable=task_var, command=lambda r=row: toggle_task(r[0], task_var.get()))
        task_check.pack(pady=5)
        if row[2]:
            category_label = ctk.CTkLabel(tasks_frame, text=f"Category: {row[2]}")
            category_label.pack(pady=5)
        if row[3]:
            due_date_label = ctk.CTkLabel(tasks_frame, text=f"Due: {row[3]}")
            due_date_label.pack(pady=5)
        edit_button = ctk.CTkButton(tasks_frame, text="Edit", command=lambda r=row: edit_task(r[0], r[1], r[2], r[3]))
        edit_button.pack(pady=5)# Add task entry and button
task_entry = ctk.CTkEntry(main_frame, width=300, placeholder_text="Enter task")
task_entry.pack(padx=10, pady=5)
category_entry = ctk.CTkEntry(main_frame, width=300, placeholder_text="Category")
category_entry.pack(padx=10, pady=5)
due_date_entry = ctk.CTkEntry(main_frame, width=300, placeholder_text="Due Date (YYYY-MM-DD)")
due_date_entry.pack(padx=10, pady=5)
add_task_button = ctk.CTkButton(main_frame, text="Add Task", command=add_task)
add_task_button.pack(padx=10, pady=5)

# Frame to display tasks
tasks_frame = ctk.CTkFrame(main_frame)
tasks_frame.pack(pady=20, fill="both", expand=True)
display_tasks()

# Add delete all tasks button
delete_all_button = ctk.CTkButton(root, text="Delete All Tasks", command=delete_all_tasks)
delete_all_button.pack(pady=10)

# Add search entry and button
search_entry = ctk.CTkEntry(main_frame, width=300, placeholder_text="Search")
search_entry.pack(padx=10, pady=5)
search_button = ctk.CTkButton(main_frame, text="Search", command=search_tasks)
search_button.pack(padx=10, pady=5)

# Add dark mode toggle
def toggle_dark_mode():
    if ctk.get_appearance_mode() == "dark":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

dark_mode_button = ctk.CTkButton(root, text="Toggle Dark Mode", command=toggle_dark_mode)
dark_mode_button.pack(pady=10)

# Track and display usage data
start_time = time.time()

def display_usage():
    end_time = time.time()
    total_time = end_time - start_time
    usage_label.config(text=f"Total Usage Time: {int(total_time)} seconds")

usage_label = ctk.CTkLabel(root, text="Total Usage Time: 0 seconds", font=("Helvetica", 16))
usage_label.pack(pady=10)

def update_usage():
    display_usage()
    root.after(1000, update_usage)

update_usage()

root.mainloop()
