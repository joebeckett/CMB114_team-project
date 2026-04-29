"""
Author: Caner

This file contains the Reaction class and chemistry calculations.
"""

import math


class Reaction:
    def _init_(self, name, order, rate_constant, initiral_concentration):
        self.name = name
        self.order = order
        self.rate_constant = rate_constant
        self.initial_concentration = initiral_concentration
        
        self.check_values()
    
    def check_values(self):
        if self.name == "":
            print("Reaction name cannot be empty.")

        if self.order not in [1, 2]:
            print("Only first-order and second-order reactions are supported.")

        if self.rate_constant <= 0:
            print("Rate constant must be greater than zero.")

        if self.initial_concentration <= 0:
            print("Initial concentration must be greater than zero.")


    def get_rate(self, concentration):
        """
        Calculates the reaction rate.

        First order: rate = k[A]
        Second order: rate = k[A]^2
        """

        if concentration < 0:
            concentration = 0

        if self.order == 1:
            return self.rate_constant * concentration

        if self.order == 2:
            return self.rate_constant * concentration ** 2

    def get_rate_equation(self):
        if self.order == 1:
            return "rate = k[A]"

        return "rate = k[A]^2"

    def get_units_for_k(self):
        if self.order == 1:
            return "s^-1"

        return "dm^3 mol^-1 s^-1"
    

    def get_theoretical_half_life(self):
        """
        Calculates theoretical half-life.

        First order: t1/2 = ln(2) / k
        Second order: t1/2 = 1 / k[A]0
        """

        if self.order == 1:
            return math.log(2) / self.rate_constant

        return 1 / (self.rate_constant * self.initial_concentration)

    def get_description(self):
        return (
            f"Reaction name: {self.name}\n"
            f"Reaction order: {self.order}\n"
            f"Rate equation: {self.get_rate_equation()}\n"
            f"Rate constant: {self.rate_constant} {self.get_units_for_k()}\n"
            f"Initial concentration: {self.initial_concentration} mol dm^-3"
        )

def calculate_arrhenius_rate_constant(activation_energy, temperature, pre_exponential_factor):
    """
    Calculates k using the Arrhenius equation:

    k = A * e^(-Ea / RT)
    """

    gas_constant = 8.314

    if activation_energy <= 0:
        raise ValueError("Activation energy must be greater than zero.")

    if temperature <= 0:
        raise ValueError("Temperature must be above 0 K.")

    if pre_exponential_factor <= 0:
        raise ValueError("Pre-exponential factor must be greater than zero.")

    return pre_exponential_factor * math.exp(
        -activation_energy / (gas_constant * temperature)
    )


def compare_arrhenius_temperatures(activation_energy, pre_exponential_factor, temperatures):
    """
    Calculates k values for several temperatures.
    This helps show how temperature changes reaction rate.
    """

    results = []

    for temperature in temperatures:
        k = calculate_arrhenius_rate_constant(
            activation_energy,
            temperature,
            pre_exponential_factor
        )

        results.append({
            "temperature": temperature,
            "rate_constant": k
        })

    return results

def explain_reaction_order(order):
    if order == 1:
        return (
            "A first-order reaction has a rate directly proportional to the "
            "concentration of one reactant."
        )

    if order == 2:
        return (
            "A second-order reaction has a rate proportional to the square "
            "of the concentration, or to two reacting species."
        )

    return "This order is not supported by the current program."