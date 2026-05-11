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

from .validation_caner import (
    TITRATION_TYPES,
    validate_inputs,
    validate_filename,
    get_strong_acid_example,
    get_weak_acid_example,
    get_blank_inputs
)

from Joe.Titration_Simulator.calculations_joe import calculate_titration
from Joe.Titration_Simulator.plotting_joe import Plotter


class TitrationApp:
    def __init__(self, root):
        self.root = root
        self.entries = {}
        self.titration_type = tk.StringVar()
        self.results_text = tk.StringVar(value="No results yet.")

        self.last_result = None
        self.last_figure = None
        self.canvas = None
        self.plotter = Plotter()

        self.build_gui()
        self.load_weak_example()

    def build_gui(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)

        title = tk.Label(
            main_frame,
            text="Acid-Base Titration Simulator",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(0, 10))

        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)

        self.left_frame = tk.Frame(content_frame)
        self.left_frame.pack(side="left", fill="y", padx=(0, 10))

        self.graph_frame = tk.LabelFrame(
            content_frame,
            text="Titration Curve",
            padx=5,
            pady=5
        )
        self.graph_frame.pack(side="right", fill="both", expand=True)

        self.build_inputs()
        self.build_buttons()
        self.build_results()
        self.show_placeholder()

    def build_inputs(self):
        input_frame = tk.LabelFrame(
            self.left_frame,
            text="Input Values",
            padx=10,
            pady=10
        )
        input_frame.pack(fill="x")

        tk.Label(input_frame, text="Titration type").grid(
            row=0,
            column=0,
            sticky="w",
            pady=4
        )

        type_box = ttk.Combobox(
            input_frame,
            textvariable=self.titration_type,
            values=TITRATION_TYPES,
            state="readonly",
            width=25
        )
        type_box.grid(row=0, column=1, pady=4)

        fields = [
            ("Acid concentration / mol dm⁻³", "acid_concentration"),
            ("Acid volume / cm³", "acid_volume"),
            ("Base concentration / mol dm⁻³", "base_concentration"),
            ("Maximum base volume / cm³", "max_base_volume"),
            ("Selected base volume / cm³", "selected_volume"),
            ("Graph points", "graph_points"),
            ("pKa, weak acid only", "pka")
        ]

        for row, field in enumerate(fields, start=1):
            label_text, key = field

            tk.Label(input_frame, text=label_text).grid(
                row=row,
                column=0,
                sticky="w",
                pady=4
            )

            entry = tk.Entry(input_frame, width=20)
            entry.grid(row=row, column=1, pady=4)
            self.entries[key] = entry

    def build_buttons(self):
        button_frame = tk.LabelFrame(
            self.left_frame,
            text="Actions",
            padx=10,
            pady=10
        )
        button_frame.pack(fill="x", pady=10)

        buttons = [
            ("Calculate", self.calculate),
            ("Load strong example", self.load_strong_example),
            ("Load weak example", self.load_weak_example),
            ("Clear", self.clear_inputs),
            ("Export graph", self.export_graph),
            ("Export data", self.export_data),
            ("About", self.show_about)
        ]

        for text, command in buttons:
            tk.Button(
                button_frame,
                text=text,
                command=command,
                width=22
            ).pack(pady=2)

    def build_results(self):
        results_frame = tk.LabelFrame(
            self.left_frame,
            text="Results",
            padx=10,
            pady=10
        )
        results_frame.pack(fill="both", expand=True)

        tk.Label(
            results_frame,
            textvariable=self.results_text,
            justify="left",
            anchor="nw",
            width=38
        ).pack(fill="both", expand=True)

    def set_values(self, values):
        self.titration_type.set(values["titration_type"])

        for entry in self.entries.values():
            entry.delete(0, tk.END)

        for key, value in values.items():
            if key != "titration_type":
                self.entries[key].insert(0, value)

    def get_raw_inputs(self):
        return {
            "titration_type": self.titration_type.get(),
            "acid_concentration": self.entries["acid_concentration"].get(),
            "acid_volume": self.entries["acid_volume"].get(),
            "base_concentration": self.entries["base_concentration"].get(),
            "max_base_volume": self.entries["max_base_volume"].get(),
            "selected_volume": self.entries["selected_volume"].get(),
            "graph_points": self.entries["graph_points"].get(),
            "pka": self.entries["pka"].get()
        }

    def calculate(self):
        try:
            data = validate_inputs(self.get_raw_inputs())
            result = calculate_titration(data)

            figure = self.plotter.create_single_curve_figure(
                result["curve_data"],
                result["key_points"],
                result["selected_point"],
                result["data"]
            )

            self.last_result = result
            self.last_figure = figure

            self.show_results(result)
            self.show_graph(figure)

        except ValueError as error:
            messagebox.showerror("Input Error", str(error))

        except Exception as error:
            messagebox.showerror("Calculation Error", str(error))

    def show_results(self, result):
        key = result["key_points"]
        selected = result["selected_point"]
        reaction = result["reaction"]

        lines = [
            f"Initial pH: {key['initial_ph']:.2f}",
            f"Equivalence volume: {key['equivalence_volume']:.2f} cm³",
            f"Equivalence pH: {key['equivalence_ph']:.2f}",
            f"Half-equivalence volume: {key['half_equivalence_volume']:.2f} cm³"
        ]

        if key["half_equivalence_ph"] is not None:
            lines.append(f"Half-equivalence pH: {key['half_equivalence_ph']:.2f}")
        else:
            lines.append("Half-equivalence pH: not used")

        lines += [
            "",
            f"Selected volume: {selected['volume']:.2f} cm³",
            f"Selected pH: {selected['ph']:.2f}",
            f"Region: {selected['region']}",
            "",
            "Reaction:",
            reaction["ionic_equation"],
            reaction["note"]
        ]

        self.results_text.set("\n".join(lines))

    def clear_graph(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        self.canvas = None

    def show_placeholder(self):
        self.clear_graph()

        tk.Label(
            self.graph_frame,
            text="Graph will appear here after calculation."
        ).pack(expand=True)

    def show_graph(self, figure):
        self.clear_graph()

        self.canvas = FigureCanvasTkAgg(
            figure,
            master=self.graph_frame
        )

        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def load_strong_example(self):
        self.set_values(get_strong_acid_example())

    def load_weak_example(self):
        self.set_values(get_weak_acid_example())

    def clear_inputs(self):
        self.set_values(get_blank_inputs())
        self.results_text.set("No results yet.")

        self.last_result = None
        self.last_figure = None

        self.show_placeholder()

    def export_graph(self):
        if self.last_figure is None:
            messagebox.showinfo("Export graph", "Please calculate a graph first.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG image", "*.png")]
        )

        if filename == "":
            return

        try:
            filename = validate_filename(filename, ".png")
            self.plotter.save_figure(self.last_figure, filename)

        except ValueError as error:
            messagebox.showerror("Export Error", str(error))

    def export_data(self):
        if self.last_result is None:
            messagebox.showinfo("Export data", "Please calculate data first.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV file", "*.csv")]
        )

        if filename == "":
            return

        try:
            filename = validate_filename(filename, ".csv")
            self.plotter.export_curve_data(
                filename,
                self.last_result["curve_data"]
            )

        except ValueError as error:
            messagebox.showerror("Export Error", str(error))

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Acid-Base Titration Simulator\n\n"
            "This application simulates titration curves for:\n"
            "- strong acid vs strong base\n"
            "- weak acid vs strong base\n\n"
            "It calculates pH, equivalence point, half-equivalence point, "
            "and plots the curve using matplotlib."
        )

    def run(self):
        self.root.mainloop()