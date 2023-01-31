"""
Equations and constants related to the sun. All of these came from Sun.cs in the SolarRacer.
"""

__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"


import math
from typing import Tuple

import core.earth as earth


J1970: float = 2440588
"""
Julian days of the J1970 epoch.
"""


J2000: float = 2451545
"""
"2451545.0 is the equivalent Julian year of Julian days for 2000, 1, 1.5, noon"
https://en.wikipedia.org/wiki/Epoch_(astronomy)
"""

"""
Constants for the solar mean anomaly equation.
https://en.wikipedia.org/wiki/Sunrise_equation#Solar_mean_anomaly
"""
M0: float = math.radians(357.5291)
M1: float = math.radians(0.98560028)


"""
Constants for the solar transit equation
https://en.wikipedia.org/wiki/Sunrise_equation#Solar_transit
"""
J1: float = 0.0053
J2: float = -0.0069


"""
Constants for the equation of center
https://en.wikipedia.org/wiki/Equation_of_the_center
"""
C1: float = math.radians(1.9148)
"""
"the coefficient of the Equation of the Center for the planet the
observer is on (in this case, Earth)"
"""
C2: float = math.radians(0.0200)
C3: float = math.radians(0.0003)


P: float = math.radians(102.9372)
"""
Argument of Perihelion
https://en.wikipedia.org/wiki/Sunrise_equation#Ecliptic_longitude
https://en.wikipedia.org/wiki/Argument_of_periapsis
"""


e: float = math.radians(23.45)
"""
"23.44 is Earth's maximum axial tilt toward the sun"
https://en.wikipedia.org/wiki/Sunrise_equation#Declination_of_the_Sun
"""


"""
https://en.wikipedia.org/wiki/Position_of_the_Sun#Ecliptic_coordinates
"""
th0: float = math.radians(280.1600)
th1: float = math.radians(360.9856235)


s_in_day: int = 60 * 60 * 24
"""
Seconds in a day
"""


I_0: float = 1353.0  # <watt/m/m>
"""
Solar intensity external to Earth's atmosphere.
https://en.wikipedia.org/wiki/Air_mass_(solar_energy)#Solar_intensity
"""


Rx: float = earth.MEAN_RADIUS / earth.ATMOSPHERE_THICKNESS
"""
Ratio of Earth's mean radius to its atmospheric thickness.
"""


def date_to_julian_date(date: float) -> float:
    """
    Convert date (in seconds) to Julian date.

    :param date: Date as seconds since unix epoch

    :return: Julian date
    """
    return date / s_in_day - 0.5 + J1970


def get_solar_mean_anomaly(js: float) -> float:
    """
    Calculates the solar mean anomaly given the julian day.

    https://en.wikipedia.org/wiki/Sunrise_equation#Solar_mean_anomaly
    https://en.wikipedia.org/wiki/Mean_anomaly

    :param js: Julian day

    :return: Solar mean anomaly
    """
    return M0 + M1 * (js - J2000)


def get_equation_of_center(m: float) -> float:
    """
    Calculates the equation of center value given the solar mean anomaly.

    https://en.wikipedia.org/wiki/Sunrise_equation#Equation_of_the_center
    https://en.wikipedia.org/wiki/Equation_of_the_center

    :param m: Solar mean anomaly

    :return: Equation of center value
    """
    return C1 * math.sin(m) + C2 * math.sin(2.0 * m) + C3 * math.sin(3.0 * m)


def get_ecliptic_longitude(m: float, c: float) -> float:
    """
    Caculates the ecliptic longitude given the solar mean anomaly and equation of the center value.

    Details: https://en.wikipedia.org/wiki/Sunrise_equation#Ecliptic_longitude

    :param m: Solar mean anomaly
    :param c: Equation of center value

    :return: Ecliptic longitude
    """
    return m + P + c + math.pi  # TODO: is this missing a mod by 360 (2 pi)?


def get_sun_declination(lsun: float) -> float:
    """
    Calculates the declination of the sun given the ecliptic longitude.
    https://en.wikipedia.org/wiki/Sunrise_equation#Declination_of_the_Sun

    :param lsun: Ecliptic longitude

    :return: Sun declination
    """
    return math.asin(math.sin(lsun) * math.sin(e))


def get_right_ascension(lsun: float) -> float:
    """
    https://en.wikipedia.org/wiki/Right_ascension

    :param lsun: Eliptic Longitude

    :return: Right ascension
    """
    # TODO: Find source of this equation (Maybe it's just derived geometrically?)
    return math.atan2(math.sin(lsun) * math.cos(e), math.cos(lsun))


def get_sidereal_time(j: float, lw: float) -> float:
    """
    https://en.wikipedia.org/wiki/Sidereal_time
    https://www.aa.quae.nl/en/reken/sterrentijd.html

    :param j: Julian day
    :param lw: West longitude

    :return: Sidereal time
    """
    return th0 + th1 * (j - J2000) - lw


def get_hour_angle(th: float, a: float) -> float:
    """
    https://en.wikipedia.org/wiki/Hour_angle

    :param th: Sidereal time
    :param a: Right Ascension

    :return: local hour angle
    """
    return th - a


def get_azimuth(th: float, a: float, phi: float, delta: float) -> float:
    """
    Calculate the solar azimuth from the given parameters.

    :param th: Sidereal time
    :param a: Right Ascension
    :param phi: Local Latitude
    :param delta: Solar Declination

    :return: Solar azimuth
    """
    h: float = get_hour_angle(th, a)

    return math.atan2(math.sin(h), math.cos(h) * math.sin(phi) - math.tan(delta) * math.cos(phi))


def get_altitude(th: float, a: float, phi: float, delta: float) -> float:
    """
    https://en.wikipedia.org/wiki/Solar_zenith_angle

    :param th: Sidereal time
    :param a: Right ascension
    :param phi: Local latitude
    :param delta: Solar Declination

    :return: Solar altitude
    """
    h: float = get_hour_angle(th, a)

    # TODO: Find source of this equation
    return math.asin(math.sin(phi) * math.sin(delta) +
                     math.cos(phi) * math.cos(delta) * math.cos(h))


def _get_sun_position(j: float, lw: float, phi: float) -> Tuple[float, float]:
    """
    Calculate the sun's altitude and azimuth given the
    julian day, west longitude, and local latitude.

    :param j: Julian day
    :param lw: West longitude
    :param phi: Local latitude

    :return: Tuple of solar altitude and azimuth in radians.
    """
    m: float = get_solar_mean_anomaly(j)
    c: float = get_equation_of_center(m)
    lsun: float = get_ecliptic_longitude(m, c)
    d: float = get_sun_declination(lsun)
    a: float = get_right_ascension(lsun)
    th: float = get_sidereal_time(j, lw)

    return get_altitude(th, a, phi, d), get_azimuth(th, a, phi, d)


def get_sun_position(date: float, longitude: float, latitude: float) -> Tuple[float, float]:
    """
    Calculate the sun's altitude and azimuth given the date and location.

    :param date: Date as the number of seconds since unix epoch.
    :param longitude: Local longitude as degrees.
    :param latitude: Local latitude as degrees.

    :return: Tuple of solar altitude and azimuth in radians.
    """
    return _get_sun_position(date_to_julian_date(date),
                             -math.radians(longitude),
                             math.radians(latitude))


def get_sun_power(altitude: float) -> float:
    """
    Calculates the shortwave infrarred radiation in watts per square meter given the sun's altitude.

    https://en.wikipedia.org/wiki/Air_mass_(solar_energy)
    https://en.wikipedia.org/wiki/Air_mass_(astronomy)
    https://www.pveducation.org/pvcdrom/properties-of-sunlight/air-mass

    :param alitude: Solar altitude

    :return: Shortwave infrarred radiation in watts/meter/meter.
    """

    # By definition alitude + zenith = pi/2
    zenith = (math.pi / 2.0) - altitude

    # TODO: take elevation above sea level into account?
    am = math.sqrt(math.pow(Rx * math.cos(zenith), 2.0) +
                   2.0 * Rx + 1.0) - Rx * math.cos(zenith)
    """
    air mass
    https://en.wikipedia.org/wiki/Air_mass_(solar_energy)#Calculation
    """

    # https://en.wikipedia.org/wiki/Air_mass_(solar_energy)#Solar_intensity
    return 1.1 * I_0 * math.pow(0.7, math.pow(am, 0.678))
