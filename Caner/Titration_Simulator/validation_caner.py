"""
validation_caner.py
Author: Caner

This file validates the values entered into the Tkinter application before
they are passed into Joe's calculation code.
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


def convert_to_float(value, field_name):
    if value.strip() == "":
        raise ValueError(f"{field_name} is missing.")

    try:
        return float(value)

    except ValueError:
        raise ValueError(f"{field_name} must be a number.")


def convert_to_int(value, field_name):
    if value.strip() == "":
        raise ValueError(f"{field_name} is missing.")

    try:
        number = float(value)

    except ValueError:
        raise ValueError(f"{field_name} must be a whole number.")

    if not number.is_integer():
        raise ValueError(f"{field_name} must be a whole number.")

    return int(number)


def check_range(value, field_name, minimum, maximum):
    if value < minimum or value > maximum:
        raise ValueError(
            f"{field_name} must be between {minimum} and {maximum}."
        )


def check_positive(value, field_name):
    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")


def check_concentration(value, field_name):
    check_positive(value, field_name)
    check_range(value, field_name, MIN_CONCENTRATION, MAX_CONCENTRATION)


def check_volume(value, field_name):
    check_positive(value, field_name)
    check_range(value, field_name, 0.000001, MAX_VOLUME)


def check_selected_volume(value, max_volume):
    check_range(value, "Selected volume", MIN_VOLUME, max_volume)


def check_graph_points(value):
    check_range(value, "Graph points", MIN_GRAPH_POINTS, MAX_GRAPH_POINTS)


def check_pka(value, required):
    if value.strip() == "":
        if required:
            raise ValueError("pKa is required for a weak acid titration.")
        return None

    pka = convert_to_float(value, "pKa")
    check_range(pka, "pKa", MIN_PKA, MAX_PKA)

    return pka


def get_filename_only(filename):
    filename = filename.replace("\\", "/")
    return filename.split("/")[-1]


def validate_filename(filename, extension):
    if filename.strip() == "":
        raise ValueError("Filename cannot be blank.")

    filename_only = get_filename_only(filename)
    invalid_characters = ["<", ">", ":", '"', "|", "?", "*"]

    for character in invalid_characters:
        if character in filename_only:
            raise ValueError(f"Filename cannot contain {character}.")

    if not filename.endswith(extension):
        filename += extension

    return filename


def validate_inputs(raw_inputs):
    titration_type = raw_inputs["titration_type"]

    if titration_type not in TITRATION_TYPES:
        raise ValueError("Please choose a valid titration type.")

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

    check_concentration(acid_concentration, "Acid concentration")
    check_volume(acid_volume, "Acid volume")
    check_concentration(base_concentration, "Base concentration")
    check_volume(max_base_volume, "Maximum base volume")
    check_selected_volume(selected_volume, max_base_volume)
    check_graph_points(graph_points)

    is_weak_acid = titration_type == "Weak acid vs strong base"
    pka = check_pka(raw_inputs["pka"], required=is_weak_acid)

    if not is_weak_acid:
        pka = None

    return {
        "titration_type": titration_type,
        "acid_concentration": acid_concentration,
        "acid_volume": acid_volume,
        "base_concentration": base_concentration,
        "max_base_volume": max_base_volume,
        "selected_volume": selected_volume,
        "graph_points": graph_points,
        "pka": pka
    }


def get_strong_acid_example():
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