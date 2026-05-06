"""
main.py
Authors: Caner and Joe
"""

from reaction_caner import (
    Reaction,
    calculate_arrhenius_rate_constant,
    compare_arrhenius_temperatures,
    explain_reaction_order
)

from simulator_caner import Simulator
from plotter_joe import Plotter

from input_helpers_joe import (
    get_positive_float_input,
    get_menu_choice,
    ask_yes_no
)

from data_export_joe import (
    export_simulation_to_csv,
    export_summary_to_csv,
    export_arrhenius_to_csv
)


def create_reaction_from_user():
    print("\nCreate a reaction")
    print("-----------------")

    name = input("Enter a name for the reaction: ").strip()

    print("\nChoose reaction order:")
    print("1 - First order")
    print("2 - Second order")

    order = get_menu_choice("Enter choice: ", [1, 2])

    print("\nChoose how to enter the rate constant:")
    print("1 - Enter rate constant directly")
    print("2 - Calculate rate constant using Arrhenius equation")

    k_choice = get_menu_choice("Enter choice: ", [1, 2])

    if k_choice == 1:
        rate_constant = get_positive_float_input("Enter rate constant k: ")

    else:
        activation_energy = get_positive_float_input(
            "Enter activation energy Ea in J mol^-1: "
        )

        temperature = get_positive_float_input(
            "Enter temperature in K: "
        )

        pre_exponential_factor = get_positive_float_input(
            "Enter pre-exponential factor A: "
        )

        rate_constant = calculate_arrhenius_rate_constant(
            activation_energy,
            temperature,
            pre_exponential_factor
        )

        print(f"Calculated k = {rate_constant:.5g}")

    initial_concentration = get_positive_float_input(
        "Enter initial concentration in mol dm^-3: "
    )

    return Reaction(
        name,
        order,
        rate_constant,
        initial_concentration
    )


def create_simulator_from_user(reaction):
    print("\nSimulation settings")
    print("-------------------")

    total_time = get_positive_float_input(
        "Enter total simulation time in seconds: "
    )

    time_step = get_positive_float_input(
        "Enter time step in seconds: "
    )

    return Simulator(reaction, total_time, time_step)


def print_simulation_summary(reaction, summary):
    print("\nSimulation summary")
    print("------------------")
    print(reaction.get_description())

    print(f"\nFinal concentration: {summary['final_concentration']:.5f} mol dm^-3")
    print(f"Final rate: {summary['final_rate']:.5f}")

    if summary["simulated_half_life"] is None:
        print("Simulated half-life: not reached")
    else:
        print(f"Simulated half-life: {summary['simulated_half_life']:.2f} s")

    print(f"Theoretical half-life: {summary['theoretical_half_life']:.2f} s")
    print(f"Percentage reacted: {summary['percentage_reacted']:.2f}%")
    print(f"Average rate: {summary['average_rate']:.5f}")

    if summary["time_for_90_percent"] is None:
        print("Time for 90% reacted: not reached")
    else:
        print(f"Time for 90% reacted: {summary['time_for_90_percent']:.2f} s")

    print(f"Maximum Euler percentage error: {summary['maximum_error']:.3f}%")


def run_single_reaction():
    try:
        reaction = create_reaction_from_user()
        simulator = create_simulator_from_user(reaction)

        (
            times,
            concentrations,
            rates,
            exact_concentrations,
            percentage_errors
        ) = simulator.run_simulation()

        summary = simulator.get_summary(
            times,
            concentrations,
            rates,
            percentage_errors
        )

        print_simulation_summary(reaction, summary)

        show_table = ask_yes_no("\nShow data table? (y/n): ")

        if show_table:
            simulator.print_table(
                times,
                concentrations,
                rates,
                exact_concentrations,
                percentage_errors
            )

        plotter = Plotter()

        if ask_yes_no("\nShow concentration-time graph? (y/n): "):
            plotter.plot_concentration_time(
                times,
                concentrations,
                reaction.name
            )

        if ask_yes_no("Show rate-time graph? (y/n): "):
            plotter.plot_rate_time(
                times,
                rates,
                reaction.name
            )

        if ask_yes_no("Show simulated vs exact graph? (y/n): "):
            plotter.plot_simulated_vs_exact(
                times,
                concentrations,
                exact_concentrations,
                reaction.name
            )

        if ask_yes_no("Show Euler error graph? (y/n): "):
            plotter.plot_error_time(
                times,
                percentage_errors,
                reaction.name
            )

        if ask_yes_no("\nSave full simulation data to CSV? (y/n): "):
            filename = input("Enter filename: ")

            export_simulation_to_csv(
                filename,
                times,
                concentrations,
                rates,
                exact_concentrations,
                percentage_errors
            )

        if ask_yes_no("Save summary to CSV? (y/n): "):
            filename = input("Enter filename: ")

            export_summary_to_csv(
                filename,
                reaction,
                summary
            )

    except ValueError as error:
        print(f"Error: {error}")


def compare_two_reactions():
    results = []

    try:
        for number in range(1, 3):
            print(f"\nReaction {number}")
            print("----------")

            reaction = create_reaction_from_user()
            simulator = create_simulator_from_user(reaction)

            (
                times,
                concentrations,
                rates,
                exact_concentrations,
                percentage_errors
            ) = simulator.run_simulation()

            summary = simulator.get_summary(
                times,
                concentrations,
                rates,
                percentage_errors
            )

            print_simulation_summary(reaction, summary)

            results.append({
                "name": reaction.name,
                "times": times,
                "concentrations": concentrations
            })

        plotter = Plotter()
        plotter.plot_comparison(results)

    except ValueError as error:
        print(f"Error: {error}")


def arrhenius_temperature_tool():
    try:
        print("\nArrhenius temperature comparison")
        print("--------------------------------")

        activation_energy = get_positive_float_input(
            "Enter activation energy Ea in J mol^-1: "
        )

        pre_exponential_factor = get_positive_float_input(
            "Enter pre-exponential factor A: "
        )

        number_of_temperatures = get_menu_choice(
            "How many temperatures do you want to compare? Choose 2, 3, 4, or 5: ",
            [2, 3, 4, 5]
        )

        temperatures = []

        for i in range(number_of_temperatures):
            temperature = get_positive_float_input(
                f"Enter temperature {i + 1} in K: "
            )

            temperatures.append(temperature)

        results = compare_arrhenius_temperatures(
            activation_energy,
            pre_exponential_factor,
            temperatures
        )

        print("\nTemperature / K    Rate constant k")
        print("----------------------------------")

        for result in results:
            print(
                f"{result['temperature']:12.2f}    "
                f"{result['rate_constant']:.5g}"
            )

        plotter = Plotter()

        if ask_yes_no("\nShow temperature graph? (y/n): "):
            plotter.plot_arrhenius_temperature_graph(results)

        if ask_yes_no("Save Arrhenius data to CSV? (y/n): "):
            filename = input("Enter filename: ")
            export_arrhenius_to_csv(filename, results)

    except ValueError as error:
        print(f"Error: {error}")


def about_project():
    print("\nAbout this project")
    print("------------------")
    print("This program simulates simple chemical reaction kinetics.")
    print("It supports first-order and second-order reactions.")
    print("The program uses Euler's method to estimate concentration over time.")
    print("The program also compares Euler results with exact integrated equations.")
    print("It includes the Arrhenius equation to show temperature effects.")
    print()
    print("First-order explanation:")
    print(explain_reaction_order(1))
    print()
    print("Second-order explanation:")
    print(explain_reaction_order(2))


def main_menu():
    while True:
        print("\nReaction Kinetics Simulator")
        print("---------------------------")
        print("1 - Run one reaction simulation")
        print("2 - Compare two reactions")
        print("3 - Arrhenius temperature comparison")
        print("4 - About this project")
        print("5 - Exit")

        choice = get_menu_choice("Enter choice: ", [1, 2, 3, 4, 5])

        if choice == 1:
            run_single_reaction()

        elif choice == 2:
            compare_two_reactions()

        elif choice == 3:
            arrhenius_temperature_tool()

        elif choice == 4:
            about_project()

        elif choice == 5:
            print("Goodbye.")
            break


if __name__ == "__main__":
    main_menu()
