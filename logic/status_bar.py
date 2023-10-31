import tkinter as tk
from tkinter import ttk


def create_progressbar(frame, max_value):
    # Create the Tkinter window

    # Create a progress bar
    progress = ttk.Progressbar(frame, mode="determinate", maximum=max_value)
    progress.pack()

    # Function to update the progress bar
    def update_progress(value):
        progress["value"] = value

    # Function to update the maximum value
    def update_max_value(new_max_value):
        progress.configure(maximum=new_max_value)

    return update_progress
