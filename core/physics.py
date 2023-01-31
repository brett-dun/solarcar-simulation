"""
Module containing functions for physics calculations.
"""

__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"


import math

from core.car import Car
import core.constants as constants
import core.earth as earth


class Air:
    """
    Constants for air.
    """
    molar_mass: float = 0.028964  # <kg/mol>
    specific_gas_constant: float = 287.058  # <J/(kelvin*kg)>


class Water:
    """
    Constants for water.
    """
    class Gas:
        """
        Constants for water vapor.
        """
        molar_mass: float = 0.018016  # <kg/mol>
        specific_gas_constant: float = 461.495  # <J/(kelvin*kg)>


def calculate_pressure_at_altitude(altitude: float) -> float:
    """
    Calculate pressure at the given altitude.

    :param altitude: Altitude above sea level in meters.

    :return: Pressure in pascals.
    """
    return 101325.0 * (1.0 - 2.255773e-5 * altitude)  # <pa>


# TODO: this calculation is not correct with humidity (increasing humidity should decrease density)
def calculate_air_density(temperature: float, altitude: float, humidity: float) -> float:
    """
    Calculate the air density from the given parameters.

    :param temperature: Temperature in Celcius.
    :param alitude: Altitude above sea level in meters.
    :param humidity: Relative humdity [0.0, 1.0]

    :return: Air density in kg/m/m/m.
    """
    air_pressure: float = calculate_pressure_at_altitude(altitude)  # <pa>
    saturation_pressure: float = 133.322 * \
        math.pow(10.0, 8.07131 - 1730.63 / (temperature + 233.426))
    temperature_kelvin: float = temperature + 273.15
    return ((air_pressure * Air.molar_mass) + (humidity * saturation_pressure * Water.Gas.molar_mass)) \
        / (constants.GAS_CONSTANT * temperature_kelvin)


def calculate_rolling_force(mass: float, accel: float, crr: float, angle: float) -> float:
    """
    Calculate the rolling resistance force in Newtons.

    :param mass: Mass of the car in kg.
    :param accel: Acceleration of the car in m/s/s.
    :param crr: Coefficient of rolling resistance.
    :param angle: Angle of the road in radians.

    :return: Rolling resistance force in Newtons.
    """
    return crr * (mass * accel) * math.cos(angle)


def calculate_aero_force(cda: float, rho: float, relative_speed: float) -> float:
    """
    Calculate the aerodynamic force in Newtons.

    :param cda: Coefficient of drag multiplied by frontal area (Cd*A) in meters squared.
    :param rho: Air density in kilograms per cubic meter.
    :param relative_speed: Relative air speed in the direction of travel.

    :return: Aerodyanmic force in Newtons.
    """
    return 0.5 * cda * rho * (relative_speed**2)


def calculate_power_to_drive(car: Car,
                             vehicle_speed: float,
                             angle: float = 0.0,
                             wind_speed: float = 0.0,
                             acceleration: float = 0.0,
                             rho: float = 1.2922,
                             soc=1.0) -> float:
    """
    Calculate the car's power to drive given a car object and physical parameters.
    Does not account for electrical losses in the battery.

    :param car: Car to calculate power usage for.
    :param vehicle_speed: Vehicle speed in m/s.
    :param angle: Angle of the road in radians.
    :param wind_speed: Wind speed in the direction of travel in m/s.
    :param acceleration: Acceleration of the car in m/s/s.
    :param rho: Density of air in kg/m/m/m
    :param soc: State of charge (unitless, 0.0-1.0)

    :return: Returns the power required to drive the car in watts.
    """

    # gravity that the car is fighting, not the force of gravity on the car
    gravity_force = (earth.GRAVITY * car.mass) * math.sin(angle)
    rolling_force = calculate_rolling_force(
        car.mass, earth.GRAVITY, car.crr, angle)
    aero_force = calculate_aero_force(
        car.cda, rho, (vehicle_speed - wind_speed))
    accel_force = acceleration * car.mass

    gravity_power = gravity_force * vehicle_speed
    rolling_power = rolling_force * vehicle_speed
    aero_power = aero_force * vehicle_speed
    accel_power = accel_force * vehicle_speed

    total_power = gravity_power + rolling_power + aero_power + accel_power
    motor_efficiency = 0.95 if soc > 0.2 else 0.8
    real_power = total_power / (motor_efficiency * car.powertrain_efficiency)

    return real_power
