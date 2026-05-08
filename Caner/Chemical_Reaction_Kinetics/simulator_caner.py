"""
simulator_caner.py
Author: Caner

This file contains the Simulator class.
It uses Euler's method to simulate how concentration changes over time.

Euler method idea:
new concentration = old concentration + change

For a reactant being used up:
change = -rate * time step
"""


class Simulator:
    def __init__(self, reaction, total_time, time_step):
        self.reaction = reaction
        self.total_time = total_time
        self.time_step = time_step

        self.check_values()

    def check_values(self):
        """
        Checks that the time values make sense.
        """

        if self.total_time <= 0:
            raise ValueError("Total time must be greater than zero.")

        if self.time_step <= 0:
            raise ValueError("Time step must be greater than zero.")

        if self.time_step > self.total_time:
            raise ValueError("Time step cannot be larger than total time.")

    def run_simulation(self):
        """
        Runs the simulation using Euler's method.

        Returns three lists:
        - times
        - concentrations
        - rates
        """

        times = []
        concentrations = []
        rates = []

        current_time = 0
        current_concentration = self.reaction.initial_concentration

        while current_time <= self.total_time:
            rate = self.reaction.get_rate(current_concentration)

            times.append(current_time)
            concentrations.append(current_concentration)
            rates.append(rate)

            change = -rate * self.time_step
            current_concentration = current_concentration + change

            # Concentration should not become negative in a real reaction.
            if current_concentration < 0:
                current_concentration = 0

            current_time = current_time + self.time_step

        return times, concentrations, rates

    def estimate_half_life(self, times, concentrations):
        """
        Estimates the half-life from the simulation data.

        Half-life is the time taken for concentration to fall to half
        of the starting concentration.
        """

        half_concentration = self.reaction.initial_concentration / 2

        for i in range(len(concentrations)):
            if concentrations[i] <= half_concentration:
                return times[i]

        return None

    def calculate_percentage_reacted(self, final_concentration):
        """
        Calculates what percentage of reactant has been used up.
        """

        starting_concentration = self.reaction.initial_concentration
        amount_reacted = starting_concentration - final_concentration

        percentage_reacted = (amount_reacted / starting_concentration) * 100

        return percentage_reacted

    def calculate_average_rate(self, concentrations):
        """
        Calculates the average rate over the whole simulation.
        """

        starting_concentration = concentrations[0]
        final_concentration = concentrations[-1]

        change_in_concentration = starting_concentration - final_concentration

        average_rate = change_in_concentration / self.total_time

        return average_rate

    def find_time_for_percentage_reacted(self, times, concentrations, target_percentage):
        """
        Finds the time when a certain percentage of reactant has reacted.

        Example:
        target_percentage = 90 means we are finding when 90% has reacted.
        """

        if target_percentage <= 0 or target_percentage >= 100:
            raise ValueError("Target percentage must be between 0 and 100.")

        starting_concentration = self.reaction.initial_concentration
        target_concentration = starting_concentration * (1 - target_percentage / 100)

        for i in range(len(concentrations)):
            if concentrations[i] <= target_concentration:
                return times[i]

        return None

    def get_summary(self, times, concentrations, rates):
        """
        Creates a dictionary of useful values from the simulation.
        """

        final_concentration = concentrations[-1]
        final_rate = rates[-1]

        simulated_half_life = self.estimate_half_life(times, concentrations)
        theoretical_half_life = self.reaction.get_theoretical_half_life()

        percentage_reacted = self.calculate_percentage_reacted(final_concentration)
        average_rate = self.calculate_average_rate(concentrations)

        time_for_90_percent = self.find_time_for_percentage_reacted(
            times,
            concentrations,
            90
        )

        summary = {
            "final_concentration": final_concentration,
            "final_rate": final_rate,
            "simulated_half_life": simulated_half_life,
            "theoretical_half_life": theoretical_half_life,
            "percentage_reacted": percentage_reacted,
            "average_rate": average_rate,
            "time_for_90_percent": time_for_90_percent
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