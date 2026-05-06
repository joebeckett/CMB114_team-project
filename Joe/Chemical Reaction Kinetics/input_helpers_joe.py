"""
input_helpers_joe.py
Author: Joe

This file contains helper functions for getting user input.
"""


def get_float_input(message):
    while True:
        try:
            value = float(input(message))
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_positive_float_input(message):
    while True:
        value = get_float_input(message)

        if value > 0:
            return value

        print("Value must be greater than zero.")


def get_int_input(message):
    while True:
        try:
            value = int(input(message))
            return value
        except ValueError:
            print("Please enter a whole number.")


def get_menu_choice(message, allowed_choices):
    while True:
        choice = get_int_input(message)

        if choice in allowed_choices:
            return choice

        print("Invalid choice. Please try again.")


def ask_yes_no(message):
    while True:
        answer = input(message).lower().strip()

        if answer in ["y", "yes"]:
            return True

        if answer in ["n", "no"]:
            return False

        print("Please enter y or n.")
