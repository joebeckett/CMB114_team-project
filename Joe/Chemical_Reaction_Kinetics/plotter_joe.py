"""
plotter_joe.py
Author: Joe
"""

import matplotlib.pyplot as plt


class Plotter:
    def plot_concentration_time(self, times, concentrations, reaction_name):
        plt.figure()
        plt.plot(times, concentrations, marker="o", markersize=3)
        plt.xlabel("Time / s")
        plt.ylabel("Concentration / mol dm$^{-3}$")
        plt.title(f"Concentration-Time Graph: {reaction_name}")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_rate_time(self, times, rates, reaction_name):
        plt.figure()
        plt.plot(times, rates, marker="o", markersize=3)
        plt.xlabel("Time / s")
        plt.ylabel("Rate / mol dm$^{-3}$ s$^{-1}$")
        plt.title(f"Rate-Time Graph: {reaction_name}")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_simulated_vs_exact(self, times, concentrations, exact_concentrations, reaction_name):
        plt.figure()

        plt.plot(
            times,
            concentrations,
            marker="o",
            markersize=3,
            label="Euler simulation"
        )

        plt.plot(
            times,
            exact_concentrations,
            linestyle="--",
            label="Exact integrated equation"
        )

        plt.xlabel("Time / s")
        plt.ylabel("Concentration / mol dm$^{-3}$")
        plt.title(f"Simulated vs Exact Concentration: {reaction_name}")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_error_time(self, times, percentage_errors, reaction_name):
        plt.figure()
        plt.plot(times, percentage_errors, marker="o", markersize=3)
        plt.xlabel("Time / s")
        plt.ylabel("Percentage error / %")
        plt.title(f"Euler Method Error Over Time: {reaction_name}")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

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
