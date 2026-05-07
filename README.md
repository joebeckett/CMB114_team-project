# CMB114 Team Project
Template for a simple team project

The code is divided between folders `student1` and `student2`.

You can run the code by calling
~~~~
./driver.py
~~~~


# 1. Reaction Kinetics Simulator

## Project summary

This project is a Python-based reaction kinetics simulator.

It allows the user to model simple chemical reactions and visualise how reactant concentration changes over time.

## Chemistry included

The project includes:

- First-order reactions
- Second-order reactions
- Concentration-time graphs
- Rate-time graphs
- Half-life estimation
- Arrhenius equation calculations
- Effect of temperature on rate constant

## Programming features

The project uses:

- Classes
- Functions
- Multiple Python files
- Import statements
- Error handling
- CSV export
- Graph plotting using matplotlib

## File structure

- `main.py` - main menu and overall program control
- `reaction_caner.py` - Reaction class and Arrhenius calculations
- `simulator_caner.py` - simulation logic using Euler's method
- `input_helpers_joe.py` - user input functions
- `plotter_joe.py` - graph plotting
- `data_export_joe.py` - CSV export functions

## Work split

### Caner

Caner worked mainly on:

- Reaction class
- Rate equations
- Arrhenius equation
- Euler simulation
- Half-life calculation
- Simulation summary

Files:

- `reaction_caner.py`
- `simulator_caner.py`

### Joe

Joe worked mainly on:

- User input
- Main menu
- Graphs
- CSV export
- Comparison tools

Files:

- `input_helpers_joe.py`
- `plotter_joe.py`
- `data_export_joe.py`
- `main_joe.py`
