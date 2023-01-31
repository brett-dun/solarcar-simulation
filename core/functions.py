"""
Functions that needed a home.
"""

__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"


from typing import List, Tuple


def charge_current_limit_lookup(cell_voltage: float) -> float:
    """
    Returns the maximum charge current given cell voltage.

    :param cell_voltage: Voltage of a battery cell in volts.

    :return: Maximum charge current in amps.
    """
    if cell_voltage < 4.0:
        return 65.0  # <A>
    if cell_voltage < 4.1:
        return 40.0  # <A>
    return 20.0  # <A>


def get_target_speed(target_speeds: List[Tuple[float, float]], distance: float) -> float:
    """
    Calculates the target speed given a list of target speed tuples and current distance.

    :param target_speeds: List of tuples containing target speeds and the distance
    that target speed starts at.

    :return: Target speed at the current distance along the route.
    """
    # Check if we're past the last target speed
    if distance >= target_speeds[-1][0]:
        return target_speeds[-1][1]

    index = 0
    while distance < target_speeds[index][0]:
        index += 1
    return target_speeds[index][1]
