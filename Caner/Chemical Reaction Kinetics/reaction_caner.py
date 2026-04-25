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