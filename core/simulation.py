"""
Core simulation code.
"""

__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"


import copy
from typing import Any, Callable, List, Optional, Tuple

from core.car import Car
from core.functions import charge_current_limit_lookup, get_target_speed
from core.physics import calculate_power_to_drive, calculate_air_density
from core.objects import State, RaceActions
from core.process_events import process_events
from core.race import Race
from core.sim_constants import *
import core.sun as sun


def simulate(race: Race,
             car: Car,
             wind_func: Callable[[float, float], float],
             array_model: Callable[[float, float, bool], float],
             end_simulation: Callable[[State], Any],
             battery_size: float,
             state: State,
             race_state: RaceActions,
             target_speeds: List[Tuple[float, float]],
             checkpoint_time_remaining=0.0,
             vehicle_speed=0.0,
             dt=1.0) -> Tuple[bool, State, List[Tuple]]:
    """
    Simulate the race using the provided objects.

    :param race: The race to simulate.
    :param car: The car being raced.
    :param wind_func: Function that returns wind speed given distance
    along the race route and time.
    :param array_model: Function modeling array power given irradiance,
    solar altitude, and whether the array is normalized.
    :param end_simulation: Function that decides whether to end the
    simulation given the current state.
    :param battery_size: Battery size in Joules.
    :param state: State of the environment and the vehicle.
    :param race_state: State of the race.
    :param target_speeds: List of target speed tuples.
    :param checkpoint_time_remaining: Seconds remaining before being
    allowed to leave a checkpoint.
    :param vehicle_speed: The car's current speed.

    :return: Tuple containing whether or not the race could be completed (bool),
    final state, and list containing state information.
    """

    # Add the mass of the two passengers to the car
    car = car.copy_with(mass=car.mass+2*80.0)

    state = copy.deepcopy(state)

    logged_states = [(copy.copy(state), 0.0, 0.0)]

    battery_esr = car.battery.cell_esr * \
        (car.battery.cells_in_series / car.battery.cells_in_parallel)  # <ohm>

    distance_queue = copy.deepcopy(race.distance_events)
    time_queue = copy.deepcopy(race.time_events)

    total_grid_energy = 0.0  # <J>

    while True:

        maybe: Optional[Tuple[RaceActions, float]] = process_events(distance_queue=distance_queue,
                                                                    time_queue=time_queue,
                                                                    state=state,
                                                                    race_state=race_state,
                                                                    checkpoint_time_remaining=checkpoint_time_remaining)

        if maybe:
            race_state, checkpoint_time_remaining = maybe
        else:
            # TODO: we should handle this better (so that it's more clear why we're exiting)
            return False, state, logged_states

        grid_charging = race_state.grid_charging and state.soc < 1.0

        simulation_end_reason = end_simulation(state)

        if simulation_end_reason is not None:
            return simulation_end_reason, state, logged_states

        lat, lon = race.get_location(state.distance)  # figure out where we are

        sun_altitude, _ = sun.get_sun_position(state.time, lon, lat)

        # is this all we need for determining if the car is on?
        car_is_on = sun_altitude > 0.0 or grid_charging

        if checkpoint_time_remaining > 0.0 and race_state.race_hours:
            # print('stopping at checkpoint')
            # Don't allow driving if we have time to serve at the checkpoint
            race_state = RaceActions(clock_running=False,
                                     charging=race_state.charging,
                                     driving=False,
                                     normalized=race_state.normalized,
                                     grid_charging=False,
                                     race_hours=True)
            checkpoint_time_remaining -= dt
            # print('waiting')
        elif race_state.race_hours:
            # Go ahead and resume driving if it is during race hours and
            # there is no more checkpoint time to serve
            race_state = RaceActions(clock_running=True,
                                     charging=True,
                                     driving=True,
                                     normalized=False,
                                     grid_charging=False,
                                     race_hours=True)

        # Determine the speed limit given the car's current location
        speed_limit = race.determine_speed_limit(state.distance)

        # Determine target speed based off of the speed limit and current location
        target_speed = min(speed_limit, get_target_speed(
            target_speeds, state.distance))

        prev_speed = vehicle_speed
        vehicle_speed = target_speed if race_state.driving else 0.0

        if car_is_on:

            """
            Begin Construction Zone

            This is the code that needs to be modified to really bring everything together.
            The other important change to make is the ability of the `Race` class to load .kml files.
            """

            # TODO: calculate this based on where you are along the route
            angle = 0.0
            altitude = 0.0

            # TODO: use the irradiance func instead of calculating power from the sun
            # irradiance = irradiance_func(state.distance, state.time)
            irradiance = sun.get_sun_power(sun_altitude)

            # TODO: use weather_func to use real weather
            wind = wind_func(state.distance, state.time)
            temperature, humidity = 30.0, 0.3

            """
            End Construction Zone
            """

            rho = calculate_air_density(
                temperature=temperature, altitude=altitude, humidity=humidity)  # <kg/m^3>

            ptd = calculate_power_to_drive(
                car, vehicle_speed, wind_speed=wind, angle=angle, rho=rho, soc=state.soc)

            # Charging Calculations

            cell_voltage = car.battery.estimate_cell_voltage_from_soc(
                state.soc)
            battery_voltage = cell_voltage * car.battery.cells_in_series

            max_grid_dc_current = charge_current_limit_lookup(cell_voltage)
            dc_grid_current = min((AC_CHARGE_CURRENT * AC_CHARGE_VOLTAGE *
                                  car.charger_efficiency) / battery_voltage, max_grid_dc_current)
            grid_power = dc_grid_current * battery_voltage if grid_charging else 0.0

            array_power = array_model(
                irradiance, sun_altitude, race_state.normalized) if sun_altitude > 0.0 else 0.0

            # Battery Calculations

            # Calculate the amount of power the battery is receiving
            # (negative = power out, positive = power in)
            battery_power = grid_power + array_power - ptd - car.idle_power_loss

            # Use the pack voltage to calculate the current in/out of the battery
            battery_current = battery_power / battery_voltage  # <A>

            # Use the Equivalent Series Resistance (ESR) and
            # current to calculate the battery power losses
            battery_losses = battery_current**2 * battery_esr  # <W>

            # Calculate the change in kinetic energy from changing speeds
            # Calculate this assuming that on regen we only recover some
            # of the kinetic energy we had
            delta_energy = 0.0  # <J>
            if vehicle_speed > prev_speed:
                delta_energy = 0.5 * car.mass * (vehicle_speed - prev_speed)**2
            elif vehicle_speed <= prev_speed:
                delta_energy = 0.5 * car.mass * \
                    (vehicle_speed - prev_speed)**2 * REGEN_FACTOR

            # Finish Up

            # Subtract losses from the power the battery is providing
            # to the rest of the car to calculate the net power
            net_power = battery_power - battery_losses

            state.distance += vehicle_speed * dt

            state.energy += net_power * dt - delta_energy

            state.soc = state.energy / battery_size

            total_grid_energy += grid_power * dt

            state.time += dt

            logged_states.append(
                (copy.copy(state), array_power, vehicle_speed))

        else:
            # Only increment the time if the car is not on
            state.time += dt
