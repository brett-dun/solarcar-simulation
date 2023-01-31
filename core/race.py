"""
Module containing the Race class.
"""

__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"


from dataclasses import dataclass
import math
from typing import List, Optional, Tuple


@dataclass(frozen=True)
class Race:
    """
    Class containing information specific to a race.
    """
    distance_events: List
    time_events: List
    speed_limits: List
    route: Optional[List]

    def get_location(self, distance: float) -> Tuple[float, float]:
        """
        Calculate the car's latitude and longitude given distance along the race route.

        :param distance: Distance along the race route in meters.

        :return: Tuple of latitude and longitude, both in radians.
        """
        # TODO: this is hacky to get something working for WSC
        if distance < 3022 * 1/3:
            return math.radians(-12.425724), math.radians(130.8632684)
        if distance < 3022 * 2/3:
            return math.radians(-29.0135), math.radians(134.7544)
        return math.radians(-34.9284235), math.radians(138.5657262)

    def determine_speed_limit(self, distance: float) -> float:
        """
        Determine the speed limit given the distance along the race route.

        :param distance: Distance in meters along the race route.

        :return: Current speed limit in meters per second.
        """
        if distance >= self.speed_limits[-1].distance:
            return self.speed_limits[-1].speed_limit

        index = 0
        while distance > self.speed_limits[index].distance:
            index += 1
        return self.speed_limits[index].speed_limit
