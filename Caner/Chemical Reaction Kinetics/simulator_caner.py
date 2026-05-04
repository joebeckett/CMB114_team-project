"""
simulator_caner.py
Author: Caner

This file contains the Simulator class.
It uses Euler's method to simulate concentration changes.
"""


class Simulator:
    def __init__(self, reaction, total_time, time_step):
        self.reaction = reaction
        self.total_time = total_time
        self.time_step = time_step

        self.check_values()

    def check_values(self):
        if self.total_time <= 0:
            raise ValueError("Total simulation time must be greater than zero.")

        if self.time_step <= 0:
            raise ValueError("Time step must be greater than zero.")

        if self.time_step > self.total_time:
            raise ValueError("Time step cannot be larger than total time.")

    def run_simulation(self):
        """
        Runs the reaction simulation.

        Euler method:
        new concentration = old concentration - rate * time step
        """

        times = []
        concentrations = []
        rates = []

        current_time = 0
        current_concentration = self.reaction.initial_concentration

        while current_time <= self.total_time:
            current_rate = self.reaction.get_rate(current_concentration)

            times.append(current_time)
            concentrations.append(current_concentration)
            rates.append(current_rate)

            change = current_rate * self.time_step
            current_concentration = current_concentration - change

            if current_concentration < 0:
                current_concentration = 0

            current_time = current_time + self.time_step

        return times, concentrations, rates

    def estimate_simulated_half_life(self, times, concentrations):
        starting_concentration = self.reaction.initial_concentration
        half_concentration = starting_concentration / 2

        for i in range(len(concentrations)):
            if concentrations[i] <= half_concentration:
                return times[i]

        return None

    def calculate_percentage_reacted(self, final_concentration):
        starting = self.reaction.initial_concentration

        amount_reacted = starting - final_concentration
        percentage = (amount_reacted / starting) * 100

        return percentage

    def get_summary(self, times, concentrations, rates):
        final_concentration = concentrations[-1]
        final_rate = rates[-1]

        simulated_half_life = self.estimate_simulated_half_life(
            times,
            concentrations
        )

        theoretical_half_life = self.reaction.get_theoretical_half_life()

        percentage_reacted = self.calculate_percentage_reacted(
            final_concentration
        )

        summary = {
            "final_concentration": final_concentration,
            "final_rate": final_rate,
            "simulated_half_life": simulated_half_life,
            "theoretical_half_life": theoretical_half_life,
            "percentage_reacted": percentage_reacted
        }

        return summary

    def print_table(self, times, concentrations, rates, max_rows=10):
        """
        Prints the first few rows of the simulation.
        """

        print("\nTime / s    Concentration / mol dm^-3    Rate")
        print("------------------------------------------------")

        rows_to_print = min(max_rows, len(times))

        for i in range(rows_to_print):
            print(
                f"{times[i]:8.2f}    "
                f"{concentrations[i]:12.5f}              "
                f"{rates[i]:12.5f}"
            )

        if len(times) > rows_to_print:
            print("... table shortened ...")