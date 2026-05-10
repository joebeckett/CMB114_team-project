"""
validation_caner.py
Author: Caner

This file checks the values entered into the Tkinter application before they
are passed into Joe's calculation code.

The previous terminal version used simple validation helper functions, so this
version keeps that same style while changing the input names to match the GUI.
"""

TITRATION_TYPES = [
    "Strong acid vs strong base",
    "Weak acid vs strong base"
]

MIN_CONCENTRATION = 0.000001
MAX_CONCENTRATION = 10.0

MIN_VOLUME = 0.0
MAX_VOLUME = 10000.0

MIN_GRAPH_POINTS = 20
MAX_GRAPH_POINTS = 1000

MIN_PKA = -5.0
MAX_PKA = 20.0


def validate_titration_type(titration_type):
    """
    Checks that the selected titration type is valid.
    """

    if titration_type not in TITRATION_TYPES:
        raise ValueError("Please choose a valid titration type.")


def validate_positive_number(value, field_name):
    """
    Checks that a number is greater than zero.
    """

    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")


def validate_range(value, field_name, minimum, maximum):
    """
    Checks that a number is within a sensible range.
    """

    if value < minimum or value > maximum:
        raise ValueError(
            f"{field_name} must be between {minimum} and {maximum}."
        )


def convert_to_float(value, field_name):
    """
    Converts a text input into a float.
    """

    if value.strip() == "":
        raise ValueError(f"{field_name} is missing.")

    try:
        return float(value)

    except ValueError:
        raise ValueError(f"{field_name} must be a number.")


def convert_to_int(value, field_name):
    """
    Converts a text input into an integer.
    """

    if value.strip() == "":
        raise ValueError(f"{field_name} is missing.")

    try:
        number = float(value)

    except ValueError:
        raise ValueError(f"{field_name} must be a whole number.")

    if not number.is_integer():
        raise ValueError(f"{field_name} must be a whole number.")

    return int(number)


def validate_concentration(value, field_name):
    """
    Validates concentration values.
    """

    validate_positive_number(value, field_name)

    validate_range(
        value,
        field_name,
        MIN_CONCENTRATION,
        MAX_CONCENTRATION
    )


def validate_volume(value, field_name):
    """
    Validates volume values.
    """

    validate_positive_number(value, field_name)

    validate_range(
        value,
        field_name,
        0.000001,
        MAX_VOLUME
    )


def validate_selected_volume(value, max_volume):
    """
    Checks the selected base volume used for the single pH calculation.
    """

    validate_range(
        value,
        "Selected volume",
        MIN_VOLUME,
        max_volume
    )


def validate_graph_points(value):
    """
    Checks the number of graph points.
    """

    if value < MIN_GRAPH_POINTS or value > MAX_GRAPH_POINTS:
        raise ValueError(
            f"Graph points must be between {MIN_GRAPH_POINTS} and {MAX_GRAPH_POINTS}."
        )


def validate_pka(value, required):
    """
    Checks pKa for weak acid titrations.

    Strong acid titrations do not need pKa, so blank input is allowed.
    """

    if value.strip() == "":
        if required:
            raise ValueError("pKa is required for a weak acid titration.")
        return None

    pka = convert_to_float(value, "pKa")

    validate_range(
        pka,
        "pKa",
        MIN_PKA,
        MAX_PKA
    )

    return pka


def validate_filename(filename, extension):
    """
    Validates export filenames.
    """

    if filename.strip() == "":
        raise ValueError("Filename cannot be blank.")

    invalid_characters = ["<", ">", ":", '"', "|", "?", "*"]

    for character in invalid_characters:
        if character in filename:
            raise ValueError(f"Filename cannot contain {character}.")

    if not filename.endswith(extension):
        filename = filename + extension

    return filename


def validate_inputs(raw_inputs):
    """
    Main validation function used by gui_caner.py.

    It takes raw text from the GUI and returns a clean dictionary containing
    float and integer values.
    """

    titration_type = raw_inputs["titration_type"]
    validate_titration_type(titration_type)

    acid_concentration = convert_to_float(
        raw_inputs["acid_concentration"],
        "Acid concentration"
    )

    acid_volume = convert_to_float(
        raw_inputs["acid_volume"],
        "Acid volume"
    )

    base_concentration = convert_to_float(
        raw_inputs["base_concentration"],
        "Base concentration"
    )

    max_base_volume = convert_to_float(
        raw_inputs["max_base_volume"],
        "Maximum base volume"
    )

    selected_volume = convert_to_float(
        raw_inputs["selected_volume"],
        "Selected volume"
    )

    graph_points = convert_to_int(
        raw_inputs["graph_points"],
        "Graph points"
    )

    validate_concentration(
        acid_concentration,
        "Acid concentration"
    )

    validate_volume(
        acid_volume,
        "Acid volume"
    )

    validate_concentration(
        base_concentration,
        "Base concentration"
    )

    validate_volume(
        max_base_volume,
        "Maximum base volume"
    )

    validate_selected_volume(
        selected_volume,
        max_base_volume
    )

    validate_graph_points(graph_points)

    is_weak_acid = titration_type == "Weak acid vs strong base"

    pka = validate_pka(
        raw_inputs["pka"],
        required=is_weak_acid
    )

    if not is_weak_acid:
        pka = None

    clean_data = {
        "titration_type": titration_type,
        "acid_concentration": acid_concentration,
        "acid_volume": acid_volume,
        "base_concentration": base_concentration,
        "max_base_volume": max_base_volume,
        "selected_volume": selected_volume,
        "graph_points": graph_points,
        "pka": pka
    }

    return clean_data


def get_strong_acid_example():
    """
    Returns example values for a strong acid titration.
    """

    return {
        "titration_type": "Strong acid vs strong base",
        "acid_concentration": "0.1",
        "acid_volume": "25",
        "base_concentration": "0.1",
        "max_base_volume": "50",
        "selected_volume": "25",
        "graph_points": "200",
        "pka": ""
    }


def get_weak_acid_example():
    """
    Returns example values for a weak acid titration.
    """

    return {
        "titration_type": "Weak acid vs strong base",
        "acid_concentration": "0.1",
        "acid_volume": "25",
        "base_concentration": "0.1",
        "max_base_volume": "50",
        "selected_volume": "12.5",
        "graph_points": "200",
        "pka": "4.76"
    }


def get_blank_inputs():
    """
    Returns blank values for clearing the GUI form.
    """

    return {
        "titration_type": "Strong acid vs strong base",
        "acid_concentration": "",
        "acid_volume": "",
        "base_concentration": "",
        "max_base_volume": "",
        "selected_volume": "",
        "graph_points": "",
        "pka": ""
    }