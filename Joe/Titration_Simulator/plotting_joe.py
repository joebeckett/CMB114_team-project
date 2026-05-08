"""
plotting_joe.py
Author: Joe

This file handles matplotlib graphs and CSV export.
"""

import csv
import matplotlib.pyplot as plt


class Plotter:
    """
    Plotter class for titration curves.
    """

    def setup_graph(self, title):
        """
        Adds labels, title, grid and pH limits.
        """

        plt.title(title)
        plt.xlabel("Volume of base added / cm3")
        plt.ylabel("pH")
        plt.ylim(0, 14)
        plt.grid(True)

    def add_key_markers(self, key_points):
        """
        Adds equivalence and half-equivalence markers.
        """

        plt.axvline(
            key_points["equivalence_volume"],
            linestyle="--",
            label="Equivalence point"
        )

        plt.scatter(
            key_points["equivalence_volume"],
            key_points["equivalence_ph"]
        )

        if key_points["half_equivalence_ph"] is not None:
            plt.axvline(
                key_points["half_equivalence_volume"],
                linestyle=":",
                label="Half-equivalence point"
            )

            plt.scatter(
                key_points["half_equivalence_volume"],
                key_points["half_equivalence_ph"]
            )

    def plot_single_curve(self, curve_data, key_points, data):
        """
        Plots one titration curve.
        """

        volumes = curve_data["volumes"]
        ph_values = curve_data["ph_values"]

        plt.figure(figsize=(8, 5))
        plt.plot(
            volumes,
            ph_values,
            label="Titration curve"
        )

        self.add_key_markers(key_points)
        self.setup_graph(data["titration_type"])

        plt.legend()
        plt.show()

    def plot_comparison(self, comparison):
        """
        Plots two titration curves on the same axes.
        """

        first = comparison["first"]
        second = comparison["second"]

        plt.figure(figsize=(8, 5))

        plt.plot(
            first["curve_data"]["volumes"],
            first["curve_data"]["ph_values"],
            label="First titration"
        )

        plt.plot(
            second["curve_data"]["volumes"],
            second["curve_data"]["ph_values"],
            label="Second titration"
        )

        plt.axvline(
            first["key_points"]["equivalence_volume"],
            linestyle="--",
            label="First equivalence"
        )

        plt.axvline(
            second["key_points"]["equivalence_volume"],
            linestyle=":",
            label="Second equivalence"
        )

        self.setup_graph("Comparison of titration curves")

        plt.legend()
        plt.show()

    def save_single_graph(self, filename, curve_data, key_points, data):
        """
        Saves one titration graph as an image.
        """

        volumes = curve_data["volumes"]
        ph_values = curve_data["ph_values"]

        plt.figure(figsize=(8, 5))
        plt.plot(
            volumes,
            ph_values,
            label="Titration curve"
        )

        self.add_key_markers(key_points)
        self.setup_graph(data["titration_type"])

        plt.legend()
        plt.savefig(filename, dpi=200)
        plt.close()

    def export_curve_data(self, filename, curve_data):
        """
        Exports curve data to CSV.
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
