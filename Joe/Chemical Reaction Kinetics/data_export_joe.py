"""
data_export_joe.py
Author: Joe
"""

import csv

def export_simulation_to_csv(filename, times, concentrations, rates, exact_concentrations, percentage_errors):
  
    """
    Export the full simulation data to a CSV file.
    The file includes time, simulated concentration, exact concentration,
    reaction rate, and percentage error at each time step.
    """

    if not filename.endswith(".csv"):
        filename = filename + ".csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Time / s",
            "Simulated concentration / mol dm^-3",
            "Exact concentration / mol dm^-3",
            "Rate / mol dm^-3 s^-1",
            "Percentage error / %"
        ])

        for i in range(len(times)):
            writer.writerow([
                times[i],
                concentrations[i],
                exact_concentrations[i],
                rates[i],
                percentage_errors[i]
            ])

    print(f"Simulation data saved as {filename}")


def export_summary_to_csv(filename, reaction, summary):
  
    """
    Export the main summary values for one reaction simulation.
    This includes the reaction details, final values, half-life results,
    percentage reacted, average rate, and maximum percentage error.
    """

    if not filename.endswith(".csv"):
        filename = filename + ".csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Reaction name", reaction.name])
        writer.writerow(["Reaction order", reaction.order])
        writer.writerow(["Rate equation", reaction.get_rate_equation()])
        writer.writerow(["Rate constant", reaction.rate_constant])
        writer.writerow(["Initial concentration", reaction.initial_concentration])
        writer.writerow([])

        writer.writerow(["Final concentration", summary["final_concentration"]])
        writer.writerow(["Final rate", summary["final_rate"]])
        writer.writerow(["Simulated half-life", summary["simulated_half_life"]])
        writer.writerow(["Theoretical half-life", summary["theoretical_half_life"]])
        writer.writerow(["Percentage reacted", summary["percentage_reacted"]])
        writer.writerow(["Average rate", summary["average_rate"]])
        writer.writerow(["Time for 90 percent reacted", summary["time_for_90_percent"]])
        writer.writerow(["Maximum percentage error", summary["maximum_error"]])

    print(f"Summary saved as {filename}")

def export_arrhenius_to_csv(filename, arrhenius_results):
  
    """
    Export Arrhenius temperature results to a CSV file.
    Each row contains a temperature and the corresponding rate constant.
    """

    if not filename.endswith(".csv"):
        filename = filename + ".csv"

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Temperature / K", "Rate constant k"])

        for result in arrhenius_results:
            writer.writerow([
                result["temperature"],
                result["rate_constant"]
            ])

    print(f"Arrhenius data saved as {filename}")
