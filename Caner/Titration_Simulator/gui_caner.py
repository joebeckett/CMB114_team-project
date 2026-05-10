"""
gui_caner.py
Author: Caner

This file creates the Tkinter interface for the titration simulator.

It handles the input boxes, buttons, result display, graph display and export
options. The chemistry calculations are handled in Joe's files.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from validation_caner import (
    TITRATION_TYPES,
    validate_inputs,
    validate_filename,
    get_strong_acid_example,
    get_weak_acid_example,
    get_blank_inputs
)

from Joe.Titration_Simulator.calculations_joe import calculate_titration
from Joe.Titration_Simulator.plotting_joe import PLotter