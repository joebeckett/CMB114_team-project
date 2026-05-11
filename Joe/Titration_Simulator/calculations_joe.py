"""
calculations_joe.py
Author: Joe

This file contains the calculation engine for the titration simulator
"""

import math

from reaction_joe import (
    calculate_moles,
    calculate_total_volume,
    calculate_equivalence_volume,
    calculate_half_equivalence_volume,
    describe_region,
    build_reaction_information
)

WATER_KW = 1e-14
NEUTRAL_PH = 7.0


def clamp_ph(ph):
  
    """
    Keep values limited to the range of pH
    """
  
    if ph < 0:
        return 0.0

    if ph > 14:
        return 14.0

    return ph


def safe_log10(value):
  
    """
    Return a safe log10 value without errors from zero or negative numbers
    """
  
    if value <= 0:
        value = 1e-14

    return math.log10(value)


def ph_from_hydrogen(h_concentration):
  
    """
    Calculate pH from hydrogen ion concentration
    """
  
    if h_concentration <= 0:
        return NEUTRAL_PH

    return clamp_ph(-safe_log10(h_concentration))


def ph_from_hydroxide(oh_concentration):
  
    """
    Calculate pH from hydroxide ion concentration
    """
  
    if oh_concentration <= 0:
        return NEUTRAL_PH

    poh = -safe_log10(oh_concentration)
    return clamp_ph(14 - poh)


def ka_from_pka(pka):
  
    """
    Convert pKa into Ka.
    """
  
    return 10 ** (-pka)


def values_are_close(first, second):
  
    """
    Check if two calculated values are close enough to be treated as equal
    """
  
    return math.isclose(
        first,
        second,
        rel_tol=1e-9,
        abs_tol=1e-12
    )


def calculate_initial_weak_acid_ph(concentration, pka):
  
    """
    Calculate the initial pH of a weak acid before base is added
    """
  
    ka = ka_from_pka(pka)
    h_concentration = math.sqrt(ka * concentration)

    return ph_from_hydrogen(h_concentration)


def calculate_strong_acid_ph(data, base_volume):
  
    """
    Calculate the pH for a strong acid and strong base titration
    """
  
    acid_moles = calculate_moles(
        data["acid_concentration"],
        data["acid_volume"]
    )

    base_moles = calculate_moles(
        data["base_concentration"],
        base_volume
    )

    total_volume = calculate_total_volume(
        data["acid_volume"],
        base_volume
    )

    if base_moles < acid_moles:
        excess_acid = acid_moles - base_moles
        h_concentration = excess_acid / total_volume

        return ph_from_hydrogen(h_concentration)

    if values_are_close(base_moles, acid_moles):
        return NEUTRAL_PH

    excess_base = base_moles - acid_moles
    oh_concentration = excess_base / total_volume

    return ph_from_hydroxide(oh_concentration)


def calculate_weak_acid_ph(data, base_volume):
  
    """
    Calculate the pH for a weak acid and strong base titration
    """
  
    acid_moles = calculate_moles(
        data["acid_concentration"],
        data["acid_volume"]
    )

    base_moles = calculate_moles(
        data["base_concentration"],
        base_volume
    )

    total_volume = calculate_total_volume(
        data["acid_volume"],
        base_volume
    )

    pka = data["pka"]
    ka = ka_from_pka(pka)

    if values_are_close(base_volume, 0):
        return calculate_initial_weak_acid_ph(
            data["acid_concentration"],
            pka
        )

    if base_moles < acid_moles:
        acid_left = acid_moles - base_moles
        conjugate_base = base_moles

        if conjugate_base <= 0:
            return calculate_initial_weak_acid_ph(
                data["acid_concentration"],
                pka
            )

        ph = pka + safe_log10(conjugate_base / acid_left)
        return clamp_ph(ph)

    if values_are_close(base_moles, acid_moles):
        salt_concentration = acid_moles / total_volume
        kb = WATER_KW / ka
        oh_concentration = math.sqrt(kb * salt_concentration)

        return ph_from_hydroxide(oh_concentration)

    excess_base = base_moles - acid_moles
    oh_concentration = excess_base / total_volume

    return ph_from_hydroxide(oh_concentration)


def calculate_single_ph(data, base_volume):
  
    """
    Choose the correct pH calculation for the selected titration type
    """
  
    if data["titration_type"] == "Strong acid vs strong base":
        return calculate_strong_acid_ph(data, base_volume)

    return calculate_weak_acid_ph(data, base_volume)


def classify_region(data, base_volume):
  
    """
    Classify which region of the titration curve the volume is in
    """
  
    equivalence_volume = calculate_equivalence_volume(
        data["acid_concentration"],
        data["acid_volume"],
        data["base_concentration"]
    )

    half_equivalence_volume = equivalence_volume / 2
    tolerance = max(equivalence_volume * 0.002, 0.001)

    if values_are_close(base_volume, 0):
        return "initial"

    if abs(base_volume - equivalence_volume) <= tolerance:
        return "equivalence"

    if data["titration_type"] == "Weak acid vs strong base":
        if abs(base_volume - half_equivalence_volume) <= tolerance:
            return "half-equivalence"

        if base_volume < equivalence_volume:
            return "buffer region"

    if base_volume < equivalence_volume:
        return "before equivalence"

    return "after equivalence"


def calculate_curve_data(data):
  
    """
    Calculate the volumes, pH values, and regions needed for the graph
    """
  
    volumes = []
    ph_values = []
    regions = []

    max_volume = data["max_base_volume"]
    graph_points = data["graph_points"]

    for index in range(graph_points):
        volume = max_volume * index / (graph_points - 1)
        ph = calculate_single_ph(data, volume)
        region = classify_region(data, volume)

        volumes.append(volume)
        ph_values.append(ph)
        regions.append(region)

    return {
        "volumes": volumes,
        "ph_values": ph_values,
        "regions": regions
    }


def calculate_key_points(data):
  
    """
    Calculate the main titration points such as initial and equivalence pH
    """
  
    equivalence_volume = calculate_equivalence_volume(
        data["acid_concentration"],
        data["acid_volume"],
        data["base_concentration"]
    )

    half_equivalence_volume = calculate_half_equivalence_volume(
        equivalence_volume
    )

    initial_ph = calculate_single_ph(data, 0)
    equivalence_ph = calculate_single_ph(data, equivalence_volume)

    if data["titration_type"] == "Weak acid vs strong base":
        half_equivalence_ph = calculate_single_ph(
            data,
            half_equivalence_volume
        )
    else:
        half_equivalence_ph = None

    return {
        "initial_ph": initial_ph,
        "equivalence_volume": equivalence_volume,
        "equivalence_ph": equivalence_ph,
        "half_equivalence_volume": half_equivalence_volume,
        "half_equivalence_ph": half_equivalence_ph
    }


def calculate_selected_point(data):
  
    """
    Calculate the pH and region for the user's selected volume
    """
  
    volume = data["selected_volume"]
    ph = calculate_single_ph(data, volume)
    region = classify_region(data, volume)

    return {
        "volume": volume,
        "ph": ph,
        "region": region,
        "description": describe_region(region)
    }


def calculate_curve_summary(curve_data):
  
    """
    Find the lowest and highest pH values on the titration curve
    """
  
    ph_values = curve_data["ph_values"]
    volumes = curve_data["volumes"]

    lowest_ph = min(ph_values)
    highest_ph = max(ph_values)

    lowest_index = ph_values.index(lowest_ph)
    highest_index = ph_values.index(highest_ph)

    return {
        "lowest_ph": lowest_ph,
        "lowest_ph_volume": volumes[lowest_index],
        "highest_ph": highest_ph,
        "highest_ph_volume": volumes[highest_index]
    }


def calculate_titration(data):
  
    """
    Run all titration calculations and return the full results
    """
  
    curve_data = calculate_curve_data(data)
    key_points = calculate_key_points(data)
    selected_point = calculate_selected_point(data)
    curve_summary = calculate_curve_summary(curve_data)

    reaction = build_reaction_information(
        data["titration_type"]
    )

    return {
        "data": data,
        "curve_data": curve_data,
        "key_points": key_points,
        "selected_point": selected_point,
        "curve_summary": curve_summary,
        "reaction": reaction
    }
