"""
Module containing unit conversion functions.
"""

__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"


import time
from datetime import datetime


def date(t: str) -> float:
    """
    Convert time string to seconds since the unix epoch.

    :param t: time string

    :return: seconds since unix epoch
    """
    tz_agnostic = time.mktime(datetime.strptime(
        t, "%Y-%m-%dT%H:%M:%S%z").timetuple())

    sign = t[-6]
    h_offset, m_offset = [int(x) for x in t[-5:].split(':')]
    offset = (h_offset * 60 + m_offset) * 60
    if sign == '+':
        offset = -offset

    tz_aware = tz_agnostic + offset

    return tz_aware


def distance(d: float, unit: str = 'm') -> float:
    """
    Convert the provided distance to distance in meters.

    :param d: Distance with the provided units
    :param unit: str representation of the unit

    :return: Distance in meters
    """
    if unit == 'm':
        return d
    if unit == 'km':
        return d * 1000.0
    raise ValueError(f'unit="{unit}" is not a supported distance unit.')


def duration(t: float, unit: str = 's') -> float:
    """
    Convert the provided duration to duration in seconds.

    :param t: Duration with the provided units
    :param unit: str representation of the unit

    :return: Duration in seconds
    """
    if unit == 's':
        return t
    if unit == 'min':
        return t * 60.0
    if unit == 'h':
        return t * 3600.0
    raise ValueError(f'unit="{unit}" is not a supported duration unit.')


def speed(s: float, unit: str = 'm/s') -> float:
    """
    Convert the provided speed to speed in meters per second.

    :param s: Speed with the provided units
    :param unit: str representation of th unit

    :return: Speed in meters per second
    """
    if unit == 'm/s':
        return s
    if unit in ('km/h', 'kph'):
        return s / 3.6
    if unit in ('mi/h', 'mph'):
        return s / 2.23694
    raise ValueError(f'unit="{unit}" is not a supported speed unit.')
