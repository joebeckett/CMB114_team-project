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
            raise ValueError("Reaction name cannot be empty.")

        if self.order not in [1, 2]:
            raise ValueError("Only first-order and second-order reactions are supported.")

        if self.rate_constant <= 0:
            raise ValueError("Rate constant must be greater than zero.")

        if self.initial_concentration <= 0:
            raise ValueError("Initial concentration must be greater than zero.")
