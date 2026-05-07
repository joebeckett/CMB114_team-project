"""
validation_caner.py
Author: Caner

This file checks user input before it is used in the calculation code.
It helps stop errors such as negative volumes, missing pKa values, or invalid
menu choices.
"""

MIN_CONCENTRATION = 0.000001
MAX_CONCENTRATION = 10.0

MIN_VOLUME = 0.0
MAX_VOLUME = 10000.0

MIN_GRAPH_POINTS = 20
MAX_GRAPH_POINTS = 1000

MIN_PKA = -5.0
MAX_PKA = 20.0


def validate_menu_choice(choice):
    """
    Checks whether the titration type choice is valid.
    """

    if choice not in [1, 2]:
        raise ValueError("Titration type must be 1 or 2.")


def validate_positive_number(value, field_name):
    """
    Checks that a number is greater than zero.
    """

    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")


def validate_range(value, field_name, minimum, maximum):
    """
    Checks that a value is inside a sensible range.
    """

    if value < minimum or value > maximum:
        raise ValueError(
            f"{field_name} must be between {minimum} and {maximum}."
        )


def validate_concentration(value, field_name):
    """
    Validates a concentration value.
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
    Validates a volume value.
    """

    validate_positive_number(value, field_name)
    validate_range(
        value,
        field_name,
        0.000001,
        MAX_VOLUME
    )


def validate_pka(value):
    """
    Validates pKa for weak acid titrations.
    """

    if value is None:
        raise ValueError("pKa is required for a weak acid titration.")

    validate_range(
        value,
        "pKa",
        MIN_PKA,
        MAX_PKA
    )


def validate_graph_points(value):
    """
    Validates the number of points used to draw the graph.
    """

    if value < MIN_GRAPH_POINTS or value > MAX_GRAPH_POINTS:
        raise ValueError(
            f"Graph points must be between {MIN_GRAPH_POINTS} and {MAX_GRAPH_POINTS}."
        )


def split_selected_volumes(text):
    """
    Splits comma-separated selected volumes into a list of strings.
    """

    if text.strip() == "":
        return []

    parts = text.split(",")
    cleaned_parts = []

    for part in parts:
        cleaned = part.strip()

        if cleaned != "":
            cleaned_parts.append(cleaned)

    return cleaned_parts


def parse_selected_volumes(text, max_volume):
    """
    Converts selected volume text into a list of floats.
    """

    selected_volumes = []
    parts = split_selected_volumes(text)

    for part in parts:
        try:
            volume = float(part)
        except ValueError:
            raise ValueError("Selected volumes must be numbers separated by commas.")

        if volume < MIN_VOLUME:
            raise ValueError("Selected volumes cannot be negative.")

        if volume > max_volume:
            raise ValueError(
                "Selected volumes cannot be greater than the maximum base volume."
            )

        selected_volumes.append(volume)

    return selected_volumes


def choice_to_titration_type(choice):
    """
    Converts a menu choice into a titration type name.
    """

    if choice == 1:
        return "Strong acid vs strong base"

    return "Weak acid vs strong base"


def validate_titration_inputs(raw_data):
    """
    Validates all titration inputs and returns a clean dictionary.
    """

    choice = raw_data["choice"]

    validate_menu_choice(choice)

    acid_concentration = raw_data["acid_concentration"]
    acid_volume = raw_data["acid_volume"]
    base_concentration = raw_data["base_concentration"]
    max_base_volume = raw_data["max_base_volume"]
    graph_points = raw_data["graph_points"]
    pka = raw_data["pka"]

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

    validate_graph_points(graph_points)

    selected_volumes = parse_selected_volumes(
        raw_data["selected_volumes"],
        max_base_volume
    )

    titration_type = choice_to_titration_type(choice)

    if titration_type == "Weak acid vs strong base":
        validate_pka(pka)
    else:
        pka = None

    clean_data = {
        "titration_type": titration_type,
        "acid_concentration": acid_concentration,
        "acid_volume": acid_volume,
        "base_concentration": base_concentration,
        "max_base_volume": max_base_volume,
        "selected_volumes": selected_volumes,
        "graph_points": graph_points,
        "pka": pka
    }

    return clean_data


def validate_filename(filename, extension):
    """
    Validates and fixes export filenames.
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


def get_strong_acid_example():
    """
    Returns example data for a strong acid vs strong base titration.
    """

    return {
        "titration_type": "Strong acid vs strong base",
        "acid_concentration": 0.1,
        "acid_volume": 25.0,
        "base_concentration": 0.1,
        "max_base_volume": 50.0,
        "selected_volumes": [0.0, 10.0, 25.0, 30.0],
        "graph_points": 200,
        "pka": None
    }


def get_weak_acid_example():
    """
    Returns example data for a weak acid vs strong base titration.
    """

    return {
        "titration_type": "Weak acid vs strong base",
        "acid_concentration": 0.1,
        "acid_volume": 25.0,
        "base_concentration": 0.1,
        "max_base_volume": 50.0,
        "selected_volumes": [0.0, 12.5, 25.0, 30.0],
        "graph_points": 200,
        "pka": 4.76
    }