"""
reaction_joe.py
Author: Joe

This file contains chemistry helper functions for the titration simulator.
Volumes are entered in cm3, but calculations use dm3 because concentration is
measured in mol dm^-3.
"""

STRONG_ACID_NOTE = (
    "Strong acid and strong base titrations have a sharp pH change near "
    "the equivalence point. The equivalence point is close to pH 7."
)

WEAK_ACID_NOTE = (
    "Weak acid and strong base titrations form a buffer region before "
    "the equivalence point. At half-equivalence, pH is approximately pKa."
)


def cm3_to_dm3(volume_cm3):
    
    """
    Converts cm3 to dm3.
    """

    return volume_cm3 / 1000


def dm3_to_cm3(volume_dm3):
    
    """
    Converts dm3 to cm3.
    """

    return volume_dm3 * 1000


def calculate_moles(concentration, volume_cm3):
    
    """
    Calculates moles from concentration and volume.
    """

    volume_dm3 = cm3_to_dm3(volume_cm3)
    return concentration * volume_dm3


def calculate_total_volume(acid_volume_cm3, base_volume_cm3):
    
    """
    Calculates the total solution volume in dm3.
    """

    total_volume_cm3 = acid_volume_cm3 + base_volume_cm3
    return cm3_to_dm3(total_volume_cm3)


def calculate_equivalence_volume(acid_concentration, acid_volume_cm3, base_concentration):
    
    """
    Calculates the base volume needed to reach equivalence.
    """

    acid_moles = calculate_moles(
        acid_concentration,
        acid_volume_cm3
    )

    base_volume_dm3 = acid_moles / base_concentration
    return dm3_to_cm3(base_volume_dm3)


def calculate_half_equivalence_volume(equivalence_volume):
    
    """
    Calculates the half-equivalence volume.
    """

    return equivalence_volume / 2


def get_reaction_note(titration_type):
    
    """
    Returns a short note for the selected titration type.
    """

    if titration_type == "Strong acid vs strong base":
        return STRONG_ACID_NOTE

    return WEAK_ACID_NOTE


def get_ionic_equation(titration_type):
    
    """
    Returns the ionic equation for the selected titration type.
    """

    if titration_type == "Strong acid vs strong base":
        return "H+(aq) + OH-(aq) -> H2O(l)"

    return "HA(aq) + OH-(aq) -> A-(aq) + H2O(l)"


def describe_region(region):
    
    """
    Returns a description of the titration curve region.
    """

    descriptions = {
        "initial": "Only acid is present.",
        "before equivalence": "Acid is still in excess.",
        "buffer region": "Weak acid and conjugate base are both present.",
        "half-equivalence": "At half-equivalence, pH is approximately pKa.",
        "equivalence": "Acid and base have reacted in equal mole amounts.",
        "after equivalence": "Base is in excess."
    }

    return descriptions.get(region, "Point on the titration curve.")


def build_reaction_information(titration_type):
    
    """
    Builds reaction information for the selected titration type.
    """

    return {
        "titration_type": titration_type,
        "ionic_equation": get_ionic_equation(titration_type),
        "note": get_reaction_note(titration_type)
    }
