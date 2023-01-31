"""
Module containing classes for representing different kinds of race events.
"""

__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"


from dataclasses import dataclass


@dataclass(frozen=True)
class StageStop:
    """
    WSC Stage Stop
    """
    name: str
    distance: float  # <m>
    target_arrival: float  # <s>
    latest_arrival: float  # <s>


@dataclass(frozen=True)
class ControlStop:
    """
    WSC Control Stop
    """
    name: str
    distance: float  # <m>
    duration: float  # <s>
    latest_arrival: float  # <s>


@dataclass(frozen=True)
class SpeedLimit:
    """
    Speed limit along the route.
    """
    distance: float  # <m>
    speed_limit: float  # <m/s>


@dataclass(frozen=True)
class StartOfDay:
    """
    Start of driving for a day.
    """
    name: str
    time: float  # <s>


@dataclass(frozen=True)
class EndOfDay:
    """
    End of driving for a day.
    """
    name: str
    time: float  # <s>


@dataclass(frozen=True)
class StartGridCharge:
    """
    Start of a grid charge.
    """
    time: float  # <s>


@dataclass(frozen=True)
class EndGridCharge:
    """
    End of a grid charge.
    """
    time: float  # <s>
