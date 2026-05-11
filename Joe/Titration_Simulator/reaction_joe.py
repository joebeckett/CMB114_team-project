"""
reaction_joe.py
Author: Joe

This file contains chemistry helper functions for the titration simulator.
Volumes are entered in cm3, but calculations use dm3 because concentration is
in mol dm^-3.
"""

STRONG_ACID_NOTE = (
    "Strong acid and strong base titrations usually have an equivalence "
    "point close to pH 7."
)

WEAK_ACID_NOTE = (
    "Weak acid and strong base titrations have a buffer region before "
    "equivalence. At half-equivalence, pH is approximately equal to pKa."
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
    Calculates moles using concentration and volume.
    """

    volume_dm3 = cm3_to_dm3(volume_cm3)
    return concentration * volume_dm3


def calculate_total_volume(acid_volume_cm3, base_volume_cm3):
    
    """
    Calculates total solution volume in dm3.
    """

    total_volume_cm3 = acid_volume_cm3 + base_volume_cm3
    return cm3_to_dm3(total_volume_cm3)


def calculate_equivalence_volume(acid_concentration, acid_volume_cm3, base_concentration):
    
    """
    Calculates the base volume needed for equivalence.
    Assumes a 1:1 acid-base reaction.
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
    Returns a short explanation of the titration type.
    """

    if titration_type == "Strong acid vs strong base":
        return STRONG_ACID_NOTE

    return WEAK_ACID_NOTE


def get_simple_ionic_equation(titration_type):
    
    """
    Returns a simple ionic equation for display.
    """

    if titration_type == "Strong acid vs strong base":
        return "H+(aq) + OH-(aq) -> H2O(l)"

    return "HA(aq) + OH-(aq) -> A-(aq) + H2O(l)"


def describe_region(region):
    
    """
    Explains the region of the titration curve.
    """

    descriptions = {
        "initial": "Only acid is present.",
        "before equivalence": "Acid is still in excess.",
        "buffer region": "Weak acid and conjugate base are both present.",
        "half-equivalence": "pH is approximately equal to pKa.",
        "equivalence": "Acid and base have reacted in equal mole amounts.",
        "after equivalence": "Base is in excess."
    }

    return descriptions.get(region, "Point on the titration curve.")
