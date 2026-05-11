"""
plotting_joe.py
Author: Joe

This file handles matplotlib plotting and export.

This file creates the titration curve, marks the equivalence point, the
half-equivalence point for weak acids, the selected volume and exports
curve data as CSV.
"""

import csv

from matplotlib.figure import Figure


class Plotter:
    
    """
    Plotter class for titration graphs and exports
    """

    def create_base_figure(self):
        
        """
        Creates the base matplotlib figure and axis
        """

        figure = Figure(
            figsize=(7, 5),
            dpi=100
        )

        axis = figure.add_subplot(111)

        return figure, axis

    def setup_axis(self, axis, title):
        
        """
        Adds the graph title, axis labels, grid and pH limits
        """

        axis.set_title(title)
        axis.set_xlabel("Volume of base added / cm³")
        axis.set_ylabel("pH")
        axis.set_ylim(0, 14)
        axis.grid(True)

    def add_equivalence_marker(self, axis, key_points):
        
        """
        Adds the equivalence point marker to the graph
        """

        equivalence_volume = key_points["equivalence_volume"]
        equivalence_ph = key_points["equivalence_ph"]

        axis.axvline(
            equivalence_volume,
            linestyle="--",
            label="Equivalence point"
        )

        axis.scatter(
            equivalence_volume,
            equivalence_ph
        )

        axis.annotate(
            f"Equivalence\n{equivalence_volume:.2f} cm³",
            xy=(equivalence_volume, equivalence_ph),
            xytext=(equivalence_volume, equivalence_ph + 1),
            arrowprops={"arrowstyle": "->"},
            fontsize=8
        )

    def add_half_equivalence_marker(self, axis, key_points):
        
        """
        Adds the half-equivalence point marker for weak acid titrations
        """

        if key_points["half_equivalence_ph"] is None:
            return

        half_volume = key_points["half_equivalence_volume"]
        half_ph = key_points["half_equivalence_ph"]

        axis.axvline(
            half_volume,
            linestyle=":",
            label="Half-equivalence point"
        )

        axis.scatter(
            half_volume,
            half_ph
        )

        axis.annotate(
            f"Half-equivalence\n{half_volume:.2f} cm³",
            xy=(half_volume, half_ph),
            xytext=(half_volume, half_ph - 1),
            arrowprops={"arrowstyle": "->"},
            fontsize=8
        )

    def add_selected_point_marker(self, axis, selected_point):
        
        """
        Adds the user's selected volume marker to the graph
        """

        selected_volume = selected_point["volume"]
        selected_ph = selected_point["ph"]

        axis.scatter(
            selected_volume,
            selected_ph,
            marker="x",
            s=70,
            label="Selected volume"
        )

        axis.annotate(
            f"Selected\npH {selected_ph:.2f}",
            xy=(selected_volume, selected_ph),
            xytext=(selected_volume, selected_ph + 0.8),
            arrowprops={"arrowstyle": "->"},
            fontsize=8
        )

    def create_single_curve_figure(self, curve_data, key_points, selected_point, data):
        
        """
        Creates one titration curve figure for the GUI
        """

        figure, axis = self.create_base_figure()

        axis.plot(
            curve_data["volumes"],
            curve_data["ph_values"],
            label="Titration curve"
        )

        self.add_equivalence_marker(axis, key_points)
        self.add_half_equivalence_marker(axis, key_points)
        self.add_selected_point_marker(axis, selected_point)

        self.setup_axis(
            axis,
            data["titration_type"]
        )

        axis.legend(
            loc="best",
            fontsize=8
        )

        figure.tight_layout()

        return figure

    def save_figure(self, figure, filename):
        
        """
        Saves the titration graph as an image file
        """

        figure.savefig(
            filename,
            dpi=200,
            bbox_inches="tight"
        )

    def export_curve_data(self, filename, curve_data):
        
        """
        Exports the calculated curve data to a CSV file
        """

        volumes = curve_data["volumes"]
        ph_values = curve_data["ph_values"]
        regions = curve_data["regions"]

        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Volume added / cm3",
                "pH",
                "Region"
            ])

            for volume, ph, region in zip(volumes, ph_values, regions):
                writer.writerow([
                    round(volume, 4),
                    round(ph, 4),
                    region
                ])
