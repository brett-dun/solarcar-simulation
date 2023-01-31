
import itertools
import math
from typing import Dict, List, Tuple

from core.car import Battery, Car
from core.objects import State, RaceActions
from core.race import Race
from core.simulation import simulate


__author__ = "Brett Duncan"
__email__ = "dunca384@umn.edu"


def configuration_checker(race: Race,
                          car: Car,
                          vehicle_speeds: List[float],
                          wind_speeds: List[float],
                          array_power_factors: List[float]) -> Dict[Tuple[float, float, float], Tuple[bool, State, List]]:
    """
    Check under what conditions the given race + car configuration will allow you to finish.

    :param race: Race to evaluate.
    :param car: Car to evaluate the race with.
    :param vehicle_speeds:
    :param wind_speeds:
    :param array_power_factors:

    :return: A dictionary containing keys that are a tuple of vehicle speed, wind speed,
        and array power factor and values that are a tuple of whether or not the car finished
        (bool), minimum SOC, and maximum distance completed.
    """
    def end_simulation(state: State):
        # out of power
        if state.soc <= 0.0:
            return False
        if state.time > race.time_events[-1].time:
            print('out of time')
            return False
        # end of the race
        if state.distance >= race.distance_events[-1].distance:
            return True
        return None

    results = {}

    for vehicle_speed, wind_speed, array_power_factor in itertools.product(vehicle_speeds, wind_speeds, array_power_factors):

        print(
            f'Running simulation with vehicle_speed={vehicle_speed} m/s; wind_speed={wind_speed} m/s; array_power_factor={array_power_factor}...')

        race_state = RaceActions(clock_running=False,
                                 charging=False,
                                 driving=False,
                                 normalized=False,
                                 grid_charging=False,
                                 race_hours=False)

        # start with a full battery
        energy = car.battery.energy_per_cell * \
            (car.battery.cells_in_series * car.battery.cells_in_parallel)
        state = State(distance=0.0, energy=energy, soc=1.0,
                      time=race.time_events[0].time)

        def wind_func(distance: float, time: float):
            return wind_speed  # <m/s>

        def array_model(irradiance: float, sun_altitude: float, normalized: bool):
            normalization_scalar = 1.0 if normalized else math.sin(
                sun_altitude)
            # TODO: don't hardcode these values
            # area = 5.0 m^2, efficiency = 0.25
            return array_power_factor * irradiance * normalization_scalar * 5.0 * 0.25

        target_speeds = [(0.0, vehicle_speed)]

        result, end_state, logged_states = simulate(race=race, car=car, wind_func=wind_func, array_model=array_model,
                                                    end_simulation=end_simulation, battery_size=energy, state=state, race_state=race_state, target_speeds=target_speeds)

        min_soc = min(logged_states, key=lambda s: s[0].soc)[0].soc
        max_distance = max(logged_states, key=lambda s: s[0].distance)[
            0].distance

        # save the result
        results[(vehicle_speed, wind_speed, array_power_factor)
                ] = result, min_soc, max_distance

        print('Simulation complete.')

    print('Done!')

    return results


# TODO: allow speeds and array power to be parameterized as a list or function
def find_smallest_battery(race: Race,
                          car: Car,
                          vehicle_speed: float,
                          wind_speed: float,
                          array_power_factor: float,
                          min_parallel_cells: int,
                          cell_increment: int,
                          verbose: bool = False) -> int:

    def end_simulation(state: State):
        # out of power
        if state.soc <= 0.0:
            return False
        if state.time > race.time_events[-1].time:
            print('out of time')
            return False
        # end of the race
        if state.distance >= race.distance_events[-1].distance:
            return True
        return None

    def wind_func(distance: float, time: float):
        return wind_speed  # <m/s>

    def array_model(irradiance: float, sun_altitude: float, normalized: bool):
        normalization_scalar = 1.0 if normalized else math.sin(
            sun_altitude)
        # TODO: don't hardcode these values
        # area = 5.0 m^2, efficiency = 0.25
        return array_power_factor * irradiance * normalization_scalar * 5.0 * 0.25

    result = False

    # Cells in parallel
    parallel = min_parallel_cells

    # Loop until we're able to finish the race
    while True:

        # Add an additional 2 kg for every cell in parallel
        mass = car.mass + parallel * 2.0

        battery = Battery(car.battery.cell_esr,
                          car.battery.cells_in_series,
                          parallel,
                          car.battery.energy_per_cell)

        new_car = Car(mass,
                      car.cda,
                      car.crr,
                      car.powertrain_efficiency,
                      car.motor_efficiency,
                      battery)

        race_state = RaceActions(clock_running=False,
                                 charging=False,
                                 driving=False,
                                 normalized=False,
                                 grid_charging=False,
                                 race_hours=False)

        # start with a full battery
        energy = new_car.battery.energy_per_cell * \
            (new_car.battery.cells_in_series * new_car.battery.cells_in_parallel)

        state = State(distance=0.0,
                      energy=energy,
                      soc=1.0,
                      time=race.time_events[0].time)

        target_speeds = [(0.0, vehicle_speed)]

        result, end_state, logged_states = simulate(race=race,
                                                    car=new_car,
                                                    wind_func=wind_func,
                                                    array_model=array_model,
                                                    end_simulation=end_simulation,
                                                    battery_size=energy,
                                                    state=state,
                                                    race_state=race_state,
                                                    target_speeds=target_speeds)

        min_soc = min(logged_states, key=lambda s: s[0].soc)[0].soc
        max_distance = max(logged_states, key=lambda s: s[0].distance)[
            0].distance

        if verbose:
            print(parallel, new_car.mass, min_soc, max_distance)

        if result:
            break

        parallel += cell_increment

    return parallel


def find_smallest_battery_cda_range(race: Race,
                                    car: Car,
                                    vehicle_speed: float,
                                    wind_speed: float,
                                    array_power_factor: float,
                                    min_parallel_cells: int,
                                    cell_increment: int) -> Dict[float, int]:

    results = {}

    cda = 0.17

    parallel = min_parallel_cells

    while cda < 0.25:

        new_car = Car(car.mass,
                      cda,
                      car.crr,
                      car.powertrain_efficiency,
                      car.motor_efficiency,
                      car.battery)

        parallel = find_smallest_battery(
            race, new_car, vehicle_speed, wind_speed, array_power_factor, parallel, cell_increment)

        results[cda] = parallel

        print(cda, parallel)

        cda += 0.01

    return results
