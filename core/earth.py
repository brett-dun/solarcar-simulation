"""
Module for representing constants related to earth.
"""

__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"


EQUATORIAL_RADIUS: float = 6378137.0  # <m>
"""
Earth's equatorial radius in meters.
"""


POLAR_RADIUS: float = 6356752.3  # <m>
"""
Earth's polar radius in meters.
"""


MEAN_RADIUS: float = (EQUATORIAL_RADIUS * 2.0 + POLAR_RADIUS) / 3.0  # <m>
"""
Earth's mean radius in meters.
"""


ATMOSPHERE_THICKNESS = 9000.0  # <m>
"""
Earth's atmospheric thickness in meters.
"""


GRAVITY = 9.807  # <m/sec/sec>
"""
Standard acceleration due to gravity on Earth in meters/second/second.
"""
