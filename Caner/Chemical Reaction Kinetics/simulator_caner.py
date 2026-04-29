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