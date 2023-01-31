"""
Classes that don't have a home.
"""

__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"


from dataclasses import dataclass


@dataclass
class State:
    """
    State of the race + car.
    """
    distance: float
    energy: float
    soc: float
    time: float


@dataclass(frozen=True)
class RaceActions:
    """
    What's currently happening during the race.
    """
    clock_running: bool
    charging: bool
    driving: bool
    normalized: bool
    grid_charging: bool
    race_hours: bool
