"""
Module containing the Car class and related classes.
"""

__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"

from dataclasses import dataclass
from typing import Optional

"""
SOC lookup table.
TODO: update this for the current cells.
"""
lookup_values = [
    1.0,
    0.999,
    0.997,
    0.9941,
    0.9903,
    0.9857,
    0.9801,
    0.9732,
    0.9646,
    0.9539,
    0.939,
    0.9184,
    0.8912,
    0.863,
    0.8418,
    0.8279,
    0.8169,
    0.8072,
    0.7981,
    0.7897,
    0.7815,
    0.7735,
    0.7657,
    0.7576,
    0.7494,
    0.7409,
    0.7319,
    0.7221,
    0.7118,
    0.7004,
    0.6878,
    0.674,
    0.6596,
    0.6451,
    0.631,
    0.6178,
    0.6053,
    0.593,
    0.5814,
    0.5702,
    0.559,
    0.5478,
    0.5371,
    0.5263,
    0.5156,
    0.5052,
    0.4949,
    0.4844,
    0.4742,
    0.4639,
    0.4533,
    0.4425,
    0.4316,
    0.4199,
    0.4081,
    0.3958,
    0.3832,
    0.3697,
    0.3565,
    0.3431,
    0.3296,
    0.3163,
    0.3036,
    0.2912,
    0.2796,
    0.2688,
    0.259,
    0.2496,
    0.2411,
    0.2326,
    0.223,
    0.2124,
    0.2019,
    0.1915,
    0.1813,
    0.1716,
    0.1621,
    0.1533,
    0.1458,
    0.1398,
    0.1347,
    0.1301,
    0.1259,
    0.1217,
    0.1176,
    0.1139,
    0.1103,
    0.1066,
    0.1032,
    0.1,
    0.0968,
    0.0936,
    0.0906,
    0.0877,
    0.0848,
    0.082,
    0.0793,
    0.0764,
    0.0737,
    0.071,
    0.0682,
    0.0653,
    0.0624,
    0.0594,
    0.0563,
    0.0534,
    0.0505,
    0.0477,
    0.0452,
    0.0428,
    0.0406,
    0.0384,
    0.0363,
    0.0342,
    0.0321,
    0.03,
    0.0281,
    0.0261,
    0.0243,
    0.0225,
    0.0207,
    0.0191,
    0.0175,
    0.0159,
    0.0144,
    0.0129,
    0.0115,
    0.0101,
    0.0088,
    0.0075,
    0.0063,
    0.005,
    0.0039,
    0.0027,
    0.0016,
    0.0
]


@dataclass(frozen=True)
class Battery:
    """
    Class for reprenting battery related parameters.
    """
    cell_esr: float  # <ohm>
    cells_in_series: int
    cells_in_parallel: int
    energy_per_cell: float  # <J>

    def estimate_cell_voltage_from_soc(self, soc: float) -> float:
        """
        Estimate battery cell voltage from state of charge (SOC).

        :param soc: State of Charge (unitless, 0.0-1.0)

        :return: Battery cell voltage in volts.
        """

        step = 0.01  # <V>
        lookup_min_voltage = 2.799  # <V>

        index = 0
        if soc < lookup_values[-1]:
            index = len(lookup_values) - 1
        else:
            while index < len(lookup_values) and soc < lookup_values[index]:
                index += 1

        return lookup_min_voltage + (len(lookup_values)-1 - index) * step

    def estimate_battery_voltage_from_soc(self, soc: float) -> float:
        """
        Estimate battery pack voltage from state of charge (SOC).

        :param soc: State of Charge (unitless, 0.0-1.0)

        :return: Battery pack voltage in volts.
        """
        return self.estimate_cell_voltage_from_soc(soc=soc) * self.cells_in_series


@dataclass(frozen=True)
class Car:
    """
    Class for reprepresenting car related paramters.
    """
    mass: float  # <kg>
    cda: float  # <m^2>
    crr: float
    idle_power_loss: float  # <W>
    powertrain_efficiency: float
    motor_efficiency: float
    charger_efficiency: float
    battery: Optional[Battery]

    def copy_with(self, **kwargs):
        d = self.__dict__.copy()
        for k, v in kwargs.items():
            if k in d:
                d[k] = v
            else:
                raise ValueError(f'Attempted to update unknown field `{k}`')
        return Car(**d)
