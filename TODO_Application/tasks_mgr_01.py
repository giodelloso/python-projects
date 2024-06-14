#!/usr/bin/env python

import pickle
import tkinter as tk
from tkinter import messagebox, simpledialog


class TodoApp:
    """
    A simple Todo List Application using Tkinter for GUI and Pickle for data
    storage.

    Attributes:
        root (tk.Tk): The main application window.
        tasks (list): List to store tasks.
        task_entry (tk.Entry): Entry widget to input new tasks.
        add_task_button (tk.Button): Button to add tasks.
        edit_task_button (tk.Button): Button to edit selected task.
        delete_task_button (tk.Button): Button to delete selected task.
        complete_task_button (tk.Button): Button to mark selected task as
            completed.
        task_listbox (tk.Listbox): Listbox to display tasks.
    """

    def __init__(self, root):
        """
        Initialize the TodoApp with the main window and its widgets.

        Args:
            root (tk.Tk): The main application window.
        """
        self.root = root
        self.root.title("Todo List Application")

        self.tasks = []
        self.load_tasks()

        self.task_entry = tk.Entry(root, width=50)
        self.task_entry.pack(pady=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)

        self.add_task_button = tk.Button(
            self.button_frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack(side=tk.LEFT, padx=5)

        self.edit_task_button = tk.Button(
            self.button_frame, text="Edit Task", command=self.edit_task)
        self.edit_task_button.pack(side=tk.LEFT, padx=5)

        self.delete_task_button = tk.Button(
            self.button_frame, text="Delete Task", command=self.delete_task)
        self.delete_task_button.pack(side=tk.LEFT, padx=5)

        self.complete_task_button = tk.Button(
            self.button_frame, text="Complete Task", command=self.complete_task)
        self.complete_task_button.pack(side=tk.LEFT, padx=5)

        self.task_listbox = tk.Listbox(root, width=50, height=10)
        self.task_listbox.pack(pady=10)

        self.update_task_listbox()

    def add_task(self):
        """
        Add a new task to the task list and update the listbox.
        """
        task = self.task_entry.get()
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
            self.save_tasks()

    def edit_task(self):
        """
        Edit the selected task in the task list and update the listbox.
        """
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            new_task = simpledialog.askstring(
                "Edit Task",
                "Edit the task:",
                initialvalue=self.tasks[selected_task_index]["task"])
            if new_task:
                self.tasks[selected_task_index]["task"] = new_task
                self.update_task_listbox()
                self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "No task selected")

    def delete_task(self):
        """
        Delete the selected task from the task list and update the listbox.
        """
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.tasks.pop(selected_task_index)
            self.update_task_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "No task selected")

    def complete_task(self):
        """
        Mark the selected task as completed and update the listbox.
        """
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.tasks[selected_task_index]["completed"] = True
            self.update_task_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "No task selected")

    def update_task_listbox(self):
        """
        Update the listbox to display the current list of tasks.
        """
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            display_text = task["task"]
            if task["completed"]:
                display_text += " (Completed)"
            self.task_listbox.insert(tk.END, display_text)

    def save_tasks(self):
        """
        Save the current list of tasks to a file using pickle.
        """
        with open("tasks.pkl", "wb") as f:
            pickle.dump(self.tasks, f)

    def load_tasks(self):
        """
        Load the list of tasks from a file using pickle. If the file does
        not exist, initialize an empty list.
        """
        try:
            with open("tasks.pkl", "rb") as f:
                self.tasks = pickle.load(f)
        except FileNotFoundError:
            self.tasks = []


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
