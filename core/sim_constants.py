"""
Constants that needed a home. Everything in here should
really live somewhere else.
"""

__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"

# Car uses about 30W of power when sitting idle
idle_loss_power = 30.0  # <W>

AC_CHARGE_CURRENT = 30  # <A>
AC_CHARGE_VOLTAGE = 230  # <V>

REGEN_FACTOR = 0.6

charger_efficiency = 0.92

dt = 1.0  # <s>


# These should not actually be constant
angle = 0.0
temperature = 30.0  # <C>
altitude = 0.0  # <m>
humidity = 0.0
