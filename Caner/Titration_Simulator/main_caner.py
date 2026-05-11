"""
main_caner.py
Authors: Caner and Joe

Main file for the Acid-Base Titration Simulator.

Caner mainly worked on:
- main_caner.py
- validation_caner.py
- gui_caner.py

Joe mainly worked on:
- reaction_joe.py
- calculations_joe.py
- plotting_joe.py

This program opens a Tkinter application that simulates acid-base titration
curves and displays the graph using matplotlib.
"""

import tkinter as tk
from tkinter import messagebox

from Caner.Titration_Simulator.gui_caner import TitrationApp

def main():
    try:
        root = tk.Tk()
        root.title("Acid-Base Titration Simulator")
        root.geometry("950x650")
        root.minsize(850, 550)

        app = TitrationApp(root)
        app.run()

    except Exception as error:
        messagebox.showerror(
            "Program Error",
            f"Something went wrong:\n\n{error}"
        )


if __name__ == "__main__":
    main()