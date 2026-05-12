"""
reaction_caner.py
Author: Caner

This file contains the Reaction class.
It stores the basic information for a chemical reaction and calculates
the rate of change in concentration.

For this project we are modelling simple reactions:
- Zero order:      rate = k
- First order:     rate = k[A]
- Second order:    rate = k[A]^2

The simulator uses this class to work out how concentration changes over time.
"""

import math


class Reaction:
    def __init__(self, reaction_name, order, rate_constant, initial_concentration):

        self.reaction_name = reaction_name
        self.order = order
        self.rate_constant = rate_constant
        self.initial_concentration = initial_concentration

        self.check_values()

    def check_values(self):
        """
        Checks that the user has entered sensible values.
        This helps stop the program crashing later.
        """

        if self.reaction_name == "":
            raise ValueError("Reaction name cannot be empty.")
        
        if self.order not in [0, 1, 2]:
            raise ValueError("Reaction order must be 0, 1, or 2.")

        if self.rate_constant <= 0:
            raise ValueError("Rate constant must be greater than zero.")

        if self.initial_concentration <= 0:
            raise ValueError("Initial concentration must be greater than zero.")

    def get_rate(self, concentration):
        """
        Calculates the rate of reaction at a given concentration.

        Zero order: rate = k
        First order: rate = k[A]
        Second order: rate = k[A]^2

        """

        if concentration < 0:
            concentration = 0

        if self.order == 0:
            return self.rate_constant

        elif self.order == 1:
            return self.rate_constant * concentration

        elif self.order == 2:
            return self.rate_constant * concentration ** 2

    def get_rate_equation(self):
        """
        Returns the rate equation as text.
        This is useful for printing and saving summaries.
        """

        if self.order == 0:
            return "rate = k"

        elif self.order == 1:
            return "rate = k[A]"

        else:
            return "rate = k[A]^2"

    def get_exact_concentration(self, time):
        """
        Returns the exact concentration at a given time based on reaction order.

        This is used for comparison with the Euler simulation output.
        """

        if time < 0:
            raise ValueError("Time cannot be negative.")

        if self.order == 0:
            exact = self.initial_concentration - self.rate_constant * time
            return max(exact, 0)

        elif self.order == 1:
            return self.initial_concentration * math.exp(-self.rate_constant * time)

        else:
            denominator = 1 + self.rate_constant * self.initial_concentration * time
            if denominator == 0:
                return 0
            return self.initial_concentration / denominator

    def get_units_for_k(self):
        """
        Returns suitable units for the rate constant.
        """

        if self.order == 0:
            return "mol dm^-3 s^-1"

        elif self.order == 1:
            return "s^-1"

        else:
            return "dm^3 mol^-1 s^-1"

    def get_theoretical_half_life(self):
        """
        Calculates the theoretical half-life.

        Zero order:  t1/2 = [A]0 / 2k
        First order: t1/2 = ln(2) / k
        Second order: t1/2 = 1 / k[A]0
        """

        if self.order == 0:
            return self.initial_concentration / (2 * self.rate_constant)

        elif self.order == 1:
            return math.log(2) / self.rate_constant

        else:
            return 1 / (self.rate_constant * self.initial_concentration)

    def get_description(self):
        """
        Returns a short description of the reaction.
        This is useful for printing results to the user.
        """

        if self.order == 0:
            order_text = "zero order"
        elif self.order == 1:
            order_text = "first order"
        else:
            order_text = "second order"

        return (
            f"{self.reaction_name}: {order_text} reaction\n"
            f"Rate equation: {self.get_rate_equation()}\n"
            f"k = {self.rate_constant} {self.get_units_for_k()}\n"
            f"Initial concentration = {self.initial_concentration} mol dm^-3"
        )


def calculate_arrhenius_rate_constant(activation_energy, temperature, pre_exponential_factor):
    """
    Calculates rate constant using the Arrhenius equation:

    k = A * exp(-Ea / RT)

    activation_energy should be in J mol^-1
    temperature should be in K
    pre_exponential_factor is A
    """

    gas_constant = 8.314  # J mol^-1 K^-1

    if activation_energy <= 0:
        raise ValueError("Activation energy must be greater than zero.")

    if temperature <= 0:
        raise ValueError("Temperature must be greater than zero Kelvin.")

    if pre_exponential_factor <= 0:
        raise ValueError("Pre-exponential factor must be greater than zero.")

    k = pre_exponential_factor * math.exp(-activation_energy / (gas_constant * temperature))

    return k