"""

"""

__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"


from dataclasses import dataclass


class RaceState:
    """
    """

    @dataclass(frozen=True)
    class Racing:
        """
        """
        driving: bool

    @dataclass(frozen=True)
    class Night:
        """
        """
        charging: bool
        normalized: bool
        grid_charging: bool

    @dataclass(frozen=True)
    class Checkpoint:
        """
        """
        charging: bool
        normalized: bool

    @dataclass(frozen=True)
    class CheckpointNight:
        """
        """
        charging: bool
        normalized: bool
        grid_charging: bool

    @dataclass(frozen=True)
    class StageStop:
        """
        """
        charging: bool
        normalized: bool
        grid_charging: bool
