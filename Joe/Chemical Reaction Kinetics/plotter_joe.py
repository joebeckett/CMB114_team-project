 """
plotter_joe.py
Author: Joe

This file contains the Plotter class.
It handles all graphs for the project.
"""

import matplotlib.pyplot as plt


class Plotter:
    # Plot concentration changes over time
    def plot_concentration_time(self, times, concentrations, reaction_name):
        plt.figure()
        plt.plot(times, concentrations, marker="o", markersize=3)
        plt.xlabel("Time / s")
        plt.ylabel("Concentration / mol dm$^{-3}$")
        plt.title(f"Concentration-Time Graph: {reaction_name}")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # Plot reaction rate changes over time
    def plot_rate_time(self, times, rates, reaction_name):
        plt.figure()
        plt.plot(times, rates, marker="o", markersize=3)
        plt.xlabel("Time / s")
        plt.ylabel("Rate / mol dm$^{-3}$ s$^{-1}$")
        plt.title(f"Rate-Time Graph: {reaction_name}")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # Plot several reaction simulations on one graph
    def plot_comparison(self, results):
        plt.figure()

        for result in results:
            plt.plot(
                result["times"],
                result["concentrations"],
                marker="o",
                markersize=3,
                label=result["name"]
            )

        plt.xlabel("Time / s")
        plt.ylabel("Concentration / mol dm$^{-3}$")
        plt.title("Comparison of Reaction Simulations")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    # Plot how temperature affects the rate constant
    def plot_arrhenius_temperature_graph(self, arrhenius_results):
        temperatures = []
        rate_constants = []

        for result in arrhenius_results:
            temperatures.append(result["temperature"])
            rate_constants.append(result["rate_constant"])

        plt.figure()
        plt.plot(temperatures, rate_constants, marker="o")
        plt.xlabel("Temperature / K")
        plt.ylabel("Rate constant k")
        plt.title("Effect of Temperature on Rate Constant")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
