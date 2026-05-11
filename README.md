# CMB114 Team Project

The code is divided between folders `Caner` and `Joe`.

You can run the code by calling
~~~~
- `python -m Joe.Chemical_Reaction_Kinetics.main_joe`
- `python -m Caner.Titration_Simulator.main_caner`
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

- `main_joe.py` - main menu and overall program control
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
- some of `main_joe.py`

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


## How to Run

Type into the terminal: 
- `python -m Joe.Chemical_Reaction_Kinetics.main_joe`


# 2. Acid-Base Titration Simulator

## Project summary

This project is a Python-based acid-base titration simulator.

It allows the user to enter titration values, calculate pH changes, and visualise titration curves using a Tkinter application.

The program supports strong acid vs strong base titrations and weak acid vs strong base titrations.

## Chemistry included

The project includes:

- Strong acid vs strong base titrations
- Weak acid vs strong base titrations
- pH calculations before equivalence
- pH calculations at equivalence
- pH calculations after equivalence
- Buffer region for weak acid titrations
- Half-equivalence point
- Equivalence point volume
- Initial pH calculation
- pH at a selected volume
- Simple ionic reaction equations

## Programming features

The project uses:

- Tkinter GUI
- Functions
- Classes
- Multiple Python files
- Import statements
- Error handling
- Input validation
- CSV export
- Graph export
- Graph plotting using matplotlib
- Matplotlib graphs embedded in Tkinter

## File structure

- `main_caner.py` - starts the Tkinter application and opens the main window
- `validation_caner.py` - validates user inputs from the GUI
- `gui_caner.py` - creates the Tkinter interface and connects buttons to calculations
- `reaction_joe.py` - chemistry helper functions and reaction information
- `calculations_joe.py` - pH calculations and titration curve generation
- `plotting_joe.py` - graph plotting, graph export, and CSV export
- `requirements.txt` - required Python libraries

## Work split

### Caner

Caner worked mainly on:

- Main application start-up
- Tkinter GUI layout
- Input fields
- Buttons
- Displaying calculated values
- Input validation
- Error messages
- Loading example values
- Calling Joe’s calculation and plotting functions

### Files:

- `main_caner.py`
- `validation_caner.py`
- `gui_caner.py`

### Joe

Joe worked mainly on:

- Chemistry helper functions
- Mole calculations
- Volume conversions
- Strong acid vs strong base pH calculations
- Weak acid vs strong base pH calculations
- Equivalence point calculations
- Half-equivalence point calculations
- Titration curve data generation
- Matplotlib plotting
- CSV export
- Graph export

### Files:

- `reaction_joe.py`
- `calculations_joe.py`
- `plotting_joe.py`

## How to Run

Type into the terminal 
- `python -m Caner.Titration_Simulator.main_caner`
